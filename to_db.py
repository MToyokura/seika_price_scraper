import os
from pathlib import Path
import pandas
import sqlite3


conn = sqlite3.connect('seika_hibetsu.db')

for root, dirs, files in os.walk('data'):
    if files:
        for csv_file in files:
            file_path = Path(root, csv_file)
            print(file_path)
            pandas.read_csv(file_path).to_sql(con=conn, name="hibetsu", index=False, if_exists="append")
