from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

import string

import pandas as pd


df = pd.read_csv('Womens Clothing Reviews.csv')

df.drop_duplicates(inplace=True)

df.dropna(inplace=True)

df.drop(columns=['Clothing ID', 'Age', 'Recommended IND',
                 'Positive Feedback Count', 'Division Name',
                 'Department Name', 'Class Name'])

for data in df.index:
    if df.loc[data, 'Rating'] == 3:
        df.drop(data, inplace=True)

df['Full content'] = df['Title'].astype(str) + '.' + df['Review Text']


def get_category(rating):
    score = int(rating)
    if score > 3:
        return 'Good'
    else:
        return 'Bad'


df['Category'] = df['Rating'].apply(get_category)

df = df[['Full content', 'Category']]

category_counts = df['Category'].value_counts()
good_count = category_counts.get('Good', 0)

if good_count > 2500:
    excess_rows = good_count - 2500
    excess_indexes = df[df['Category'] == 'Good'].index[:excess_rows]
    df.drop(excess_indexes, inplace=True)


def text_lowercase(text):
    return text.lower()


df['Full content'] = df['Full content'].apply(text_lowercase)


def remove_numbers(text):
    return '' .join((i for i in text if not i.isdigit()))


df['Full content'] = df['Full content'].apply(remove_numbers)


def remove_punctuation(text):
    return text.translate(str.maketrans('', '', string.punctuation))


df['Full content'] = df['Full content'].apply(remove_punctuation)


def remove_whitespace(text):
    return text.strip()


df['Full content'] = df['Full content'].apply(remove_whitespace)

stop_words = set(stopwords.words("english"))


def remove_stopwords(word_tokens):
    filtered_sentence = []
    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)
    return filtered_sentence


df['Full content'] = df['Full content'].apply(word_tokenize)
df['Full content'] = df['Full content'].apply(remove_stopwords)


stemmer = PorterStemmer()


def stem_words(tokens):
    return [stemmer.stem(token) for token in tokens]


df['Full content'] = df['Full content'].apply(stem_words)

lemmatizer = WordNetLemmatizer()


def lemmatize_word(text):
    if isinstance(text, str):
        word_tokens = word_tokenize(text)
        lemmas = [lemmatizer.lemmatize(word, pos='v') for word in word_tokens]
        return ' '.join(lemmas)
    else:
        return text


df['Full content'] = df['Full content'].apply(lambda x: ' '.join(x))
df['Full content'] = df['Full content'].apply(lemmatize_word)

count_vect = CountVectorizer()

X_train_counts = count_vect.fit_transform(df['Full content'])

df_counts = pd.DataFrame(X_train_counts.toarray(),
                         columns=count_vect.get_feature_names_out())
df_counts.to_csv('prepared data.csv', header=False, index=False)

X_train_counts = count_vect.transform(df['Full content'])

df_vectors = pd.DataFrame(X_train_counts.toarray(),
                          columns=count_vect.get_feature_names_out())
df_vectors['Category'] = df['Category']

df_vectors.to_csv('vectorized_data.csv', index=False)

tfidf_transformer = TfidfTransformer()
X = tfidf_transformer.fit_transform(X_train_counts)
y = df['Category']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3,
                                                    random_state=42)

naive_bayes = MultinomialNB()

naive_bayes.fit(X_train, y_train)

predicted = naive_bayes.predict(X_test[124].reshape(1, -1))


print("Actual Value:", y_test.iloc[124])
print("Predicted Value:", predicted[0])
