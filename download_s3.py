"""
download data from aws s3 bucket pandas-coverage
"""

import gdown
import re

# paste the raw url below
url = 'https://drive.google.com/file/d/1nZ2-ZYk_IWBHDBHtBtOpseaQr05B8zIA/view?usp=sharing'
id_ = re.search(r'file/d/(.*)/view?', url).group(1)
url = f'https://drive.google.com/uc?export=download&id={id_}'
print('url', url)
output = 'coverage.db'
gdown.download(url, output, quiet=False)

