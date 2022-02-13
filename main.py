from pdfminer.high_level import extract_text
import nltk


TECH_SKILLS_DB = [
    'java',
    'c++',
    'javascript',
    'machinelearning',
    'linux',
    'mongodb',
    'python'
]

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

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

def extract_text_from_pdf(pdf_path):
    return extract_text(pdf_path)

def extract_tech_skills(input_text):
    
    # tokenizing the text
    stop_words = set(nltk.corpus.stopwords.words('english'))
    word_tokens = nltk.tokenize.word_tokenize(input_text)

    # removing the stop words
    filtered_tokens = [w for w in word_tokens if w not in stop_words]

    # remove punctuations
    filtered_tokens = [w for w in word_tokens if w.isalpha()]

    # Generating bigrams (Machine Learning --> MachineLearning)
    bigrams_trigrams = list(map(' '.join, nltk.everygrams(filtered_tokens, 2, 3)))

    store_skills = set()

    for token in filtered_tokens:
        if token.lower() in TECH_SKILLS_DB:
            store_skills.add(token)
    
    for ngram in bigrams_trigrams:
        if ngram.lower() in TECH_SKILLS_DB:
            store_skills.add(token)
    
    return store_skills


if __name__=='__main__':
    text = extract_text_from_pdf('./resumes/rachit.pdf')
    print('Soft Skills : ',extract_tech_skills(text))