"""
download pandas at the specified commit
"""

import subprocess

subprocess.run(
    ["git", "clone", "https://github.com/pandas-dev/pandas.git", "--depth", "50"],
    check=True,
)
