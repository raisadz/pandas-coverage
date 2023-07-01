"""
download data from aws s3 bucket pandas-coverage
"""

import gdown

#url = 'https://drive.google.com/uc?id=0B9P1L--7Wd2vNm9zMTJWOGxobkU'
url = 'https://drive.google.com/uc?export=download&id=1swBRvmM79dETlHQQ6ZRRTubHcPGar-vo'
output = 'coverage.db'
gdown.download(url, output, quiet=False)

