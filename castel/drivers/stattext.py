from collections import Counter
import decimal
import logging
import regex

from castel.drivers.engine import Engine


class Stattext(Engine):
    """ The class parse a text and returns different statistics.

    This parser calculates the number of words, the number of lines,
    the most common letter(s) and the average number of letters per
    word.
    In this implementation the number and the letters are counted as words,
    for example in the following text we have 3 words: 'these 3 words'
    The words are considered separated by white space.
    """

    def __init__(self):
        self.total_words = None
        self.total_lines = None
        self.total_letters = None
        self.avg_letters_per_word = None
        self.precision = 1
        self.log = logging.getLogger(__name__)

    def get_total_words(self, text_wrapper):
        """
        The method get the total numbers of words in the
        text_wrapper passed
        args:
            text_wrapper: The text to parse
        """
        if not self.total_words:
            self.log.debug("Total words not defined proceeding"
                           "with counting words")
            self.total_words = self._count_words(text_wrapper)

        return self.total_words

    def get_total_lines(self, text_wrapper):
        """
        The method get the total numbers of lines
        found in the text_wrapper passed
        args:
            text_wrapper: The text to parse
        """
        if not self.total_lines:
            self.log.debug("Total lines not defined proceeding"
                           "with counting lines")
            self.total_lines = self._count_lines(text_wrapper)

        return self.total_lines

    def get_total_letters(self, text_wrapper):
        """
        The method get the total numbers of letters
        found in the text_wrapper passed
        args:
            text_wrapper: The text to parse
        """
        if not self.total_letters:
            self.log.debug("Total letters not defined proceeding"
                           "with counting letters")
            self.total_letters = self._count_alphanumeric(text_wrapper)

        return self.total_letters

    def get_avg_letters_per_word(self, text_wrapper):
        """
        The method get the average number of letters per word present in
        a text.
        args:
            text_wrapper: The text to parse
        """
        if not self.avg_letters_per_word:
            self.log.debug("Average letters per word  not defined proceeding"
                           "with calculating the average")
            self.avg_letters_per_word = \
                        self._avg_letters(text_wrapper,
                                         precision=self.precision)

        return self.avg_letters_per_word

    def most_common_letter(self, text_wrapper):
        """
        The method get the most letter(s) per word present in
        a text. In the case that more than one letter have the
        same occurences, they are all reported back.
        args:
            text_wrapper: The text to parse
        """
        total_occurences = Counter()
        for line in text_wrapper:
            # L matches the letter \p is for matching a single point code
            # \p{L} matches any single letter
            letters = regex.findall(r'[\p{L}]', line.lower())
            total_occurences.update(letters)

        if not total_occurences:
            self.log.debug("No matches for letters or digit")
            return

        letter_occurences = total_occurences.most_common()
        # we create a list of the letter with the same occurences of the
        # first most frequent letter found
        most_common = list(filter(lambda x: x[1] == letter_occurences[0][1],
                                  letter_occurences))
        result = ""
        # concatenate the results
        for letter in most_common:
            result = result + str(letter[0]) + " "

        return result.rstrip()

    def _avg_letters(self, text_wrapper, precision=1):
        """
        The method calculates the average number of letters
        dividing the total numbers of letter found by the
        total number of words found in a text.
        The result has "n" number of decimal digit according
        to the parameter passed.
        args:
            text_wrapper: the text to parse
            precision: define the number of decimal digits
        """
        avg = 0
        tot_words = self.get_total_words(text_wrapper)
        if tot_words == 0:
            self.log.debug("No words found")
            return 0
        text_wrapper.seek(0)
        tot_letters = self.get_total_letters(text_wrapper)
        avg = decimal.Decimal((tot_letters / tot_words))

        return float(round(avg, precision)) \
                     if precision > 0 else float(int(avg))

    def _count_alphanumeric(self, text_wrapper):
        """
        This method calculates the number of letters and number considering
        the unicode point for letters and digits.
        args:
            text_wrapper: text to parse
        """
        total_alphanumeric = 0
        for line in text_wrapper:
            total_alphanumeric += len(regex.findall(r'[\p{L}\p{N}]', line))

        return total_alphanumeric

    def _count_words(self, text_wrapper):
        """
        Giving a text it returns the number of word found.
        args:
            test_wrapper: text to parse
        """
        total_words = 0
        for line in text_wrapper:
            # we exclude words formed just by signs
            # (no unicode point letter or digit)
            words_list = list(
                            filter(lambda x: regex.findall(r'[\p{L}\p{N}]', x),
                                   line.split()))
            total_words += len(words_list)

        return total_words

    def _count_lines(self, text_wrapper):
        """
        Giving a text it returns the number of line found
        args:
            text_wrapper: the test to parse
        """
        lines = -1
        for lines, _ in enumerate(text_wrapper):
            pass
        return lines + 1
