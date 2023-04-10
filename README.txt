＜使用するまでの大まかな流れ＞
①slackアプリを作る(GUIのslackとは別)
②ワークスペースの何にアクセスする権限がほしいかを選択する(scope)
③権限を付与するパスワードみたいなものを発行する(OAuth Tokens)
④slackの対象のチャンネルに、作成したappを追加する。
⑤pythonでapiのmethods(conversations.historyとconversations.replies)を使ってデータを抽出する


＜identifier＞
チャンネルの指定
https://2023-y1v4054.slack.com/archives/Cxxxxxxxxxx
「Cxxxxxxxxxx」の部分がchannnelのidentifier

スレッドの指定
https://2023-y1v4054.slack.com/archives/Cxxxxxxxxxx/p1234567890123456
「1234567890123456」の部分を「1234567890.123456」のように(10文字).(6文字)と分けたものがtsのidentifier

※それぞれのurlはweb版slackから取得可能。


＜必要なscope＞
Bot Tiken Scopesの
channels:history
channels:read
files:read
files:write

※scopeを追加したら、reinstall appを実行する必要がある。

＜参考＞
https://www.estie.jp/blog/entry/2022/11/02/110000

https://dev.classmethod.jp/articles/slackapi-message-history/

https://api.slack.com/methods/conversations.replies

https://api.slack.com/methods/conversations.history
