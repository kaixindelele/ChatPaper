import numpy as np
import pandas as pd
import textstat
import spacy
from collections import Counter
from itertools import groupby


nlp = spacy.load("en_core_web_sm")

PRESENT_TENSE_VERB_LIST = ["VB", "VBP", "VBZ", "VBG"]
VERB_LIST = ["VB", "VBP", "VBZ", "VBG", "VBN", "VBD"]
NOUN_LIST = ["NNP", "NNPS"]


SECTIONS_MAPS = {
    "Authors": "Authors",
    "AUTHORS": "AUTHORS",
    "Abstract": "Abstract",
    "ABSTRACT": "Abstract",
    "Date": "Date",
    "DATE": "DATE",
    "INTRODUCTION": "Introduction",
    "MATERIALS AND METHODS": "Methods",
    "Materials and methods": "Methods",
    "METHODS": "Methods",
    "RESULTS": "Results",
    "CONCLUSIONS": "Conclusions",
    "CONCLUSIONS AND FUTURE APPLICATIONS": "Conclusions",
    "DISCUSSION": "Discussion",
    "ACKNOWLEDGMENTS": "Acknowledgement",
    "TABLES": "Tables",
    "Tabnles": "Tables",
    "DISCLOSURE": "Disclosure",
    "CONFLICT OF INTEREST": "Disclosure",
    "Acknowledgement": "Acknowledgements",
}


def compute_readability_stats(text):
    """
    Compute reading statistics of the given text
    Reference: https://github.com/shivam5992/textstat

    Parameters
    ==========
    text: str, input section or abstract text
    """
    try:
        readability_dict = {
            "flesch_reading_ease": textstat.flesch_reading_ease(text),
            "smog": textstat.smog_index(text),
            "flesch_kincaid_grade": textstat.flesch_kincaid_grade(text),
            "coleman_liau_index": textstat.coleman_liau_index(text),
            "automated_readability_index": textstat.automated_readability_index(text),
            "dale_chall": textstat.dale_chall_readability_score(text),
            "difficult_words": textstat.difficult_words(text),
            "linsear_write": textstat.linsear_write_formula(text),
            "gunning_fog": textstat.gunning_fog(text),
            "text_standard": textstat.text_standard(text),
            "n_syllable": textstat.syllable_count(text),
            "avg_letter_per_word": textstat.avg_letter_per_word(text),
            "avg_sentence_length": textstat.avg_sentence_length(text),
        }
    except:
        readability_dict = {
            "flesch_reading_ease": None,
            "smog": None,
            "flesch_kincaid_grade": None,
            "coleman_liau_index": None,
            "automated_readability_index": None,
            "dale_chall": None,
            "difficult_words": None,
            "linsear_write": None,
            "gunning_fog": None,
            "text_standard": None,
            "n_syllable": None,
            "avg_letter_per_word": None,
            "avg_sentence_length": None,
        }
    return readability_dict


def compute_text_stats(text):
    """
    Compute part of speech features from a given spacy wrapper of text

    Parameters
    ==========
    text: spacy.tokens.doc.Doc, spacy wrapper of the section or abstract text

    Output
    ======
    text_stat: dict, part of speech and text features extracted from the given text
    """
    try:
        pos = dict(Counter([token.pos_ for token in text]))
        pos_tag = dict(
            Counter([token.tag_ for token in text])
        )  # detailed part-of-speech

        n_present_verb = sum(
            [v for k, v in pos_tag.items() if k in PRESENT_TENSE_VERB_LIST]
        )
        n_verb = sum([v for k, v in pos_tag.items() if k in VERB_LIST])

        word_shape = dict(Counter([token.shape_ for token in text]))  # word shape
        n_word_per_sents = [len([token for token in sent]) for sent in text.sents]
        n_digits = sum([token.is_digit or token.like_num for token in text])
        n_word = sum(n_word_per_sents)
        n_sents = len(n_word_per_sents)
        text_stats_dict = {
            "pos": pos,
            "pos_tag": pos_tag,
            "word_shape": word_shape,
            "n_word": n_word,
            "n_sents": n_sents,
            "n_present_verb": n_present_verb,
            "n_verb": n_verb,
            "n_digits": n_digits,
            "percent_digits": n_digits / n_word,
            "n_word_per_sents": n_word_per_sents,
            "avg_word_per_sents": np.mean(n_word_per_sents),
        }
    except:
        text_stats_dict = {
            "pos": None,
            "pos_tag": None,
            "word_shape": None,
            "n_word": None,
            "n_sents": None,
            "n_present_verb": None,
            "n_verb": None,
            "n_digits": None,
            "percent_digits": None,
            "n_word_per_sents": None,
            "avg_word_per_sents": None,
        }
    return text_stats_dict


def compute_journal_features(article):
    """
    Parse features about journal references from a given dictionary of parsed article e.g.
    number of reference made, number of unique journal refered, minimum year of references,
    maximum year of references, ...

    Parameters
    ==========
    article: dict, article dictionary parsed from GROBID and converted to dictionary
        see ``pdf/parse_pdf.py`` for the detail of the output dictionary

    Output
    ======
    reference_dict: dict, dictionary of
    """
    try:
        n_reference = len(article["references"])
        n_unique_journals = len(
            pd.unique([a["journal"] for a in article["references"]])
        )
        reference_years = []
        for reference in article["references"]:
            year = reference["year"]
            if year.isdigit():
                # filter outliers
                if int(year) in range(1800, 2100):
                    reference_years.append(int(year))
        avg_ref_year = np.mean(reference_years)
        median_ref_year = np.median(reference_years)
        min_ref_year = np.min(reference_years)
        max_ref_year = np.max(reference_years)
        journal_features_dict = {
            "n_reference": n_reference,
            "n_unique_journals": n_unique_journals,
            "avg_ref_year": avg_ref_year,
            "median_ref_year": median_ref_year,
            "min_ref_year": min_ref_year,
            "max_ref_year": max_ref_year,
        }
    except:
        journal_features_dict = {
            "n_reference": None,
            "n_unique_journals": None,
            "avg_ref_year": None,
            "median_ref_year": None,
            "min_ref_year": None,
            "max_ref_year": None,
        }
    return journal_features_dict


def merge_section_list(section_list, section_maps=SECTIONS_MAPS, section_start=""):
    """
    Merge a list of sections into a normalized list of sections,
    you can get the list of sections from parsed article JSON in ``parse_pdf.py`` e.g.

    >> section_list = [s['heading'] for s in article_json['sections']]
    >> section_list_merged = merge_section_list(section_list)

    Parameters
    ==========
    section_list: list, list of sections

    Output
    ======
    section_list_merged: list,  sections
    """
    sect_map = section_start  # text for starting section e.g. ``Introduction``
    section_list_merged = []
    for section in section_list:
        if any([(s.lower() in section.lower()) for s in section_maps.keys()]):
            sect = [s for s in section_maps.keys() if s.lower() in section.lower()][0]
            sect_map = section_maps.get(sect, "")  #
            section_list_merged.append(sect_map)
        else:
            section_list_merged.append(sect_map)
    return section_list_merged
