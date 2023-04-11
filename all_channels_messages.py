import requests
import json
import datetime
import os
import shutil

# Bot User OAuth Token を指定
SLACK_ACCESS_TOKEN = "xxxx-0000000000000-1111111111111-AAAA1111bbbb2222CCCC3333"


# APIから情報をもらうために必要なheaderを作る関数
def MakeHeader(token):
    header = {
        "Authorization": "Bearer {}".format(token)
    }
    return header


# チャンネル一覧を取得する関数
def GetChannelsInfo(token):
    ChanReadURL = "https://slack.com/api/conversations.list"
    ChanReadRes = requests.get(ChanReadURL, headers=MakeHeader(token))
    channel_list = ChanReadRes.json()["channels"]

    ChannelIdNameList = []
    for channel in channel_list:
        ChannelName = channel["name"]
        ChannelId = channel["id"]
        ChannelIdNameList.append([ChannelName, ChannelId])
    return ChannelIdNameList


# ファイルをダウンロードする関数
def download_image(file_url, file_path, token):
    r = requests.get(file_url, headers=MakeHeader(token))
    with open(file_path, "wb") as f:
        f.write(r.content)


# チャンネルごとのフォルダを作る関数
def MkDirForEachChan(token):
    # 大元のフォルダ
    now = datetime.datetime.now()
    folder_name = now.strftime("%Y%m%d_%H%M%S")
    os.makedirs(folder_name)
    for name, id in GetChannelsInfo(token):
        channnel_folder = os.path.join(folder_name, name)
    return folder_name


# チャンネル内の全メッセージを取得する関数
def GetChannelThreads(token, channel_id):
    # 使用するAPIのメソッドのURL
    ConvHisURL = "https://slack.com/api/conversations.history?channel=" + channel_id
    ConvRepURL = "https://slack.com/api/conversations.replies"

    ConvHisRes = requests.get(ConvHisURL, headers=MakeHeader(token)).content
    ConvHisData = json.loads(ConvHisRes)

    # 出力するデータのリスト
    writeTextList = []
    # ダウンロードしたファイルの一時保管場所
    tmp_folder = "tmp/tmp_{}".format(channel_id)
    os.makedirs(tmp_folder)

    # チャンネルへ正常にアクセスできている場合の処理
    if ConvHisData["ok"] == True:
        # データをデコードし、リストへ格納する
        ThreadList = ConvHisData["messages"]
        for messages in ThreadList:
            # スレッドのIDを取得
            THREAD_NUMBER = messages["ts"]  # tsはスレッドの識別子。
            dt = datetime.datetime.fromtimestamp(float(token))

            # スレッドのメッセージとリプライを取得
            payload = {
                "channel": channel_id,
                "ts": THREAD_NUMBER
            }
            ConvRepRes = requests.get(
                ConvRepURL, headers=MakeHeader(token), params=payload)

            ThreadJson = ConvRepRes.json()
            ThreadMessages = ThreadJson["messages"]
            if 0 != len(ThreadMessages):
                for reply in ThreadMessages:
                    dt = datetime.datetime.fromtimestamp(float(reply["ts"]))
                    ReplyText = reply["text"]
                    if "files" in reply:
                        for file_info in reply["files"]:
                            file_id = file_info["id"]
                            file_name = file_info["name"]
                            file_url = file_info["url_private_download"]
                            ReplyText = "{}\n{}\n{}\n{}\n{}\n".format(
                                dt, ReplyText, file_id, file_name, file_url)
                            # ファイルをダウンロードする
                            file_path = os.path.join(tmp_folder, file_name)
                            download_image(file_url, file_path, token)
                    else:
                        ReplyText = "{}\n{}\n".format(dt, ReplyText)
                    writeTextList.append(ReplyText)
            writeTextList.append("----------------------------------------")

    # チャンネルにアクセスできていない場合の処理。
    else:
        writeTextList.extend(
            ["チャンネルID:{}".format(channel_id), "エラーメッセージ:{}".format(
                ConvHisData["error"]), "エラーです。チャンネルにアクセスすることができません。一部のチャンネルのみでこのエラーが出る場合は、チャンネルにアプリが追加されていないことが原因である可能性が高いです。"]
        )
    return writeTextList, tmp_folder


# 実際の処理
os.makedirs("tmp", exist_ok=True)
out_folder = MkDirForEachChan(SLACK_ACCESS_TOKEN)

for name, id in GetChannelsInfo(SLACK_ACCESS_TOKEN):
    message_list, tmp_folder = GetChannelThreads(SLACK_ACCESS_TOKEN, id)

    # 一時保管フォルダの中身を移動
    shutil.move(tmp_folder, "{}/{}/files".format(out_folder, name))

    # リストのデータ(取得したメッセージ)をファイルへ出力する
    if 0 != len(message_list):
        obj = map(lambda x: x + "\n", message_list)
        with open("{}/{}/message.txt".format(out_folder, name), "a", encoding="utf-8", newline="\n") as f:
            f.writelines(obj)
