import requests
import datetime
import os
import shutil

# スクリプトファイルのあるディレクトリをカレントディレクトリにする
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Bot User OAuth Token を指定
SLACK_ACCESS_TOKEN = "xxxx-0000000000000-1111111111111-AAAA1111bbbb2222CCCC3333"


# APIから情報をもらうために必要なheaderを作る関数
def MakeHeader(token):
    header = {
        "Authorization": "Bearer {}".format(token)
    }
    return header


# SlackAPIからレスポンスを受け取る関数
def GetSlackApiResponse(url, token, params=None):
    response = requests.get(url, headers=MakeHeader(token), params=params)
    return response


# チャンネル一覧を取得する関数
def GetChannelsInfo(token):
    ChanReadURL = "https://slack.com/api/conversations.list"
    ChanReadRes = GetSlackApiResponse(ChanReadURL, token)
    # channelsキーが存在しない場合には空のリストをデフォルト値として取得
    channel_list = ChanReadRes.json().get("channels", [])

    ChannelIdNameList = [[channel["name"], channel["id"]]
                         for channel in channel_list]
    return ChannelIdNameList


# ファイルをダウンロードする関数
def download_image(file_url, file_path, token):
    res = GetSlackApiResponse(file_url, token)
    with open(file_path, "wb") as f:
        f.write(res.content)


# 指定した親ディレクトリ内に新しいディレクトリを作り、そのパスを返す関数
def MkDir(parent_dir, folder_name):
    created_folder_path = os.path.join(parent_dir, folder_name)
    os.makedirs(created_folder_path, exist_ok=True)
    return created_folder_path


# チャンネル内の全メッセージを取得する関数
def GetChannelThreads(token, channel_id):
    # 使用するAPIのメソッドのURL
    ConvHisURL = "https://slack.com/api/conversations.history?channel=" + channel_id
    ConvRepURL = "https://slack.com/api/conversations.replies"
    # メソッドを使ってチャンネルの情報を取得
    ConvHisData = GetSlackApiResponse(ConvHisURL, token).json()

    # 出力するメッセージデータのリスト
    writeTextList = []
    # ダウンロードしたファイルの一時保管場所
    tmp_folder = os.path.join("tmp_for_files", "tmp_{}".format(channel_id))
    os.makedirs(tmp_folder)

    # チャンネルへ正常にアクセスできている場合の処理
    if ConvHisData["ok"] == True:
        # データをデコードし、リストへ格納する
        ThreadList = ConvHisData["messages"]
        for messages in ThreadList:
            # スレッドのIDを取得
            THREAD_NUMBER = messages["ts"]  # tsはスレッドの識別子。
            dt = datetime.datetime.fromtimestamp(float(THREAD_NUMBER))

            # スレッドのメッセージとリプライを取得
            payload = {
                "channel": channel_id,
                "ts": THREAD_NUMBER
            }
            ThreadMessages = GetSlackApiResponse(
                ConvRepURL, token, payload).json()["messages"]
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
# 出力先のフォルダを作成
now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
out_folder_path = MkDir("out", now)


for channel_name, channel_id in GetChannelsInfo(SLACK_ACCESS_TOKEN):
    message_list, tmp_folder = GetChannelThreads(
        SLACK_ACCESS_TOKEN, channel_id)
    channel_folder_path = MkDir(out_folder_path, channel_name)

    # 一時保管フォルダの中身を移動
    shutil.move(tmp_folder, os.path.join(channel_folder_path, "files"))

    # リストのデータ(取得したメッセージ)をファイルへ出力する
    if 0 != len(message_list):
        obj = map(lambda x: x + "\n", message_list)
        with open(os.path.join(channel_folder_path, "message.txt"), "a", encoding="utf-8", newline="\n") as f:
            f.writelines(obj)

os.rmdir("tmp_for_files")
