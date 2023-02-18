＜大まかな流れ＞
①slackアプリを作る(GUIのslackとは別)
②ワークスペースの何にアクセスする権限がほしいかを選択する(scope)
③権限を付与するパスワードみたいなものを発行する(OAuth Tokens)
④pythonでapiのmethods(conversations.historyとconversations.replies)を使ってデータを抽出する


＜identifier＞
チャンネルの指定
https://2023-y1v4054.slack.com/archives/Cxxxxxxxxxx
「Cxxxxxxxxxx」の部分がchannnelのidentifier

スレッドの指定
https://2023-y1v4054.slack.com/archives/Cxxxxxxxxxx/p1234567890123456
「1234567890123456」の部分を「1234567890.123456」のように(10文字).(6文字)と分けたものがtsのidentifier

それぞれのurlはslckから取得可能。


＜ソースコードイメージ＞
conversations.historyでtsを取得。取得したtsを使ってconversation.repliesを使えばリプライを含めたメッセージが取得できる。


＜参考＞
https://www.estie.jp/blog/entry/2022/11/02/110000

https://dev.classmethod.jp/articles/slackapi-message-history/

https://api.slack.com/methods/conversations.replies

https://api.slack.com/methods/conversations.history
