import gdown 
import kaggle

from kaggle.api.kaggle_api_extended import KaggleApi

api = KaggleApi()
api.authenticate()

api.kernels_output('marcogorelli/who-tests-what-in-pandas', 'output')

#url = 'https://drive.google.com/uc?id=16Y8SSNqMDGyIhedgF6BzASSXtKZIL89u'
#output = 'output/pandas-dev/.coverage'
#gdown.download(url, output)
