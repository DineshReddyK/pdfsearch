import time
import numpy as np
import streamlit as st
import os, re, io, pickle
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def dir_selector(path='/tmp/'):
    filenames = os.listdir(path)
    dirnames = [f for f in filenames if os.path.isdir(os.path.join(path,f))]
    selected_dir = st.selectbox('Select a directory', dirnames)
    return os.path.join(path, selected_dir)

def read_pdf(file_path):
    with open(file_path, 'rb') as file:
        print(f'reading .. {file_path}')
        pdf = PdfReader(io.BytesIO(file.read()))
        text = ' '.join(page.extract_text() for page in pdf.pages)
        text = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', text) #insert space b/w lowercase and upper case
        text = re.sub(r'(?<=[a-zA-Z])(?=\d)', ' ', text) #insert space b/w letters and digits
        text = re.sub(r'(?<=\d)(?=[a-zA-Z])', ' ', text) #insert space b/w digits and letters
        print('returning text')
    return text

def create_tfidf_matrix(path):
    documents, tfidf_matrix, filenames = [], [], []
    vectorizer = None
    pdf_files = [f for f in os.listdir(path) if f.endswith('.pdf')]
    print(f'Found {pdf_files} in {path}')
    total_files = len(pdf_files)
    text_display = "Reading PDF files..."
    progress_bar = st.progress(0, text_display)

    for i, filename in enumerate(pdf_files):
        try:
            document = read_pdf(os.path.join(path, filename))
            documents.append(document)
            filenames.append(filename)
        except Exception as e:
            print(f'Error occured: {e}')
        progress_bar.progress((i+1)/total_files, text_display)

    progress_bar.empty()
    if documents:
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(documents)

    return vectorizer, tfidf_matrix, filenames

def search(vectorizer, tfidf_matrix, filenames, query):
    query_tfidf = vectorizer.transform([query])
    similarities = cosine_similarity(query_tfidf, tfidf_matrix).flatten()

    #get indices of documents sorted by similarity
    sorted_indices = np.argsort(similarities)[::-1]

    #filterout indicies where similarity is zero
    filtered_indices = sorted_indices[similarities[sorted_indices] > 0]

    #return filenames sorted by similarity
    return [filenames[i] for i in filtered_indices]

user_dirname = dir_selector()

if ('user_dirname' not in st.session_state) or (st.session_state.user_dirname != user_dirname):
    st.session_state.user_dirname = user_dirname
    start_time = time.time()
    vectorizer, tfidf_matrix, filenames = create_tfidf_matrix(user_dirname)
    end_time = time.time()
    time_taken = round(end_time - start_time, 2)
    st.caption('Took %.2f seconds to read %s PDF files'%(time_taken, len(filenames)))
    st.session_state.vectorizer = vectorizer
    st.session_state.tfidf_matrix = tfidf_matrix
    st.session_state.filenames = filenames

if 'filenames' in st.session_state and len(st.session_state.filenames) == 0:
    st.write('Found 0 PDF files')
    st.stop()
else:
    st.write('Found `%s` PDF files' % len(st.session_state.filenames))
    search_key = st.chat_input('Enter Search Keyword')
    if search_key:
        user = st.chat_message('user')
        user.write(search_key)
        search_result = search(st.session_state.vectorizer,
                               st.session_state.tfidf_matrix,
                               st.session_state.filenames,
                               search_key,
        )

        ass = st.chat_message('assistant')
        if search_result:
            ass.write(f'Found `{search_key}` in the following document(s)')
            for res in search_result:
                ass.write(res)
        else:
            ass.write(f'Couldnt find any documents matching `{search_key}`')
