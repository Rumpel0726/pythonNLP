import nltk
from nltk import stem
from nltk.tokenize import sent_tokenize
# nltk.download('punkt_tab')


text = """Была зима. Стоял лютый мороз. Люба и Люся бежали домой. Видит Люба: на дворе дети Андрюша и Нюра. Они сделали две кормушки и повесили их на дерево. Андрюша насыпал в кормушки зёрен."""

print("\nРазделение текста на предложения")
sentences = sent_tokenize(text, language="russian")
for sentence in sentences:
    print(sentence)

print("\nРазделение текста на слова")
tokens = nltk.word_tokenize(text, language="russian")
print(tokens)

print("\nРазделение предложений на слова")
for sentence in sentences:
    wordsList = nltk.word_tokenize(sentence, language="russian")
    print(wordsList)

print("\nРазделение предложений на слова без знаков препинания")
tokenizer = nltk.RegexpTokenizer(r'\w+')
for sentence in sentences:
    wordsList = tokenizer.tokenize(sentence)
    print(wordsList)

print("\nВывод слов с большой буквы")
tokenizer = nltk.RegexpTokenizer(r'[А-Я]\w+')
wordsList = tokenizer.tokenize(text)
print(wordsList)

print("\nСтематизация")
textRu = """Мы живем в информационную эпоху, когда компьютерная сеть охватывает
весь земной шар и соединяет не только страны и космические станции,
но и множество людей по всему миру"""
tokensRu = nltk.word_tokenize(textRu, language="russian")
stemmerRu = stem.snowball.SnowballStemmer("russian")
stemmedWordsRu = [stemmerRu.stem(word) for word in tokensRu]
print(stemmedWordsRu)
