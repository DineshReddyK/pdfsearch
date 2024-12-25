import numpy as np
import os, re, io
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class PDFSearch:
    def __init__(self):
        self.vectorizer = None
        self.tfidf_matrix = []
        self.filenames = []

    def _clean_text(self, text):
        text = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', text) #insert space b/w lowercase and upper case
        text = re.sub(r'(?<=[a-zA-Z])(?=\d)', ' ', text) #insert space b/w letters and digits
        text = re.sub(r'(?<=\d)(?=[a-zA-Z])', ' ', text) #insert space b/w digits and letters
        return text

    def _read_pdf(self, file_path):
        with open(file_path, 'rb') as file:
            pdf = PdfReader(io.BytesIO(file.read()))
            text = ' '.join(page.extract_text() for page in pdf.pages)
        return self._clean_text(text)

    def create_search_index(self, search_dir):
        documents = []
        pdf_files = [f for f in os.listdir(search_dir) if f.endswith('.pdf')]
        print(f'Found {pdf_files} in {search_dir}')

        for filename in pdf_files:
            try:
                document = self._read_pdf(os.path.join(search_dir, filename))
                documents.append(document)
                self.filenames.append(filename)
            except Exception as e:
                print(f'Error occured: {e}')

        if documents:
            self.vectorizer = TfidfVectorizer()
            self.tfidf_matrix = self.vectorizer.fit_transform(documents)

        return self.filenames

    def search(self, query):
        query_tfidf = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_tfidf, self.tfidf_matrix).flatten()

        #get indices of documents sorted by similarity
        sorted_indices = np.argsort(similarities)[::-1]

        #filterout indicies where similarity is zero
        filtered_indices = sorted_indices[similarities[sorted_indices] > 0]

        #return filenames sorted by similarity
        return [self.filenames[i] for i in filtered_indices]
