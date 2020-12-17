import os
import pytest
import random
import string
from collections import Counter

from word_parser.parser import Parser

FILE_PATH = os.path.dirname(__file__)


@pytest.fixture(scope="function")
def test_input():
    with open(f"{FILE_PATH}/test_input.txt") as input_file:
        words = input_file.read().splitlines()[0].split(" ")
    yield words


def test_get_stop_words():
    test_parser = Parser(
        input_file="fake.txt", rules_file=f"{FILE_PATH}/test_stopwords.txt"
    )
    assert test_parser.stop_words == {"a", "about", "above", "after", "again"}


def test_stop_words_removed(test_input):
    test_parser = Parser(
        input_file="fake.txt", rules_file=f"{FILE_PATH}/test_stopwords.txt"
    )

    final_list = []
    for word in test_input:
        if not test_parser.exclude_stop_words(word):
            final_list.append(word)
    assert final_list == [
        "There's",
        "story",
        "simple",
        "man",
        "trying",
        "to",
        "make",
        "his",
        "way",
        "in",
        "the",
        "universe",
    ]


def test_non_alpha_removed(test_input):
    test_parser = Parser(input_file="fake.txt", rules_file="fake.txt")
    final_list = []
    for word in test_input:
        final_list.append(test_parser.remove_non_alpha(word))
    assert final_list == [
        "Theres",
        "a",
        "story",
        "about",
        "a",
        "simple",
        "man",
        "trying",
        "to",
        "make",
        "his",
        "way",
        "in",
        "the",
        "universe",
    ]


def test_parse_line():
    test_parser = Parser(
        input_file="fake.txt", rules_file=f"{FILE_PATH}/test_stopwords.txt"
    )
    with open(f"{FILE_PATH}/test_input.txt") as input_file:
        line = input_file.read().splitlines()[0]
        test_parser.parse_line(line)
    assert test_parser.final_words == Counter(
        {
            "there": 1,
            "stori": 1,
            "simpl": 1,
            "man": 1,
            "try": 1,
            "to": 1,
            "make": 1,
            "hi": 1,
            "wai": 1,
            "in": 1,
            "the": 1,
            "univers": 1,
        }
    )


def test_parse_file():
    test_parser = Parser(
        input_file=f"{FILE_PATH}/test_input.txt",
        rules_file=f"{FILE_PATH}/test_stopwords.txt",
    )
    test_parser.parse_file()
    assert test_parser.final_words == Counter(
        {
            "there": 1,
            "stori": 1,
            "simpl": 1,
            "man": 1,
            "try": 1,
            "to": 1,
            "make": 1,
            "hi": 1,
            "wai": 1,
            "in": 1,
            "the": 1,
            "univers": 1,
        }
    )


def test_insert_top_word():
    test_parser = Parser(input_file="fake.txt", rules_file="fake.txt")
    top_words = [("a", 4), ("b", 3)]
    test_parser.insert_top_word(0, top_words, 5, "c", 5)
    assert top_words == [("c", 5), ("a", 4), ("b", 3)]


def test_insert_top_word_beyond_max():
    test_parser = Parser(input_file="fake.txt", rules_file="fake.txt")
    top_words = [("a", 4), ("b", 3)]
    test_parser.insert_top_word(3, top_words, 2, "c", 2)
    assert top_words == [("a", 4), ("b", 3)]


def test_get_root_word():
    test_parser = Parser(input_file="fake.txt", rules_file="fake.txt")
    root_words = []
    with open(f"{FILE_PATH}/test_stem.txt") as f:
        for word in f.read().splitlines():
            root_words.append(test_parser.get_root_word(word))
    assert root_words == ["jump", "jump", "jump"]


def test_top_words():
    # Seed random to ensure same results
    random.seed(1)
    test_parser = Parser(input_file="fake.txt", rules_file="fake.txt")
    for letter in string.ascii_lowercase:
        test_parser.final_words[letter] = random.randint(1, 20)
    top_words = test_parser.get_top_words(20)
    print(test_parser.final_words.most_common(20))
    print(top_words)
    assert top_words == [
        ("p", 20),
        ("b", 19),
        ("u", 19),
        ("f", 16),
        ("h", 16),
        ("l", 16),
        ("g", 15),
        ("r", 15),
        ("o", 14),
        ("i", 13),
        ("n", 13),
        ("w", 11),
        ("d", 9),
        ("s", 9),
        ("t", 8),
        ("j", 7),
        ("a", 5),
        ("e", 4),
        ("k", 4),
        ("v", 4),
    ]
