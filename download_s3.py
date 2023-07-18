"""
download data from aws s3 bucket pandas-coverage
"""

import gdown

url = 'https://drive.google.com/uc?export=download&id=1w12bgXVSVMzCui2EOGVuuXSZ5Ql-Nk82'
output = 'coverage.db'
gdown.download(url, output, quiet=False)

