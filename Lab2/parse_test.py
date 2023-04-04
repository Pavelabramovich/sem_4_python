import unittest

from parse import clear_ellipsis
from parse import clear_name_abbreviations
from parse import clear_other_abbreviations
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
        self.ELLIPSIS_TST = "This was so close. . . I want see this again."
        self.ELLIPSIS_RES = "This was so close. I want see this again."

        self.ClEAR_NAME_ABBREVIATION_TST = "Dr. Livesey said, that the log cabin is not visible from the ship."
        self.ClEAR_NAME_ABBREVIATION_RES = "Dr  Livesey said, that the log cabin is not visible from the ship."

        self.CLEAR_OTHER_ABBREVIATION_TST = """"The chest contains gold, diamonds, etc.," Billy said."""
        self.CLEAR_OTHER_ABBREVIATION_RES = """"The chest contains gold, diamonds, etc ," Billy said."""

        self.CLEAR_DIRECT_SPEECHES_TST = """"Come to me at 7p.m.," he said to Jim."""
        self.CLEAR_DIRECT_SPEECHES_RES = """Come to me at 7p m , he said to Jim."""

        self.CLEAR_SENTENCES_TST = """
        Dr. Livesey said, "The log cabin is not visible from the ship. 
        They must be aiming at a flag. We must load a flag advance."
        """

        self.CLEAR_SENTENCES_RES = """
        Dr  Livesey said, The log cabin is not visible from the ship  
        They must be aiming at a flag  We must load a flag advance."""

        self.TEXT_TST = """
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

        self.SENTENCES_COUNT = 15

        self.NON_DECLARATIVE_SENTENCES_COUNT = 4

        self.AVERAGE_SENTENCE_LENGTH = 437 / 15

        self.AVERAGE_WORD_LENGTH = 437 / 116

        self.SPLIT_WORDS_TST = """The word "rum" and the word "death" mean the same thing to you."""

        self.SPLIT_WORDS_RES = ['The', 'word', 'rum', 'and', 'the', 'word', 'death', 'mean', 'the', 'same', 'thing', 'to', 'you']

        self.TOP_TST = [("['the', 'word']", 2), ("['word', 'rum']", 1), ("['rum', 'and']", 1)]

    def test_clear_ellipsis(self):
        self.assertEqual(clear_ellipsis(self.ELLIPSIS_TST), self.ELLIPSIS_RES)

    def test_clear_name_abbreviation(self):
        self.assertEqual(clear_name_abbreviations(self.ClEAR_NAME_ABBREVIATION_TST), self.ClEAR_NAME_ABBREVIATION_RES)

    def test_clear_other_abbreviation(self):
        self.assertEqual(clear_other_abbreviations(self.CLEAR_OTHER_ABBREVIATION_TST),
                         self.CLEAR_OTHER_ABBREVIATION_RES)

    def test_clear_direct_speeches(self):
        self.assertEqual(clear_direct_speeches(self.CLEAR_DIRECT_SPEECHES_TST), self.CLEAR_DIRECT_SPEECHES_RES)

    def test_clear_sentences(self):
        self.assertEqual(clear_sentences(self.CLEAR_SENTENCES_TST), self.CLEAR_SENTENCES_RES)

    def test_sentences_count(self):
        self.assertEqual(sentences_count(self.TEXT_TST), self.SENTENCES_COUNT)

    def test_non_declarative_sentences_count(self):
        self.assertEqual(non_declarative_sentences_count(self.TEXT_TST), self.NON_DECLARATIVE_SENTENCES_COUNT)

    def test_average_sentence_length(self):
        self.assertEqual(average_sentence_length(self.TEXT_TST), self.AVERAGE_SENTENCE_LENGTH)

    def test_average_word_length(self):
        self.assertEqual(average_word_length(self.TEXT_TST), self.AVERAGE_WORD_LENGTH)

    def test_split_words(self):
        self.assertEqual(split_words(self.SPLIT_WORDS_TST), self.SPLIT_WORDS_RES)

    def test_sub_sentences_top(self):
        self.assertEqual(sub_sentences_top(self.SPLIT_WORDS_TST, 3, 2), self.TOP_TST)


if __name__ == '__main__':
    unittest.main()
