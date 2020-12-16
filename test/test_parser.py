import os
import pytest

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
    assert test_parser.final_words == [
        "Theres",
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


def test_parse_file():
    test_parser = Parser(
        input_file=f"{FILE_PATH}/test_input.txt",
        rules_file=f"{FILE_PATH}/test_stopwords.txt",
    )
    test_parser.parse_file()
    assert test_parser.final_words == [
        "Theres",
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


def test_get_root_word():
    assert False


def test_word_frequency():
    assert False


def test_top_words():
    assert False
