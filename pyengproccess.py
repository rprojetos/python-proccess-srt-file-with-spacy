from sys import stdin, stdout
import subprocess
import spacy
import re

regex_pattern = re.compile(r'^\d{1,2}:\d{1,2}(:\d{1,2})?$')

def extract_times_from_sentences(lst_sentence):
    regex_pattern = re.compile(r'\b(\d{1,2}:\d{1,2}(:\d{1,2})?)\b')
    concatenated_text = ' '.join(lst_sentence)
    matches = regex_pattern.findall(concatenated_text)
    time_values = [match[0] for match in matches]
    return time_values


def lst_filter_sentence(lst_str):
    regex_pattern = re.compile(r'\b(\d{1,2}:\d{1,2}(:\d{1,2})?)\b')
    str_sentence = ""
    separator = ""
    str_time = ""
    for sentence in lst_str:
        if regex_pattern.match(sentence):
            if str_time == "":
                str_time = sentence
        else:
            str_sentence += f"{separator}{sentence}"
            separator = " "
    return str_time, str_sentence


def get_content_file(path_file):
    with open(path_file, 'r') as f:
        content_file = f.read()
    return content_file


def split_into_sentences(text):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    sentences = [sent.text.strip() for sent in doc.sents]
    return sentences


def make_sentences_time(tpl_sentence):
    str_time = ''
    str_sentence = ''
    lst_time_sentence = []
    for tpl in tpl_sentence:  
        if tpl[0] != '':
            if str_time != "":
                lst_time_sentence.append([str_time, str_sentence,tpl[0]])
                str_time = ""
                str_sentence = ""
            str_time = tpl[0]
            str_sentence = tpl[1]
        else:
            str_sentence += f' {tpl[1]}'
    lst_time_sentence.append([str_time, str_sentence,''])
    return lst_time_sentence


def extract_times_from_sentences(lst_sentence):
    i = 0
    str_sentence = ""
    lst_tpl = []
    for sentence in lst_sentence:
        lst_str = sentence.split('\n')
        lst_tpl.append(lst_filter_sentence(lst_str))
    return lst_tpl


def proccess_time_sentences(path_file_srt):
    str_content = get_content_file('transcription.srt')
    lst_sentence = split_into_sentences(str_content)
    list_time_sentences = extract_times_from_sentences(lst_sentence)
    return make_sentences_time(list_time_sentences)


if __name__ == '__main__':
    for lst_time_sentence in proccess_time_sentences('transcription.srt'):
        print(lst_time_sentence)
        print('\n------------\n')