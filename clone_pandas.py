import re
import subprocess
import os

output_files = os.listdir(os.getcwd())
pattern_commit = re.compile(r'coverage_(.+?)\.db')
pandas_commit = [pattern_commit.search(i).group(1) for i in output_files if pattern_commit.search(i)][0]

subprocess.run(['git', 'clone', 'https://github.com/pandas-dev/pandas.git'])
subprocess.run(['git', 'clone', 'https://github.com/pandas-dev/pandas.git', '--depth', 10])
subprocess.run(['git', 'checkout', pandas_commit], cwd='pandas')