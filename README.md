# Who tests what in pandas?

Ever wondered which tests executed a given line of code? Enter the filename and line number in this [app](https://pandas-coverage.herokuapp.com/) to find out!

## Installation

If you want to run the app locally follow the steps below.

Install anaconda or miniconda https://docs.conda.io/en/latest/miniconda.html.

Clone the repository:
```bash
git clone git@github.com:raisadz/pandas-coverage.git pandas-coverage
cd pandas-coverage
```

Create a conda environment:

```bash
conda create -n pandas-coverage python=3.10
```

Activate the environment:

```bash
conda activate pandas-coverage
```

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the requirements:
```bash
pip install -r requirements.txt
```

Go to Kaggle, and generate a .kaggle.json file, save locally see [here](https://github.com/Kaggle/kaggle-api#api-credentials) for how to do that.

Run the following line to download coverage.db and metadata.txt from kaggle:
```bash
kaggle kernels output marcogorelli/who-tests-what-in-pandas -p .
```

Run the app with 
```bash
python clone_pandas.py && streamlit run main.py
```

