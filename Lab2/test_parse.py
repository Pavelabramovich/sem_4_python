import unittest

from parse import clear_ellipsis
from parse import clear_name_abbreviations
from parse import clear_noname_abbreviations
from parse import clear_direct_speeches
from parse import clear_sentences
from parse import sentences_count
from parse import non_declarative_sentences_count
from parse import average_sentence_length
from parse import average_word_length
from parse import split_words
from parse import sub_sentences_top


class ParseTest(unittest.TestCase):

    def setUp(self):
        self.test_text = """
            Dr. Livesey said, "The log cabin is not visible from the ship. They must be aiming at a flag. We must load a flag advance."
            The word "rum" and the word "death" mean the same thing to you.
            Where's the map, Billy?
            The devil is with them! It's been over hours! It's getting a little boring. . .
            Billy Bones, aka "Captain". The owner of the Treasure Island map, which started it all. 
            He drinks a lot and always has a cold. Bad character. Not married.
            "The chest contains gold, diamonds, etc.," Billy said.
            Gold, diamonds, etc. not interested for me. We need a map!
            "Come to me at 7p.m.," he said to Jim.
            """

    def test_clear_ellipsis(self):
        test_str = "This was so close. . . I want see this again."

        expected_res = "This was so close. I want see this again."
        res = clear_ellipsis(test_str)

        self.assertEqual(res, expected_res)

    def test_clear_name_abbreviation(self):
        test_str = "Dr. Livesey said, that the log cabin is not visible from the ship."

        expected_res = "Dr  Livesey said, that the log cabin is not visible from the ship."
        res = clear_name_abbreviations(test_str)

        self.assertEqual(res, expected_res)

    def test_clear_noname_abbreviation(self):
        test_str = """"The chest contains gold, diamonds, etc.," Billy said."""

        expected_res = """"The chest contains gold, diamonds, etc ," Billy said."""
        res = clear_noname_abbreviations(test_str)

        self.assertEqual(res, expected_res)

    def test_clear_direct_speeches(self):
        test_str = '"Come to me at 7p.m.," he said to Jim.'

        expected_res = 'Come to me at 7p m , he said to Jim.'
        res = clear_direct_speeches(test_str)
        self.assertEqual(res, expected_res)

    def test_clear_sentences(self):
        test_str = """
            Dr. Livesey said, "The log cabin is not visible from the ship. 
            They must be aiming at a flag. We must load a flag advance."
            """

        expected_res = """
            Dr  Livesey said, The log cabin is not visible from the ship  
            They must be aiming at a flag  We must load a flag advance."""

        res = clear_sentences(test_str)

        self.assertEqual(res, expected_res)

    def test_sentences_count(self):
        test_text = self.test_text

        expected_res = 15
        res = sentences_count(test_text)

        self.assertEqual(res, expected_res)

    def test_non_declarative_sentences_count(self):
        test_text = self.test_text

        expected_res = 4
        res = non_declarative_sentences_count(test_text)

        self.assertEqual(res, expected_res)

    def test_average_sentence_length(self):
        test_text = self.test_text

        expected_res = 437 / 15
        res = average_sentence_length(test_text)

        self.assertEqual(res, expected_res)

    def test_average_word_length(self):
        test_text = self.test_text

        expected_res = 437 / 116
        res = average_word_length(test_text)

        self.assertEqual(res, expected_res)

    def test_split_words(self):
        test_str = 'The word "rum" and the word "death" mean the same thing to you.'

        expected_res = [
            'The', 'word', 'rum', 'and', 'the', 'word',
            'death', 'mean', 'the', 'same', 'thing', 'to', 'you'
        ]
        res = split_words(test_str)

        self.assertSequenceEqual(res, expected_res)

    def test_sub_sentences_top(self):
        self.SPLIT_WORDS_TST = 'The word "rum" and the word "death" mean the same thing to you.'
        self.TOP_TST = [(('the', 'word'), 2), (('word', 'rum'), 1), (('rum', 'and'), 1)]
        self.assertSequenceEqual(sub_sentences_top(self.SPLIT_WORDS_TST, 3, 2), self.TOP_TST)


if __name__ == '__main__':
    unittest.main()
