import json
import re
import os.path
import pickle
from pymorphy2 import MorphAnalyzer


class SearchEngine:
    """
    Search engine
    """
    def __init__(self):
        self.morph = MorphAnalyzer()
        self.inverted_index_dict = {'phrases_index': {},
                                    'counter_dict': {},
                                    'categories': []}

        if os.path.isfile('inverted_index.pickle'):
            with open('inverted_index.pickle', 'rb') as handle:
                self.inverted_index_dict = pickle.load(handle)
        else:
            with open('docs.json', encoding='utf8') as f:
                self.docs = json.load(f)
            self.build_inverted_index(self.docs)
            with open('inverted_index.pickle', 'wb') as handle:
                pickle.dump(self.inverted_index_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
            del self.docs

    async def convert_sentence(self, sentence):
        """
        Each word converts to normal form and returned as a list.
        """
        sentence = re.sub(r'\W|\d', ' ', sentence)
        tokens = sentence.lower().split()
        result = [self.morph.parse(word)[0].normal_form for word in tokens]
        return result

    def build_inverted_index(self, docs):
        """
        Initializes creation of inverted index and category list.
        """
        for document_idx, doc in enumerate(docs):
            self.build_dictionary(document_idx, doc, 'phrases', self.inverted_index_dict['phrases_index'])

        self.inverted_index_dict['categories'] = [i['category'] for i in self.docs]

    def build_dictionary(self, doc_idx, doc, section, dictionary):
        """
        Builds an inverted index dictionary.
        """
        if section in doc:
            for sentence_ind, sentence in enumerate(doc[section]):
                splitted_sentence = self.tokenize(sentence)

                if doc_idx in self.inverted_index_dict['counter_dict']:
                    self.inverted_index_dict['counter_dict'][doc_idx] += (len(splitted_sentence),)
                else:
                    self.inverted_index_dict['counter_dict'][doc_idx] = (len(splitted_sentence),)
                for word in splitted_sentence:
                    if word not in dictionary:
                        dictionary[word] = {}
                    if doc_idx in dictionary[word]:
                        dictionary[word][doc_idx] += (sentence_ind,)
                    else:
                        dictionary[word][doc_idx] = (sentence_ind,)

    async def get_categories(self, sentence):
        """
        Сoroutine get the sentence and returns json with the list of categories.
        """
        result = {'categories': ()}
        _categories = ()
        _links = []

        # calling coroutine, bringing each word to normal form.
        converted_words = await self.convert_sentence(sentence)
        for word in converted_words:
            if word in self.inverted_index_dict['phrases_index']:
                # tuple with category_ids in index for word
                _categories += tuple(self.inverted_index_dict['phrases_index'][word].keys())
                # dicts with categories_id and phrases_id in index  for word
                _links.append(self.inverted_index_dict['phrases_index'][word])

        for category in set(_categories):
            # count the number of words for each of the categories
            _word_ids = sum([x[category] for x in _links if x.get(category)], ())
            for i in set(_word_ids):
                real_count = _word_ids.count(i)
                # If count of words in phrase matches the actual number === the phrase matches the search query.
                if self.inverted_index_dict['counter_dict'][category][i] == real_count:
                    result['categories'] += (self.inverted_index_dict['categories'][category],)
        return result

    def tokenize(self, sentence):
        sentence = re.sub(r'\W|\d', ' ', sentence)
        tokens = sentence.lower().split()
        result = [self.morph.parse(word)[0].normal_form for word in tokens]
        return result
