"""
This is the main function that creates a streamlit app on Heroku
"""

import os
import sqlite3
import subprocess

import streamlit as st

# output_files = os.listdir(os.getcwd())
with open("metadata.txt", "r", encoding="utf-8") as fl:
    pandas_commit = fl.read().split("\n")[0]
DATABASE = "coverage.db"

conn = sqlite3.connect(DATABASE)
c = conn.cursor()


def fixup_path(file):
    """
    make a kaggle path
    """
    return f"/kaggle/working/pandas-dev/{file}"


def unfixup_path(file):
    """
    remove a kaggle path
    """
    return file.replace("/kaggle/working/pandas-dev/", "")


def pandas_path(file):
    """
    add a pandas path
    """
    return f"pandas/{file}"


def convert_context_to_test(context):
    """
    change the test names so that they can be run by pytest
    """
    n_range = None
    pieces = context.split(".")
    for n_range in range(len(pieces)):
        path = os.path.join("pandas", *pieces[:n_range]) + ".py"
        if os.path.exists(path):
            test = "::".join([path[len("pandas/") :], *pieces[n_range:]])
            break
    else:
        # Couldn't reconstruct test name
        # Shouldn't really happen, this is just to not break the app
        return context

    return test


@st.cache
def get_filenames():
    """
    get the tests for the selected file and line
    """
    filenames_query = """
        select distinct file.path
        from arc, context, file
        where arc.context_id = context.id
        and arc.file_id = file.id
        and context.context != ''
        and file.path not like '%tests%'
        and file.path not like '%__init__%'
        and file.path not like '%conftest%'
        and file.path not like '%testing%'
        and file.path not like '%.pxi'
        and file.path not like '%.pxd'
        """
    c.execute(filenames_query)
    filenames = c.fetchall()
    filenames = sorted(unfixup_path(i[0]) for i in filenames)
    return filenames


test_filenames = get_filenames()

sidebar = st.sidebar
sidebar.title("Who tests what in pandas?")
sidebar.header(
    "Ever wondered which tests executed a given line of code? "
    "Enter the filename and line number below to find out!"
)


selected_file = sidebar.selectbox("filename", test_filenames)


LINENOS_QUERY = """
       select distinct arc.tono
       from file, arc, context
       where arc.file_id = file.id
       and arc.context_id = context.id
       and file.path = ?
       and arc.tono > 0
       and context.context != ''
       """

c.execute(LINENOS_QUERY, (fixup_path(selected_file),))
linenos = c.fetchall()
linenos = sorted(lineno[0] for lineno in linenos)

with open(pandas_path(selected_file), "r", encoding="utf-8") as pandas_fl:
    code = pandas_fl.read()

lines = code.split("\n")

st.text("Content of selected file:")
CONTENT = ""
for i, line in enumerate(lines):
    CONTENT += f"{i+1}: {line}\n"
st.code(CONTENT, language=None)

selected_line = sidebar.selectbox("Select a line:", options=linenos)

if selected_line is not None:
    sidebar.markdown(
        "You selected line: \n" "\n" "```\n" f"{lines[selected_line-1]}\n" "```" "\n"
    )

    QUERY = """
            select distinct context.context
            from arc, context, file
            where arc.context_id = context.id
            and arc.file_id = file.id
            and arc.tono = ?
            and file.path = ?
            and context.context != ''
            order by context.context
            """

    c.execute(QUERY, (selected_line, fixup_path(selected_file)))
    sidebar.markdown("The following tests executed it:\n")
    sidebar.table({"test name": [convert_context_to_test(i[0]) for i in c.fetchall()]})

sidebar.markdown(f"INFO: using commit {pandas_commit}")


date_output = subprocess.run(
    ["git", "log", "-n", "1", "--format='%cd'"],
    cwd="pandas",
    capture_output=True,
    text=True,
    check=True,
)
sidebar.markdown(f"Last updated {date_output.stdout}")
