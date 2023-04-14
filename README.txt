＜使用するまでの大まかな流れ＞
①slackアプリを作る(GUIのslackとは別)
②ワークスペースの何にアクセスする権限がほしいかを選択する(scope)
③権限を付与するパスワードみたいなものを発行する(OAuth Tokens)
④slackの対象のチャンネルに、作成したappを追加する。
⑤pythonでapiのmethods(conversations.historyとconversations.replies)を使ってデータを抽出する

＜tokenの設定＞
slackAPIのページでtokenが発行されたら、環境変数として設定してください。
変数名はSLACK_ACCESS_TOKENです。複数のワークスペースで使用したい場合は、スクリプト毎に変数名の変更が必要です。
（そのうち改善します。）

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
