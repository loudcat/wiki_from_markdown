import unittest
import walk

class TestSearchInFiles(unittest.TestCase):
    def test_one_word(self):
        out = walk.search_in_files('wiki', 'Contributing')
        self.assertEqual([],out)
