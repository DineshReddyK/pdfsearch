import unittest
import os
from search import PDFSearch
from PyPDF2 import PdfWriter

class TestPDFSearch(unittest.TestCase):

    def setUp(self):
        self.pdf_search = PDFSearch()
        self.test_dir = 'test_pdfs'
        os.makedirs(self.test_dir, exist_ok=True)
        self.create_test_pdf('test1.pdf', 'This is a test PDF document.')
        self.create_test_pdf('test2.pdf', 'Another test PDF document with different content.')

    def tearDown(self):
        for file in os.listdir(self.test_dir):
            os.remove(os.path.join(self.test_dir, file))
        os.rmdir(self.test_dir)

    def create_test_pdf(self, filename, text):
        pdf_writer = PdfWriter()
        pdf_writer.add_blank_page(width=72, height=72)
        pdf_writer.add_text(text, 10, 10)
        with open(os.path.join(self.test_dir, filename), 'wb') as f:
            pdf_writer.write(f)

    def test_create_search_index(self):
        filenames = self.pdf_search.create_search_index(self.test_dir)
        self.assertIn('test1.pdf', filenames)
        self.assertIn('test2.pdf', filenames)
        self.assertEqual(len(filenames), 2)

    def test_search(self):
        self.pdf_search.create_search_index(self.test_dir)
        results = self.pdf_search.search('test PDF')
        self.assertIn('test1.pdf', results)
        self.assertIn('test2.pdf', results)

    def test_search_no_results(self):
        self.pdf_search.create_search_index(self.test_dir)
        results = self.pdf_search.search('nonexistent content')
        self.assertEqual(results, [])

    def test_read_pdf_error(self):
        with self.assertRaises(Exception):
            self.pdf_search._read_pdf('nonexistent.pdf')

    def test_clean_text(self):
        text = 'ThisIsATest123'
        cleaned_text = self.pdf_search._clean_text(text)
        self.assertEqual(cleaned_text, 'This Is A Test 123')

if __name__ == '__main__':
    unittest.main()