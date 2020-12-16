import re


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
        self.valid_characters = r"\w"
        self.final_words = []

    @property
    def stop_words(self):
        """
        Creates a set of the words to ignore

        :return: Set
        """
        with open(self.rules_file, "r") as rules:
            return set(line.strip() for line in rules.read().splitlines())

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
                self.final_words.append(self.remove_non_alpha(word))

    def parse_file(self):
        """
        Opens the provided input file and parses it line by line

        :return: None
        """
        with open(self.input_file, "r") as f:
            for line in f.read().splitlines():
                self.parse_line(line)
