# このプロジェクト
勉強用として、機械学習アプリを作りました。バックエンドはGoogleCloud上にフロントエンドはFirebaseでホスティングする予定です 音楽雑誌、音楽書籍から文章を抜き出し、前処理後、WordEmbeddingを実装したライブラリで学習し、アーティストの近傍探索ができるアプリとなります。 このレポジトリはバックエンドのプロジェクトとなります。

# 利用技術一覧
!["Python badge"](https://img.shields.io/badge/-Python-a.svg?logo=Python&style=flat)
!["GCP badge"](https://img.shields.io/badge/-Google%20Cloud%20Platform-a.svg?logo=google%20cloud&style=flat)
!["Github badge"](https://img.shields.io/badge/-Github-181717.svg?logo=github&style=flat)
!["Neo4j badge"](https://img.shields.io/badge/-Neo4j-a.svg?logo=neo4j&style=flat)
!["Elasticsearch badge"](https://img.shields.io/badge/-Elasticsearch-005571.svg?logo=Elasticsearch&style=flat)
!["Ubuntu badge"](https://img.shields.io/badge/-Ubuntu-E95420.svg?logo=Elasticsearch&style=flat)
# 全体構成図
![Image](https://github.com/user-attachments/assets/d5aa1344-8b51-4ed0-a3ce-05229ea8b29b)
# バックエンドプロジェクト構成
<pre>
ROOT
|
|-app.py ＃Webアプリのメイン部分リクエストを直接受け付ける
│-Dockerfile　＃CloudRunというサーバーレス環境でコンテナを実行するための設定ファイル
│-readme.md
│-requirements.txt　＃ビルドのタイミングでインストールするpythonモジュール一覧
│
├─elasticsearch_model
│    emodel.py　＃DBへアクセスするためのコアモジュール
│    helper_for_disp.py　＃DBの検索結果をレイアウトに合わせるためのヘルパー
│    helper_for_search.py　＃DBの検索をするためのヘルパー
│  
└─neo4j_model
      nmodel.py　＃グラフDBへアクセスするためのコアモジュール
      urlutil.py　＃DBの検索結果をレイアウトに合わせたりするためのヘルパー
    
</pre>
# API仕様

### サジェスト検索(入力補完)
* 概要</br>
検索ボックスにアーティスト名を入力するごとに名前候補のリストを返す
* URL</br>
/suggest
* パラメーター</br>
    <table>
        <thead>
            <tr>
                <th>パラメータ名</th> <th>説明</th>
            </tr>
        </thead>
            <tr>
                <td> suggest </td> <td>アーティス名の部分集合</td>
            </tr>
    </table>
### アーティスト詳細情報
* 概要</br>
アーティスト名の詳細情報と代表曲をリリース。リリースはYoutubeURL
* URL</br>
/get_artist_detail_with_releases
* パラメーター</br>
    <table>
        <thead>
            <tr>
                <th>パラメータ名</th> <th>説明</th>
            </tr>
        </thead>
            <tr>
                <td> artist_name_trance_remove_kakko </td> <td>アーティスト名（日本語）</td>
            </tr>
            <tr>
                <td> artist_name_kakko_none_en </td> <td>>アーティスト名（アルファベット）</td>
            </tr>
            <tr>
                <td> artistID </td> <td>アーティストID</td>
            </tr>
    </table>
### 近傍アーティスト
* 概要</br>
アーティストの近傍アーティストを返す
* URL</br>
/nn_neighbor_artist
* パラメーター</br>
    <table>
        <thead>
            <tr>
                <th>パラメータ名</th> <th>説明</th>
            </tr>
        </thead>
            <tr>
                <td> artist_name_trance_remove_kakko </td> <td>>アーティスト名（日本語）</td>
            </tr>
            <tr>
                <td> artist_name_kakko_none_en </td> <td>>アーティスト名（アルファベット）</td>
            </tr>
            <tr>
                <td> artistID </td> <td>アーティストID</td>
            </tr>
    </table>
### メインディスプレイ
* 概要</br>
ランダムにアーティストを複数表示用に返す
* URL</br>
/maindisp
* パラメーター</br>
    <table>
        <thead>
            <tr>
                <th>パラメータ名</th> <th>説明</th>
            </tr>
        </thead>
            <tr>
                <td>  </td> <td>なし</td>
            </tr>
    </table>



