"""
download pandas at the specified commit
"""

import subprocess

with open("metadata.txt", "r", encoding="utf-8") as fl:
    pandas_commit = fl.read().split("\n")[0]

subprocess.run(
    ["git", "clone", "https://github.com/pandas-dev/pandas.git", "--depth", "10"],
    check=True,
)
subprocess.run(["git", "checkout", pandas_commit], cwd="pandas", check=True)
