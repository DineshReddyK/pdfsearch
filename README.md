# PDF Search Utility
PDF Search Utility is a simple tool designed to facilitate faster search across a directory of PDF files. The tool provides an easy-to-use GUI where users can input a directory. The utility then reads and indexes all PDF files in that directory. Users can enter a search query, and the tool will list the file names containing the search string.

*Note*: For better performance, you can use `PyMuPDF` or `fitz`. Due to license limitations this tool currently uses `PyPDF2`.

### Installation
To install and run the PDF Search Utility, follow these steps:

Clone the repository:

```bash
git clone https://github.com/DineshReddyK/pdfsearch.git
cd pdfsearch
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Usage
Import the package and use the `PDFSearch` class in your module to use it.\
Or\
To launch the UI, run
```bash
streamlit run st_interface.py
```

### Contributing
Contributions are welcome! If you have any suggestions or improvements, please submit a pull request or open an issue.

