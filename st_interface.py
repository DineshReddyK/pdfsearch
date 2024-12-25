import time
from pathlib import Path
import streamlit as st
from search import PDFSearch

search_dir = Path(st.text_input(label='Enter the search directory',
                            placeholder="Absolute path to pdf files"))

if not search_dir.exists():
    st.write("Invalid path", search_dir)
    st.stop()

search_dir = str(search_dir)
if ('search_dir' not in st.session_state) or (st.session_state.search_dir != search_dir):
    start_time = time.time()
    pdf_indexer = PDFSearch()
    files_read = pdf_indexer.create_search_index(search_dir)
    end_time = time.time()
    time_taken = round(end_time - start_time, 2)
    st.caption('Took %.2f seconds to read %s PDF files'%(time_taken, len(files_read)))

    st.session_state.search_dir = search_dir
    st.session_state.files_read = files_read
    st.session_state.pdf_indexer = pdf_indexer

if 'files_read' in st.session_state and len(st.session_state.files_read) == 0:
    st.write('Found 0 PDF files')
    st.stop()
else:
    st.write('Found `%s` PDF files' % len(st.session_state.files_read))
    search_key = st.chat_input('Enter Search Keyword')
    if search_key:
        user = st.chat_message('user')
        user.write(search_key)
        search_result = st.session_state.pdf_indexer.search(search_key)

        ass = st.chat_message('assistant')
        if search_result:
            ass.write(f'Found `{search_key}` in the following document(s)')
            for res in search_result:
                ass.write(res)
        else:
            ass.write(f'Couldnt find any documents matching `{search_key}`')
