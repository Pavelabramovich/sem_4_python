from parse import sentences_count
from parse import non_declarative_sentences_count
from parse import average_sentence_length
from parse import average_word_length
from parse import sub_sentences_top

from input import non_empty_input
from input import pos_int_input


if __name__ == '__main__':
    try:
        text = non_empty_input("Enter the text to analiz: ")

        print("Sentence count: ", sentences_count(text))
        print("Non declarative sentence count: ", non_declarative_sentences_count(text))

        print("Average sentence length: ", average_sentence_length(text))

        print("Average word length: ", average_word_length(text))

        k = pos_int_input("Enter top size: ")
        n = pos_int_input("Enter subsentence length: ")
        prettier_subsentence = lambda ss: ' '.join(ss[0]) + f' x{ss[1]}'
        ans = ', '.join([prettier_subsentence(subsentence) for subsentence in sub_sentences_top(text, k, n)])

        if ans:
            print("Top subsentence: ", ans)
        else:
            print("There are no subsentences in the text")

    except ValueError as error:
        print(error)



