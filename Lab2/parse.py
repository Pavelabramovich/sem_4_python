import re
from collections import Counter


NAME_ABBREVIATION_PATTERN = (
    r"\b(Mr\.|Ms\.|Mrs\.|Dr\.|Lt\.|St\.|Blvd\.|" +
    r"Ave\.|Sq\.|Rd\.|Bldg\.|B\.Sc\.|M\.D\.|Ph\.D\.|Rep\.|\w\.)")

NONAME_ABBREVIATIONS_PATTERN = (
    r"\b(i\.e|e\.g\.|etc\.|p\.a\.|a\.m\.|p\.m\.|P\.S\.|Re\.|p\.|" +
    r"exp\.|err\.|et\.al\.|ex\.|fin\.|vs\.|N\.B\.|" +
    r"ft\.|oz\.|pt\.|in\.|sec\.|g\.|cm\.|qt\.|" +
    r"Jan\.|Feb\.|Aug\.|Sept\.|Oct\.|Nov\.|Dec\.|Sun\.|" +
    r"Mon\.|Tues\.|Wed\.|Thurs\.|Fri\.|Sat.\|Sun\.|" +
    r"\.com|\.ru|\.by|\.cpp|\.cs|\.txt|\.py)")

ELLIPSE_PATTERN = r"\.\s*\.\s*\."

QUESTION_PATTERN = r"(\!\?|\?\!|\!\s*\!\s*\!|\?\?)"

DIRECT_SPEECH_PATTERN = r'"([^"]*?)([\.?!])?"\s*([^A-Z])?'

WORD_PATTERN = r"\w*[a-zA-Z]\w*"


def clear_ellipsis(text: str) -> str:
    text = re.sub(ELLIPSE_PATTERN, '.', text)
    return re.sub(QUESTION_PATTERN, ' ! ', text)


def clear_name_abbreviations(text: str) -> str:
    return re.sub(NAME_ABBREVIATION_PATTERN, clear_points, text)


def clear_noname_abbreviations(text: str) -> str:
    return re.sub(fr"{NONAME_ABBREVIATIONS_PATTERN}(?!\s+[A-Z])", clear_points, text)


def clear_points(abbreviation: re.Match) -> str:
    return abbreviation.group(0).replace('.', ' ')


def clear_direct_speeches(text: str) -> str:
    return re.sub(DIRECT_SPEECH_PATTERN, clear_direct_speech, text)


def clear_direct_speech(direct_speech: re.Match) -> str:
    result = re.match(DIRECT_SPEECH_PATTERN, direct_speech.group(0))

    # If direct speech contains replicas ending with a period, question or exclamation marks,
    # then this is not considered a sentence. Therefore, you need to remove unnecessary characters.
    ds = result.group(1).replace('.', ' ').replace('!', ' ').replace('?', ' ')

    letter = result.group(3) if result.group(3) else ''

    # If the end of direct speech is the end of a sentence, then we need to
    # leave a dot for further consideration as a declarative sentence.
    return ds + ('.' if result.group(2) and not result.group(3) else ' ') + letter


def clear_sentences(text: str) -> str:
    text = clear_direct_speeches(text)
    text = clear_ellipsis(text)
    text = clear_noname_abbreviations(text)
    text = clear_name_abbreviations(text)

    return text


def sentences_count(text: str) -> int:
    text = clear_sentences(text)

    return text.count('.') + text.count('?') + text.count('!')


def non_declarative_sentences_count(text: str) -> int:
    text = clear_sentences(text)

    return text.count('?') + text.count('!')


def average_sentence_length(text: str) -> float:
    text = clear_sentences(text)

    # After split, list will contain one extra empty sentence. Slice is needed to get rid of it.
    sentences = text.replace('?', '.').replace('!', '.').split('.')[:-1]
    words = split_words(text)

    if not words:
        raise ValueError("Text has no words")

    lengths = [len(word) for word in words]

    try:
        return sum(lengths) / len(sentences)
    except ZeroDivisionError as error:
        raise ValueError("Text has no sentences.") from error


def average_word_length(text: str):
    text = clear_sentences(text)
    words = split_words(text)

    if not words:
        raise ValueError("Text has no words")

    lengths = [len(word) for word in words]

    return sum(lengths) / len(words)


def split_words(sentence: str) -> list[str]:
    return re.findall(WORD_PATTERN, sentence)


def sub_sentences_top(text: str, top_of: int = 10, ss_len: int = 4):
    words = split_words(text)
    words = [word.lower() for word in words]

    # We create a collection of sub-sentences by enumeration of all combinations with
    # a check for the count of words. Converting to tuple to get the hash.
    sub_sentences = [tuple(words[i:i + ss_len]) for i in range(len(words) - ss_len + 1)]

    # We transform the collection into a dictionary for counting and removing duplicates.
    counter = Counter(sub_sentences)

    # We get a list of pairs: sub-sentence and the number of repetitions.
    # Sort by number of repetitions in reverse order.
    lst = sorted(counter.items(), key=lambda kv: kv[1], reverse=True)

    # Return the required number of sub-sentences.
    return lst[:top_of:]


if __name__ == "__main__":

    string = """
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

    string2 = "lol2 loL lol lal. Lol. "

    string3 = "I hate you. You be my brother, Anakin. "

    print(sentences_count(string))
    print(non_declarative_sentences_count(string))
    print(average_sentence_length(string))
    print(average_word_length(string))
    print(sub_sentences_top(string, 10, 3))
