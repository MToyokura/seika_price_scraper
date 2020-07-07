# Creates nested directory for saving the downloaded data.

import os
from pathlib import Path

if not 'data' in os.listdir():
    region_folders_names = ['hirosima', 'hukuoka', 'kanazawa', 'kitakyu', 'kobe', 'kyoto', 'nagoya', 'okinawa', 'oosaka', 'sapporo', 'sendai', 'takamatu', 'tokyo', 'total', 'yokohama']
    for region in region_folders_names:
        Path('data', region, 'k').mkdir(parents=True)
        Path('data', region, 'y').mkdir(parents=True)

# Also create temp folder.
if not 'temp' in os.listdir():
    os.mkdir('temp')