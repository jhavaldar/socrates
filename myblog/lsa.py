
from gensim import corpora, models, similarities
import json
from collections import defaultdict
import os

class LSA:

  def __init__(self, relative_root, sentiment_path, num_topics=500):

    self.dict_path = relative_root+'corp.dict'
    self.corp_path = relative_root+"corp.mm"
    self.model_path = relative_root+'corp.lsi'
    self.index_path = relative_root+'corp1.index'
    self.num_topics = num_topics
    self.sentiment_path = sentiment_path
    with open(self.sentiment_path) as data_file:
      self.sentiments = json.load(data_file)

    for path in [self.dict_path, self.corp_path, self.model_path, self.index_path]:
      dirname = os.path.dirname(path)
      if not os.path.exists(dirname):
        os.makedirs(dirname)

    self.sentiment_tags = [key for key in self.sentiments]

  def analyze_corpus(self,comments):
    self.save_dict(comments, dict_path=self.dict_path, corp_path=self.corp_path)  # Saves full corpus & dictionary
    self.save_lsi(dict_path=self.dict_path, corp_path=self.corp_path, num_topics=self.num_topics, model_path=self.model_path) # Saves model
    self.save_index(dict_path=self.dict_path, corp_path=self.corp_path, sentiment_path=self.sentiment_path, model_path=self.model_path, index_path=self.index_path) # Saves index

  @staticmethod
  # Check if a string is ASCII
  def is_ascii(s):
      return all(ord(c) < 128 for c in s)

  # Input is an array of documents. Output is a dictionary (map from words to IDs); corpus and dictionary are saved to disk.
  def save_dict(self, corp, dict_path, corp_path):
    stemmer = PorterStemmer()
    stoplist = set('for a of the and to in [deleted] [removed]'.split())
    texts = [[word for word in comment.lower().split() if word not in stoplist] for comment in corp]

    # Create the frequency dictionary of words.
    frequency = defaultdict(int)
    for text in texts:
      for token in text:
        frequency[token] += 1

    # Turn each sentence into a list of present tokens

    texts = [[token for token in text if frequency[token] > 1]  for text in texts]

    dictionary = corpora.Dictionary(texts)
    dictionary.save(dict_path)  # store the dictionary, for future reference
    corpus = [dictionary.doc2bow(text) for text in texts]
    corpora.MmCorpus.serialize(corp_path, corpus)
    return dictionary

  # Inputs are a corpus, a number of topics (singular values), and a dictionary (words to IDs). Output is a trained LSI model
  # which uses tf idf
  def save_lsi(self, dict_path, corp_path, model_path, num_topics=300):
    dictionary = corpora.Dictionary.load(dict_path)
    corpus = corpora.MmCorpus(corp_path)

    tfidf = models.TfidfModel(corpus) # step 1 -- initialize a model

    corpus_tfidf = tfidf[corpus]  # Re-write the corpus using tf-idf weightings

    # Initialize an LSI model given a corpus, a dictionary, and a number of singular values.
    lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=num_topics) # initialize an LSI transformation
    corpus_lsi = lsi[corpus_tfidf] # create a double wrapper over the original corpus: bow->tfidf->fold-in-lsi
    lsi.save(model_path) # same for tfidf, lda, ...
    return lsi

  # Given a dictionary, a corpus, and an LSI model, and an array of documents upon which to perform a query, 
  # Return an index and save to a given path
  def save_index(self, dict_path, corp_path, sentiment_path, model_path, index_path):
    lsi = models.LsiModel.load(model_path)
    corpus = corpora.MmCorpus(corp_path)
    dictionary = corpora.Dictionary.load(dict_path)
    tfidf = models.TfidfModel(corpus)

    with open(sentiment_path) as data_file:
      data = json.load(data_file)

    texts = [[word for word in data[key].lower().split()] for key in data]
    self.feelings = [key for key in data]

    comparison_corp = [dictionary.doc2bow(text) for text in texts]
    comparison_corpus_tfidf = tfidf[comparison_corp]
    index = similarities.MatrixSimilarity(lsi[comparison_corpus_tfidf])
    index.save(index_path)
    return index

  # Given an array of names for each document, a query document, return the top two most similar documents 
  # In the index corpus (aka sentiments)
  def get_sentiment(self, query):
    lsi = models.LsiModel.load(self.model_path)
    dictionary = corpora.Dictionary.load(self.dict_path)
    index = similarities.MatrixSimilarity.load(self.index_path)

    query = [word for word in query.lower().split() if self.is_ascii(word)]

    vec_bow = dictionary.doc2bow(query)
    vec_lsi = lsi[vec_bow]
    sims = index[vec_lsi] # perform a similarity query against the corpus
    scores = [list(i) for i in enumerate(sims)]
    sorted_scores = sorted(scores, key=lambda pair: abs(pair[1]))
    dict = {}
    for pair in sorted_scores:
      feeling = self.sentiment_tags[pair[0]]
      score = abs(pair[1])
      dict[feeling] = score
    return dict
