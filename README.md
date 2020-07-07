# seika_price_scraper.py
[青果物卸売市場調査（日別調査）](https://www.seisen.maff.go.jp/seisen/bs04b040md001/BS04B040UC020SC998-Evt001.do)にて提供されている卸売市場データをダウンロードし、文字コードを Shift JIS から UTF-8 に変換し、各中央卸売市場別に分類するプログラムです。

GitHubでは空のディレクトリをaddすることができないので表示されていませんが、本来は以下のような構造になっています。

```
seika_price_scraper/
├── data/
│   ├── hirosima/
│   │   ├── k/
│   │   └── y/
│   ├── hukuoka/
│   ...
├── temp/
├── .gitignore
├── LICENSE
├── Pipfile
├── Pipfile.lock
├── README.md
└── seika_price_scraper.py
```

これらのフォルダが存在する状態で seika_price_scraper.py を実行すると動きます。

これらのフォルダが存在しない場合、`make_region_folders.py`を実行することでフォルダを作成することができます。

`seika_price_scraper.py`内の日付を変更して実行することで随時データを更新することができます。

`to_db.py`は、`data`フォルダ内のデータをもとにデータベースファイルを作成します。