import streamlit as st
from io import StringIO
from pprint import pprint
import sqlite3
from coverage.numbits import register_sqlite_functions
import os

import argparse
import pathlib

@st.cache
def _upload_file():
    uploaded_file = st.file_uploader("Choose a file")
    return uploaded_file

uploaded_file = _upload_file()
if uploaded_file is not None:

    commit = uploaded_file.name.split('_')[1].split('.')[0]

    bytes_data = uploaded_file.getvalue()
    with open('.coverage', 'wb') as fd:
        fd.write(bytes_data)
    database = '.coverage'

    st.text(f'Using commit: {commit}')

    conn = sqlite3.connect(database)
    register_sqlite_functions(conn)
    c = conn.cursor()

    def fixup_path(file):
        return f'/kaggle/working/pandas-dev/{file}'

    def unfixup_path(file):
        return file.replace('/kaggle/working/pandas-dev/', '')

    filenames_query = (
            """
            select distinct file.path
            from file
            """
    )

    c.execute(filenames_query)
    filenames = c.fetchall()
    filenames = sorted(unfixup_path(i[0]) for i in filenames)

    file = st.selectbox('filename', filenames)

    linenos_query = (
            """
            select distinct arc.tono
            from file, arc, context
            where arc.file_id = file.id
            and arc.context_id = context.id
            and file.path = ?
            and arc.tono > 0
            and context.context != ''
            """
    )

    c.execute(linenos_query, (fixup_path(file),))
    linenos = c.fetchall()
    linenos = sorted(lineno[0] for lineno in linenos)

    lineno = st.selectbox('line number', linenos)

    QUERY = (
            """
            select context.context
            from arc, context, file
            where arc.context_id = context.id
            and arc.file_id = file.id
            and arc.tono = ?
            and file.path = ?
            and context.context != ''
            """
    )

    c.execute(QUERY, (lineno, fixup_path(file)))
    st.table({'test name': [i[0] for i in c.fetchall()]})

