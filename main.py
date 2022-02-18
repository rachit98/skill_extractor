from pdfminer.high_level import extract_text
import nltk
import string
import random
import pandas as pd

# Correspond to question tags field
# need not be manually coded can be inputed from inventory.csv
TECH_SKILLS_DB = [
    'java',
    'c',
    'javascript',
    'machinelearning',
    'linux',
    'mongodb',
    'python',
    'oops',
    'unix'
]

# Corresponding to questions for HR round 
SOFT_SKILLS_DB = [
    'honesty',
    'integrity',
    'respect',
    'managment',
    'leardership',
    'timemanagement',
    'adaptability',
    'discipline'
]

# downloading word dictionaries, will be useful when word2vec is implemented
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('maxent_ne_chunker', quiet=True)
nltk.download('words', quiet=True)

def extract_text_from_pdf(pdf_path):
    return extract_text(pdf_path)

def extract_tech_skills(input_text):
    
    # tokenizing the text
    stop_words = set(nltk.corpus.stopwords.words('english'))
    word_tokens = nltk.tokenize.word_tokenize(input_text)

    # removing the stop words
    filtered_tokens = [w for w in word_tokens if w not in stop_words]

    # remove punctuations (Need to check this one)
    # filtered_tokens = [w for w in word_tokens if w.isalpha()]
    filtered_tokens = str.maketrans(string.punctuation, ' '*len(string.punctuation))
    filtered_tokens = [w for w in word_tokens if w.isalpha()]
    

    # Generating bigrams (Machine Learning --> MachineLearning)
    bigrams_trigrams = list(map(' '.join, nltk.everygrams(filtered_tokens, 2, 3)))

    store_skills = set() #Returning a set, can be converted into list/JSON/P-Queue/other

    for token in filtered_tokens:
        if token.lower() in TECH_SKILLS_DB:
            store_skills.add(token.lower())
    
    for ngram in bigrams_trigrams:
        if ngram.lower() in TECH_SKILLS_DB:
            store_skills.add(token.lower())
    
    return store_skills


def get_questions_for_round_1(skill_list):
    question_bank = pd.read_csv('./inventory.csv')

    question_bank = question_bank.loc[question_bank['tag'].isin(skill_list)]
    question_bank = question_bank.loc[question_bank['difficulty'].isin(['easy','med'])]

    return question_bank['question']

def get_questions_for_round_2(skill_list):
    question_bank = pd.read_csv('./inventory.csv')

    question_bank = question_bank.loc[question_bank['tag'].isin(skill_list)]
    question_bank = question_bank.loc[question_bank['difficulty'].isin(['med','hard'])]

    return question_bank['question']


if __name__=='__main__':
    text = extract_text_from_pdf('./JD/MS_JD.pdf') # Can be autoupdated based on Candidate id/ Job id
    skill_list = list(extract_tech_skills(text))
    print('Tech Skills : ',skill_list)
    print()
    print('-----------------------------------------------------------')
    skill_list.append('datastructures')
    questions_list = list(get_questions_for_round_1(skill_list))
    print("All Questions for Round 1: ",questions_list)
    print("Recommended Questions for Round 1: ",random.sample(questions_list, 3))
    print()
    print('-----------------------------------------------------------')
    skill_list.remove('datastructures')
    skill_list.append('systemdesign')
    questions_list = list(get_questions_for_round_2(skill_list))
    print("All Questions for Round 2: ",questions_list)
    print("Recommended Questions for Round 2: ",random.sample(questions_list, 3))
    print()
    print('-----------------------------------------------------------')


