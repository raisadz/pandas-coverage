import gdown 

url = 'https://drive.google.com/uc?id=16Y8SSNqMDGyIhedgF6BzASSXtKZIL89u'
output = 'output/pandas-dev/.coverage'
gdown.download(url, output)
