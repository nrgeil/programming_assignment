import re
from collections import Counter

from word_parser.utils.porter_stemmer import PorterStemmer


class Parser:
    def __init__(self, input_file, rules_file):
        """
        This class takes an input file and a rules file. Any words in the rules file are excluded and non-alphabetical
        characters are removed. Words are them stemmed into their root form using the Porter Stemmer algorithm and the
        frequency of each word calculated. Finally, returns the top 20 most used words

        :param input_file: File to parse
        :param rules_file: File containing words to ignore with one word per line
        """
        self.input_file = input_file
        self.rules_file = rules_file
        self.valid_characters = r"[A-Za-z]"
        self.final_words = Counter()
        self.stemmer = PorterStemmer()

    @property
    def stop_words(self):
        """
        Creates a set of the words to ignore

        :return: Set
        """
        with open(self.rules_file, "r") as rules:
            return set(line.strip() for line in rules.read().splitlines())

    @staticmethod
    def insert_top_word(idx, top_words, n, word, count):
        if idx > n:
            return
        else:
            top_words.insert(
                idx,
                (
                    word,
                    count,
                ),
            )

    def get_top_words(self, n):
        """
        Originally planned on using a dictionary to keep track of unique word counts. While checking the
        python documentation for OrderedDict in collections, I came across the Counter class and used that instead.
        Implementing my own "most_common" method in case that is desired.

        :param n: Number of words to return
        :return: List of tuples of the "n" most common words and how often they appeared.
        """
        top_words = []
        for word, count in self.final_words.items():
            if not top_words:
                top_words.append(
                    (
                        word,
                        count,
                    )
                )
                continue
            insert_at = None
            # Check in reverse order so if current item is lower than min value or alphabetically sorts lower,
            # we can safely break out to save on iterations
            for idx, top_word in enumerate(top_words[-1::-1]):
                # Need to grab position from start of list since iterating backwards
                position = len(top_words) - 1 - idx
                # If max number of words not yet found and word is new lowest value, just append to list and stop
                # checking
                if count < top_word[1] and len(top_words) < n:
                    insert_at = position + 1
                    break
                if count > top_word[1]:
                    insert_at = position
                    continue
                # For ties at a position, take the alphabetically first word to ensure consistent results
                elif count == top_word[1] and word < top_word[0]:
                    insert_at = position
                elif count == top_word[1] and word > top_word[0]:
                    insert_at = position + 1
                    # List already alphabetically sorted. Safe to break out
                    break
                # List already sorted by frequency. Safe to break out
                elif count < top_word[1]:
                    break
            if insert_at is not None:
                self.insert_top_word(insert_at, top_words, n, word, count)
            # Check if word inserted and caused number of results to exceed max number expected
            if len(top_words) > n:
                top_words.pop()
        return top_words

    def exclude_stop_words(self, word):
        """
        Determines if a word should be ignored

        :param word: The word to consider
        :return: Boolean
        """
        if word in self.stop_words:
            return True
        else:
            return False

    def remove_non_alpha(self, word):
        """
        Removes any non-alphabetical characters from a word

        :param word: The word to consider
        :return: String: The input word with all invalid characters removed
        """
        return "".join(re.findall(self.valid_characters, word))

    def parse_line(self, line):
        """
        Splits a line on the space character and runs the rules against it. If the word isn't excluded, it appends
        it to a list of valid words with invalid characters removed

        :param line: The current line being parsed
        :return: None
        """
        for word in line.split(" "):
            if self.exclude_stop_words(word):
                continue
            else:
                alpha_word = self.remove_non_alpha(word)
                if not alpha_word:
                    continue
                root_word = self.get_root_word(alpha_word)
                try:
                    self.final_words[root_word] += 1
                except KeyError:
                    self.final_words[root_word] = 1

    def get_root_word(self, word):
        """
        Using the Python supported Porter Stemmer algorithm from https://tartarus.org/martin/PorterStemmer/,
        stem the word into its root form

        :param word: The word to find the root of using the Porter Stemmer Algorithm
        :return: String: The root form of the provided word
        """
        root_word = self.stemmer.stem(word.lower(), 0, len(word) - 1)
        return root_word

    def parse_file(self):
        """
        Opens the provided input file and parses it line by line

        :return: None
        """
        with open(self.input_file, "r") as f:
            for line in f.read().splitlines():
                if line == "":
                    continue
                self.parse_line(line)
