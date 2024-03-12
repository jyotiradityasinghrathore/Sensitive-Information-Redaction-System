import re
import pyap
import nltk
import spacy
from commonregex import CommonRegex
from snorkel.labeling import LabelingFunction
from spacy_download import load_spacy
import en_core_web_md

from warnings import filterwarnings
filterwarnings("ignore")

#Load Spacy Model
nlp = en_core_web_md.load()

def PhoneCensor(data):
    data1 = CommonRegex(data)
    list_phones = data1.phones

    for item in list_phones:
        data = data.replace(item,'\u2588'* len(item))

    return data, list_phones

def AddressCensor(data):
    List_Address = []
    All_Address = pyap.parse(data,country = 'US')

    for address in All_Address:
        S_Index = data.index(str(address).split(',')[0].strip())
        E_Index = data.index(str(address).split(',')[-1].strip()) + len(str(address).split(',')[-1].strip())
        List_Address.append(data[S_Index:E_Index])
        data = data[:S_Index] + '\u2588'* len(str(address)) + data[E_Index:]

    return data, List_Address

def DatesCensor(data):
    data1 = nlp(data)
    List_Dates_Ent = []

    for i in [ent.text.split('\n') for ent in data1.ents if ent.label_ == "DATE"]:
        for j in i:
            List_Dates_Ent.append(j)

    pattern = r'(\d{1,4}/\d{1,2}/\d{1,4})'
    List_Dates_Re = re.findall(pattern,data)
    List_Dates = set(List_Dates_Ent + List_Dates_Re)
    Excluded_List = [
    "Year's", "weeks", "Week's", "day", "Year", "month's", "month", 
    "Today", "yesterday", "Weeks", "century", "Year's", "today", 
    "week", "Month", "Day", "Tomorrow", "Week", "months", "year's", 
    "Months", "tomorrow", "Weeks", "week's", "Month's"
    ]
    for i in Excluded_List:
        if i in List_Dates:
            List_Dates.remove(i)
            
    for items in List_Dates:
        data = data.replace(items,'\u2588'* len(items))

    return data,List_Dates




# Snorker name censoring
def Entity_Extract(text):
    doc = nlp(text)
    Entity = [(ent.text, ent.label_) for ent in doc.ents]
    return Entity

def Title_Capital_Name(x):
    Title = ['Mrs.', 'Mr.', 'Dr.', 'Prof.']
    Word = x.split()
    for i, word in enumerate(Word[:-1]):
        if word in Title and Word[i + 1][0].isupper():
            return 1  
    return 0 

def refine_with_snorkel(sentences, extract_entities_fn, labeling_fn):
    Entity_Refined = []
    for sentence in sentences:
        Entity = extract_entities_fn(sentence)
        for entity in Entity:
            label = labeling_fn(entity[0])
            if label == 1 or entity[1] == 'PERSON':
                Entity_Refined.append(entity)
    return Entity_Refined

def Snorkel_Censor_Name(data):
    title_before_name_lf = LabelingFunction(
    name="title_before_capitalized_word",
    f=Title_Capital_Name
    )

    sentences = data.split('.')
    Entity_Refined = refine_with_snorkel(sentences, Entity_Extract, Title_Capital_Name)
    names_list = [entity[0] for entity in Entity_Refined]
    for item in names_list:
        data = data.replace(item, '\u2588'* len(item))
    return data, names_list
