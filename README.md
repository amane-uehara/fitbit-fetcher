FitbitのデータをPCにバックアップするためのスクリプト
====================================================

Linux環境にデータをバックアップするための環境を構築する。

アプリアカウントの作成
----------------------

<https://dev.fitbit.com/apps>

のREGISTER AN APPからアプリを登録。

|項目|値|
|:--|:--|
|Application Name| てきとう|
|Description| てきとうに10文字以上|
|Application Website| http://www.てきとう|
|Organization| てきとう|
|Organization Website| http://www.てきとう|
|OAuth 2.0 Application Type **Personal**|
|Callback URL| **http://127.0.0.1:8080/**  (最後のスラッシュが大事)|
|Default Access Type| **Read-Only**|

入力後に登録すると
<https://dev.fitbit.com/apps/details/@@@ClientId@@@>
に飛ぶ。

* OAuth 2.0 Client ID
* Client Secret

をメモ。

OAuth2.0周りの準備
------------------

OAuth 2.0 tutorial pageに移動。

Flow typeをAuthorization Code Flow にする。

* Fitbit URL:
* Fitbit API URL:
* OAuth 2.0 Client ID:
* Client Secret:
* Redirect URI:

が自動で入力されているはず。

<https://www.fitbit.com/oauth2/authorize?response_type=token&client_id=...>

のようなリンクに跳び、許可を押す。

URLバーの
<http://localhost:8888/callback?code=@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#_=_">
の`@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@`をコピーする。
`1A Get Code`に貼り付ける

CURLコマンドが出るのでCUIで実行。
JSON形式で結果が得られるのでコピーしてメモ

`2 Parse response`
に貼り付ける

`3 Make Request`
が生成される。

CURLコマンドが出るので、CUIで実行。最後の部分のURLを
<https://dev.fitbit.com/reference/web-api/heart-rate/#get-heart-rate-intraday-time-series>
を参考に
<https://api.fitbit.com/1/user/-/activities/heart/date/today/1d/1sec/time/00:00/00:01.json>
などに変更してうまくいくことを確かめる。

`token.json`の作成
--------------

さっきメモしたJSONテキストを`token.json`という名前のファイルに保存する。
形式の詳細は`sample_token.json`を参照。

`client.txt`の作成
--------------

さっきメモしたClient IDとClient Secretを

```python
ClientID
ClientSecret
```

という2行のテキスト形式で、`client.txt`という名前のファイルに保存する。
形式の詳細は`sample_client.txt`を参照。

fitbit公式のpythonリポジトリの導入
----------------------------------

以下のコマンドを実行

```sh
$ sh install.sh
```

以下のようになればOK

```
$ ls
README.md
client.txt
fetch.py
install.sh
python-fitbit
sample_client.txt
sample_token.json
token.json
```

データの取得
--------

UNIX-likeなシェルがあれば

```sh
$ python3 fetch.py client.txt token.json /path/to/save/dir 20210101
```

とすれば、`/path/to/save/dir`以下に2021年1月1日のFitbitのデータが保存される。


LICENSE
-------

MIT
