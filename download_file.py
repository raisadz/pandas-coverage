#import gdown 

#url = 'https://drive.google.com/uc?id=1RqLvO0NA5yutlXreo8MdoewQdyVGi77h'
#output = 'output/pandas-dev/.coverage'
#gdown.download(url, output)

import subprocess

subprocess.run(['kaggle', 'kernels', 'output', 'marcogorelli/who-tests-what-in-pandas', '-p', 'output'])
