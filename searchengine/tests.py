import unittest
from searchengine.engine import SearchEngine


class TestSearch(unittest.TestCase):
    def test_tokenize_normalisation(self):
        engine = SearchEngine()

        tokens = engine.tokenize('Рецепты тайских супов')
        self.assertEqual(tokens, ['рецепт', 'тайский', 'суп'])

    def test_tokenize_letters(self):
        engine = SearchEngine()

        tokens = engine.tokenize('СтрокА вКлючаеТ цифры и небуквенные символы 23, 44 и @ * )')
        self.assertEqual(tokens, ['строка', 'включать', 'цифра', 'и', 'небуквенный', 'символ', 'и'])

    def test_search(self):
        engine = SearchEngine()

        self.assertEqual(engine.inverted_index_dict['phrases_index']['гагарин'][9][0], 2)
        self.assertEqual(engine.inverted_index_dict['counter_dict'][0][3], 5)
        self.assertEqual(engine.inverted_index_dict['categories'][0], 'News')


if __name__ == '__main__':
    unittest.main()
