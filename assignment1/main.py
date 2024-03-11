import nltk
from commonregex import CommonRegex
import pyap
import re
import spacy
from snorkel.labeling import LabelingFunction
from spacy_download import load_spacy
import en_core_web_md

from warnings import filterwarnings
filterwarnings("ignore")


# nlp = load_spacy("en_core_web_md", exclude=["parser", "tagger"])
nlp = en_core_web_md.load()
# nltk.download('wordnet', quiet=True)
# nltk.download('averaged_perceptron_tagger', quiet=True)
# nltk.download('maxent_ne_chunker', quiet=True)
# nltk.download('words', quiet=True)
# nltk.download('omw-1.4', quiet=True)
# nltk.download('punkt', quiet=True)

# def censor_names(data):
#     words = nltk.word_tokenize(data)
#     tag = nltk.pos_tag(words)
#     tree = nltk.ne_chunk(tag)
#     names_list = [ent[0][0] for ent in list(tree.subtrees()) if ent.label() in ['PERSON','GPE']]
#     list_to_exclude = ['mr', 'ms', 'mrs','miss','mister','missus','maiden','sir','madam','madame','master','mistress','lady','ladies','gentleman','gentlemen','Hi', "Hey"]
#     for i in list_to_exclude:
#         if i in names_list:
#             names_list.remove(i)

#     for item in names_list:
#         data = data.replace(item, '\u2588'* len(item))

#     return data, names_list

def censor_dates(data):
    data1 = nlp(data)
    dates_ent_list = []
    for i in [ent.text.split('\n') for ent in data1.ents if ent.label_ == "DATE"]:
        for j in i:
            dates_ent_list.append(j)
    pattern = r'(\d{1,4}/\d{1,2}/\d{1,4})'
    dates_re_list = re.findall(pattern,data)
    dates_list = set(dates_ent_list + dates_re_list)
    list_to_excluded = ["day", "tomorrow","yesterday","today","Day","Today","Tomorrow","century","weeks","week","Week","Weeks","week's","Week's","year", "Year","Year's","year's","month","Month","month's","Month's","months","Months"]
    for i in list_to_excluded:
        if i in dates_list:
            dates_list.remove(i)
    for items in dates_list:
        data = data.replace(items,'\u2588'* len(items))
    return data,dates_list
    
def censor_phones(data):
    data1 = CommonRegex(data)
    phones_list = data1.phones
    for item in phones_list:
        data = data.replace(item,'\u2588'* len(item))
    return data, phones_list

def censor_address(data):
    address_list = []
    addresses = pyap.parse(data,country = 'US')
    for address in addresses:
        start_index = data.index(str(address).split(',')[0].strip())
        end_index = data.index(str(address).split(',')[-1].strip()) + len(str(address).split(',')[-1].strip())
        address_list.append(data[start_index:end_index])
        data = data[:start_index] + '\u2588'* len(str(address)) + data[end_index:]
    return data, address_list




# --------------------------name censoring using snorkel--------------------------------
def extract_entities(text):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

def lf_title_before_capitalized_word(x):
    titles = ['Mr.', 'Mrs.', 'Dr.', 'Prof.']
    words = x.split()
    for i, word in enumerate(words[:-1]):  # Loop to the second-to-last word
        if word in titles and words[i + 1][0].isupper():
            return 1  # Potential name found
    return 0  # No potential name found

def refine_with_snorkel(sentences, extract_entities_fn, labeling_fn):
    refined_entities = []
    for sentence in sentences:
        entities = extract_entities_fn(sentence)
        for entity in entities:
            # Apply the labeling function to each entity; this is simplified
            label = labeling_fn(entity[0])
            if label == 1 or entity[1] == 'PERSON':
                refined_entities.append(entity)
    return refined_entities

def censor_names_snorkel(data):
    title_before_name_lf = LabelingFunction(
    name="title_before_capitalized_word",
    f=lf_title_before_capitalized_word
    )

    sentences = data.split('.')
    refined_entities = refine_with_snorkel(sentences, extract_entities, lf_title_before_capitalized_word)
    names_list = [entity[0] for entity in refined_entities]
    for item in names_list:
        data = data.replace(item, '\u2588'* len(item))
    return data, names_list
