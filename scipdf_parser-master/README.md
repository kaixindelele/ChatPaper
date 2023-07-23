# SciPDF Parser

A Python parser for scientific PDF based on [GROBID](https://github.com/kermitt2/grobid).

## Installation

Use `pip` to install from this Github repository

```bash
pip install git+https://github.com/titipata/scipdf_parser
```

**Note**
* We also need an `en_core_web_sm` model for spacy, where you can run `python -m spacy download en_core_web_sm` to download it
* You can change GROBID version in `serve_grobid.sh` to test the parser on a new GROBID version

## Usage

Run the GROBID using the given bash script before parsing PDF

```bash
bash serve_grobid.sh
```

This script will download GROBID and run the service at default port 8070 (see more [here](https://grobid.readthedocs.io/en/latest/Grobid-service/)).
To parse a PDF provided in `example_data` folder or direct URL, use the following function:

```python
import scipdf
article_dict = scipdf.parse_pdf_to_dict('example_data/futoma2017improved.pdf') # return dictionary
 
# option to parse directly from URL to PDF, if as_list is set to True, output 'text' of parsed section will be in a list of paragraphs instead
article_dict = scipdf.parse_pdf_to_dict('https://www.biorxiv.org/content/biorxiv/early/2018/11/20/463760.full.pdf', as_list=False)

# output example
>> {
    'title': 'Proceedings of Machine Learning for Healthcare',
    'abstract': '...',
    'sections': [
        {'heading': '...', 'text': '...'},
        {'heading': '...', 'text': '...'},
        ...
    ],
    'references': [
        {'title': '...', 'year': '...', 'journal': '...', 'author': '...'},
        ...
    ],
    'figures': [
        {'figure_label': '...', 'figure_type': '...', 'figure_id': '...', 'figure_caption': '...', 'figure_data': '...'},
        ...
    ],
    'doi': '...'
}

xml = scipdf.parse_pdf('example_data/futoma2017improved.pdf', soup=True) # option to parse full XML from GROBID
```

To parse figures from PDF using [pdffigures2](https://github.com/allenai/pdffigures2), you can run

```python
scipdf.parse_figures('example_data', output_folder='figures') # folder should contain only PDF files
```

You can see example output figures in `figures` folder.
