# -*- coding: utf-8 -*-
"""
@author: Alex Measure
"""
import os
import xml.etree.ElementTree as ET
from nltk import word_tokenize

DL_FRAMEWORKS = ['Theano', 'Tensorflow', 'Dynet', 'Chainer', 'Keras', 'Torch', 
                 'MxNet', 'CNTK', 'PyTorch', ('DL4J', 'Deeplearning4J', 'DeepLearning4Java')]
NLP_LIBRARIES = [('CoreNLP', 'StanfordCoreNLP'), 'NLTK', 'LingPipe', 'OpenNLP']
LANGUAGES = ['Python', 'Java', 'C++', 'Lua', 'Matlab', 'Octave', 'Perl']
# R copula package
ACL_DOI = r'https://doi.org/10.18653/'

def get_pages(infile):
    tree = ET.parse(infile)
    root = tree.getroot()
    head = root.getchildren()[0]
    title = head.getchildren()[-1]
    print(title.text)
    body = root.getchildren()[1]
    pages = body.getchildren()
    print('number of pages:', len(pages))
    return pages

def get_doi(infile):
    basename = os.path.basename(infile)
    prefix = basename[0:5]
    return os.path.join(ACL_DOI, prefix)
    
def get_paragraphs(page):
    return page.findall('{http://www.w3.org/1999/xhtml}p')    

def get_normalized_text(paragraph):
    text = paragraph.text
    if not text:
        text = ''
    return text

def is_first_page(paragraphs, conference_doi):
    texts = [get_normalized_text(paragraph) for paragraph in paragraphs]
    has_abstract = any([text == 'Abstract\n' for text in texts])
    has_introduction = any([text == '1 Introduction\n' for text in texts])
    if has_abstract or has_introduction:
        return True
    else:
        return False

def get_papers(pages, conference_doi):
    papers = []
    paper = []
    for page in pages:
        paragraphs = get_paragraphs(page)
        if is_first_page(paragraphs, conference_doi):
            papers.append(paper)
            paper = []
        for n, paragraph in enumerate(paragraphs):
            text = get_normalized_text(paragraph)
            # add the tokens to our current paper
            tokens = word_tokenize(text)
            paper += tokens
    # the end of the last paper won't be indicated but we still want to save it
    papers.append(paper)      
    print('papers retrieved:', len(papers))
    return papers

def get_paper_count(words, papers, match_case=False):
    count = 0
    for paper in papers:
        if isinstance(words, str):
            words = [words]
        if not match_case:
            paper_tokens = [token.lower() for token in paper]
            word_tokens = [word.lower() for word in words]
        if any([word_token in paper_tokens for word_token in word_tokens]):
            count += 1
    return count

def count_words(words, papers, match_case=False):
    for word in words:
        print(word, get_paper_count(word, papers, match_case))
        
def run(input_dir=r'C:\Users\Alex Measure\Desktop\ACL_analysis\extract'):
    files = [f for f in os.listdir(input_dir) if f.endswith('.xml')]
    for file in files:
        print('=' * 80)
        print('analyzing:', file)
        doi = get_doi(os.path.join(input_dir, file))
        print('doi:', doi)
        pages = get_pages(os.path.join(input_dir, file))
        papers = get_papers(pages, doi)
        for category in [DL_FRAMEWORKS, NLP_LIBRARIES, LANGUAGES]:
            print('*' * 80)
            count_words(category, papers)