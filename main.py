import streamlit as st
import os
import sqlite3
import re
import subprocess

output_files = os.listdir(os.getcwd())
pattern_commit = re.compile(r'coverage_(.+?)\.db')
#coverage_db = [i for i in output_files if pattern_commit.search(i)][0]
pandas_commit = [pattern_commit.search(i).group(1) for i in output_files if pattern_commit.search(i)][0]
#breakpoint()
#database = f'output/{coverage_db}'

#database = 'output/pandas-dev/.coverage'

database = [i for i in output_files if pattern_commit.search(i)][0]

conn = sqlite3.connect(database)
c = conn.cursor()

def fixup_path(file):
    return f'/kaggle/working/pandas-dev/{file}'

def unfixup_path(file):
    return file.replace('/kaggle/working/pandas-dev/', '')

def pandas_path(file):
        return f'pandas/{file}'

def convert_context_to_test(context):
    n = None
    pieces = context.split('.')
    for n in range(len(pieces)):
        path = os.path.join('pandas', *pieces[:n]) + '.py'
        if os.path.exists(path):
            test = '::'.join([path[len('pandas/'):], *pieces[n:]])
            break
    else:
        # Couldn't reconstruct test name
        # Shouldn't really happen, this is just to not break the app
        return context

    return test

filenames_query = (
        """
        select distinct file.path
        from file
        where file.path not like '%tests%'
        and file.path not like '%__init__%'
        and file.path not like '%conftest%'
        and file.path not like '%testing%'
        and file.path not like '%.pxi'
        and file.path not like '%.pxd'
        """
)

c.execute(filenames_query)
filenames = c.fetchall()
filenames = sorted(unfixup_path(i[0]) for i in filenames)

sidebar = st.sidebar
sidebar.title('Who tests what in pandas?')
sidebar.header(
    'Ever wondered which tests executed a given line of code? '
    'Enter the filename and line number below to find out!'
)


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

code = open(pandas_path(file), 'r').read()

lines = code.split('\n')

st.text('Content of selected file:')
markdown = ""
for i, line in enumerate(lines):
    markdown += f"{i+1}: {line}\n"
st.code(markdown, language=None)

selected_line = sidebar.selectbox("Select a line:", options=linenos)

if selected_line is not None:
	sidebar.markdown(
		"You selected line: \n"
		"\n"
		"```\n"
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
	sidebar.markdown('The following tests executed it:\n')
	sidebar.table({'test name': [convert_context_to_test(i[0]) for i in c.fetchall()]})

#sidebar.markdown("INFO: using commit f4136c0415, from Sat Jan 7 18:57:42")
sidebar.markdown(f"INFO: using commit {pandas_commit}")


date_output = subprocess.run(['git', 'log', '-n', '1', "--format='%cd'"], cwd='pandas', capture_output=True, text=True)
sidebar.markdown(f"Last updated {date_output.stdout}")