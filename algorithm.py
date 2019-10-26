import os
import csv
import subprocess
import re
import random
import numpy as np


def read_in_shakespeare():
  '''Reads in the Shakespeare dataset processesit into a list of tuples.
     Also reads in the vocab and play name lists from files.

  Each tuple consists of
  tuple[0]: The name of the play
  tuple[1] A line from the play as a list of tokenized words.

  Returns:
    tuples: A list of tuples in the above format.
    document_names: A list of the plays present in the corpus.
    vocab: A list of all tokens in the vocabulary.
  '''

  tuples = []

  with open('items.csv') as f:
    csv_reader = csv.reader(f, delimiter=';')
    for row in csv_reader:
      play_name = row[0]
      line = row[1]
      line_tokens = re.sub(r'[^a-zA-Z0-9\s]', ' ', line).split()
      line_tokens = [token.lower() for token in line_tokens]

      tuples.append((play_name, line_tokens))

  with open('vocabulary.txt') as f:
    vocab =  [line.strip() for line in f]

  with open('url.txt') as f:
    document_names =  [line.strip() for line in f]

  return tuples, document_names, vocab

def get_row_vector(matrix, row_id):
  return matrix[row_id, :]

def get_column_vector(matrix, col_id):
  return matrix[:, col_id]

def create_term_document_matrix(line_tuples, document_names, vocab):
  '''Returns a numpy array containing the term document matrix for the input lines.

  Inputs:
    line_tuples: A list of tuples, containing the name of the document and 
    a tokenized line from that document.
    document_names: A list of the document names
    vocab: A list of the tokens in the vocabulary

  # NOTE: THIS DOCSTRING WAS UPDATED ON JAN 24, 12:39 PM.

  Let m = len(vocab) and n = len(document_names).

  Returns:
    td_matrix: A mxn numpy array where the number of rows is the number of words
        and each column corresponds to a document. A_ij contains the
        frequency with which word i occurs in document j.
  '''

  vocab_to_id = dict(zip(vocab, range(0, len(vocab))))
  docname_to_id = dict(zip(document_names, range(0, len(document_names))))

  # YOUR CODE HERE
  result = np.zeros((len(vocab_to_id),len(docname_to_id)), dtype=int)
  try:
    for book,line in line_tuples:
      doc_index = docname_to_id.get(book)
      if(doc_index is not None):
        for word in line:
          vocab_index = vocab_to_id.get(word)
          if(vocab_index is not None):
            result[vocab_index][doc_index]+=1
  except Exception as e:
    print(e)
  return result

def compute_cosine_similarity(vector1, vector2):
  '''Computes the cosine similarity of the two input vectors.

  Inputs:
    vector1: A nx1 numpy array
    vector2: A nx1 numpy array

  Returns:
    A scalar similarity value.
  '''
  d = np.dot(vector1,vector2)
  a = np.sqrt((vector1**2).sum())
  b = np.sqrt((vector2**2).sum())
  result = d/(a*b)
  # YOUR CODE HERE
  return result

def compute_jaccard_similarity(vector1, vector2):
  '''Computes the cosine similarity of the two input vectors.

  Inputs:
    vector1: A nx1 numpy array
    vector2: A nx1 numpy array

  Returns:
    A scalar similarity value.
  '''
  
  # YOUR CODE HERE
  return np.minimum(vector1, vector2).sum() / np.maximum(vector1, vector2).sum()

def compute_dice_similarity(vector1, vector2):
  '''Computes the cosine similarity of the two input vectors.

  Inputs:
    vector1: A nx1 numpy array
    vector2: A nx1 numpy array

  Returns:
    A scalar similarity value.
  '''

  # YOUR CODE HERE
  n = 2. * np.minimum(vector1,vector2).sum()
  d = (vector1 + vector2).sum()
  return n/d

def rank_plays(target_play_index, term_document_matrix, similarity_fn):
  ''' Ranks the similarity of all of the plays to the target play.

  # NOTE: THIS DOCSTRING WAS UPDATED ON JAN 24, 12:51 PM.

  Inputs:
    target_play_index: The integer index of the play we want to compare all others against.
    term_document_matrix: The term-document matrix as a mxn numpy array.
    similarity_fn: Function that should be used to compared vectors for two
      documents. Either compute_dice_similarity, compute_jaccard_similarity, or
      compute_cosine_similarity.

  Returns:
    A length-n list of integer indices corresponding to play names,
    ordered by decreasing similarity to the play indexed by target_play_index
  '''
  
  # YOUR CODE HERE
  m = len(term_document_matrix)
  n = len(term_document_matrix[0])
  result = np.zeros(n)
  tpi = get_column_vector(term_document_matrix, target_play_index)
  for index in range(n):
    doc = get_column_vector(term_document_matrix, index)
    result[index] = similarity_fn(tpi, doc)
  sort_result = np.argsort(-result)
  return sort_result

def calculate(url=None,amount=10):
  tuples, document_names, vocab = read_in_shakespeare()
  # print(len(tuples))
  # print(len(document_names))
  # print(len(vocab))
  print('Computing term document matrix...')
  td_matrix = create_term_document_matrix(tuples, document_names, vocab)
  if url is None:
    random_idx = random.randint(0, len(document_names)-1)
    similarity_fns = [compute_cosine_similarity, compute_jaccard_similarity, compute_dice_similarity]
    for sim_fn in similarity_fns:
      print('\nThe %i most similar websites to "%s" using %s are:' % (amount,document_names[random_idx], sim_fn.__name__))
      ranks = rank_plays(random_idx, td_matrix, sim_fn)
      for idx in range(0, amount):
        doc_id = ranks[idx]
        print('%d: %s' % (idx+1, document_names[doc_id]))
