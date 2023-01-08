import gdown 

url = 'https://drive.google.com/uc?id=1RqLvO0NA5yutlXreo8MdoewQdyVGi77h'
output = 'output/pandas-dev/.coverage'
gdown.download(url, output)
