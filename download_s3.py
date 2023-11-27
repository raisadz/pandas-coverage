"""
download data from aws s3 bucket pandas-coverage
"""

import gdown
import re

url = 'https://drive.google.com/uc?export=download&id=1w12bgXVSVMzCui2EOGVuuXSZ5Ql-Nk82'
id_ = re.search(r'download&id=(.*)', url).group(1)
url = f'https://drive.google.com/file/d/{id_}/view?usp=sharing'
print('url', url)
output = 'coverage.db'
gdown.download(url, output, quiet=False)

