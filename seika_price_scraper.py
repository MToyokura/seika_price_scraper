"""
    seika_price_scraper
    ~~~~~
    青果物卸売市場調査（日別調査）
    (https://www.seisen.maff.go.jp/seisen/bs04b040md001/BS04B040UC020SC998-Evt001.do)
    にて提供されている卸売市場データをダウンロードし、
    文字コードを Shift JIS から UTF-8 に変換し、
    各中央卸売市場別に分類するプログラム。
"""

import requests
import os
import zipfile
import codecs
from pathlib import PurePath
import shutil
import time


for year in range(2019, 2020):
    for month in range(1, 13):
        for day in range (1, 4):
            s027year = str(year)
            if month < 10:
                s027month = '0' + str(month)
            else:
                s027month = str(month)
            s027tendays = str(day)
            print(s027year, s027month, s027tendays)

            payload = {'s027.sessionId':'A73643EEB3F962A029081A74E6E98CD2','s027.year': s027year, 's027.month': s027month, 's027.tendays': s027tendays, 's027.chohyoFileType': 'CSV'}
            zipped_csv = requests.post('https://www.seisen.maff.go.jp/seisen/bs04b040md001/BS04B040UC020SC002-Evt001.do', data=payload)

            if zipped_csv.status_code == 200:
                print('Status: 200')
                with open(PurePath('temp', s027year + s027month + s027tendays + '_CSV.zip'), 'wb') as f:
                        for chunk in zipped_csv.iter_content(chunk_size=1024): 
                            if chunk:
                                f.write(chunk)
            else: 
                print('Status: Error')
                continue

            # tempフォルダ内にダウンロードし、その場で解凍、文字コード変換、分類を行う
            # zipファイルを解凍する
            os.chdir('temp')
            zip_list = os.listdir()
            for a in zip_list:
                print(a)
                with zipfile.ZipFile(a, 'r') as zip_ref:
                    zip_ref.extractall()
                os.remove(a)
            
            # Shift JIS から UTF-8 に変換する
            csv_file_list = os.listdir()
            for i in csv_file_list:
                with codecs.open(i, 'r', 'cp932') as rf:
                    u = rf.read()
                with codecs.open(i, 'w', 'utf-8') as wf:
                    wf.write(u)

            # 各卸売市場別にフォルダを分ける
            # ワーキングディレクトリを一つ上にする
            os.chdir('../')

            regions = ['hirosima', 'hukuoka', 'kanazawa', 'kitakyu', 'kobe', 'kyoto', 'nagoya', 'okinawa',
                    'oosaka', 'sapporo', 'sendai', 'takamatu', 'tokyo', 'yokohama']
            total = 'total'
            
            # temp フォルダ内の一つ一つを見ていき、data フォルダ内に収めていく
            read_folder = 'temp'
            parent_write_folder = 'data'
            files_list = os.listdir(read_folder)
            for i in files_list:
                copy_src = PurePath(read_folder, i)
                # 全国合計は 'kk.csv' と 'ky.csv' というファイル名なので別で扱う
                if i.find('kk.csv') != -1:
                    # 'kk.csv' が見つかった場合
                    copy_dst = PurePath(parent_write_folder, 'total','k' ,i)
                elif i.find('ky.csv') != -1:
                    # 'ky.csv' が見つかった場合
                    copy_dst = PurePath(parent_write_folder, 'total','y' ,i)
                else:
                    # 全国合計以外の場合
                    for u in regions:
                        if i.find(u) != -1:
                            if i.find('tk') != -1:
                                seika_type =  'k'
                            elif i.find('ty') != -1:
                                seika_type =  'y'
                            copy_src = PurePath(read_folder, i)
                            copy_dst = PurePath(parent_write_folder, u, seika_type ,i)
                print(copy_src,'\n',copy_dst)
                shutil.copyfile(copy_src, copy_dst)

                # tempフォルダ内のファイルを削除する
                os.remove(PurePath(read_folder, i))

            # サーバー負荷を下げるために一応間隔をあける
            time.sleep(2)
