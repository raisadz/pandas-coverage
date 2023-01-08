import streamlit as st
from io import StringIO
from pprint import pprint
import sqlite3
from coverage.numbits import register_sqlite_functions
import os
import re

import argparse
import pathlib

import numpy as np
import streamlit_scrollable_textbox as stx
import pandas as pd

from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode


database = 'output/pandas-dev/.coverage'

conn = sqlite3.connect(database)
register_sqlite_functions(conn)
c = conn.cursor()

def fixup_path(file):
    return f'/kaggle/working/pandas-dev/{file}'

def unfixup_path(file):
    return file.replace('/kaggle/working/pandas-dev/', '')

def pandas_path(file):
        return f'pandas/{file}'

filenames_query = (
        """
        select distinct file.path
        from file
        """
)

c.execute(filenames_query)
filenames = c.fetchall()
filenames = sorted(unfixup_path(i[0]) for i in filenames)
filenames = [i for i in filenames if '__init__' not in i]
regex = r'test_|\.pxi$'
filenames = [i for i in filenames if not re.search(regex, i)]

sidebar = st.sidebar

sidebar.markdown("Select the filename and the line number for which you would like to see all the executed tests")

sidebar.markdown("Using commit: a28cadbeb6f21da6c768b84473b3415e6efb3115")

file = sidebar.selectbox('filename', filenames)


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

#lineno = st.selectbox('line number', linenos)


#file_lines = open(pandas_path(file), 'r').readlines()
code = open(pandas_path(file), 'r').read()

lines = code.split('\n')

markdown = ""
for i, line in enumerate(lines):
    markdown += f"{i+1}: {line}\n"
st.code(markdown)
#stx.scrollableTextbox(markdown, height=800)

#selected_line = st.selectbox("Select a line:", options=lines)
#st.write(selected_line)

selected_line = sidebar.selectbox("Select a line:", options=linenos)

#selected_line = st.selectbox("Select a line:", options=np.arange(1, len(lines)+1))
if selected_line is not None:
	sidebar.markdown(
		"You selected line: \n"
		"\n"
		"```python\n"
		f"{lines[selected_line-1]}\n"
		"```"
		"\n")


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

	c.execute(QUERY, (selected_line, fixup_path(file)))
	#sidebar.markdown( c.fetchall())
	sidebar.markdown('The following tests executed it:\n')
	sidebar.table({'test name': [i[0] for i in c.fetchall()]})

