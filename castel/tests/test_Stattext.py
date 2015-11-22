import io
from unittest import TestCase
from unittest import mock

from castel.drivers.stattext import Stattext

class TestStattext(TestCase):
    def setUp(self):
        self.stattext = Stattext()

    @mock.patch.object(Stattext, '_count_words')
    def test_total_words(self, mock_count_words):
        self.stattext.total_words = None
        self.stattext.get_total_words("fake")
        mock_count_words.assert_called_with("fake")

    @mock.patch.object(Stattext, '_count_words')
    def test_count_words_no_called(self, mock_count_words):
        self.stattext.total_words = 21
        self.stattext.get_total_words("fake")
        self.assertFalse(mock_count_words.called)

    @mock.patch.object(Stattext, '_count_lines')
    def test_total_lines(self, mock_count_lines):
        self.stattext.total_lines = None
        self.stattext.get_total_lines("fake")
        mock_count_lines.assert_called_with("fake")

    @mock.patch.object(Stattext, '_count_lines')
    def test_count_lines_no_called(self, mock_count_lines):
        self.stattext.total_lines = 21
        self.stattext.get_total_lines("fake")
        self.assertFalse(mock_count_lines.called)

    @mock.patch.object(Stattext, '_count_alphanumeric')
    def test_total_letters(self, mock_count_letters):
        self.stattext.total_letters = None
        self.stattext.get_total_letters("fake")
        mock_count_letters.assert_called_with("fake")

    @mock.patch.object(Stattext, '_count_alphanumeric')
    def test_count_letters_no_called(self, mock_count_letters):
        self.stattext.total_letters = 21
        self.stattext.get_total_letters("fake")
        self.assertFalse(mock_count_letters.called)

    @mock.patch.object(Stattext, '_avg_letters')
    def test_avg_letters_per_word(self, mock_avg_letters):
        self.stattext.avg_letters_per_word = None
        self.stattext.get_avg_letters_per_word("fake")
        mock_avg_letters.assert_called_with("fake", precision=1)

    @mock.patch.object(Stattext, '_avg_letters')
    def test_avg_letters_no_called(self, mock_avg_letters):
        self.stattext.avg_letters_per_word = 21
        self.stattext.get_avg_letters_per_word("fake")
        self.assertFalse(mock_avg_letters.called)

class TestAvgLetterForWord(TestCase):
    def setUp(self):
        self.stattext = Stattext()

    def do_count_letters(self, text):
        file_content = io.StringIO(text)
        return self.stattext._count_alphanumeric(file_content)

    def do_avg_letters(self, text, precision=1):
        file_content = io.StringIO(text)
        return self.stattext._avg_letters(file_content, precision)

    def test_count_letters(self):
        text =  "This is a good test"
        result = self.do_count_letters(text)
        expected = 15
        self.assertEqual(result, expected)

    def test_count_letters_multi_line(self):
        text =  "This\n is \na good test\n\n\n"
        result = self.do_count_letters(text)
        expected = 15
        self.assertEqual(result, expected)

    def test_count_letters_ignoring_signs(self):
        text = "  Hello, | World!! ...\n Is a ''good day''"
        result = self.do_count_letters(text)
        expected = 20
        self.assertEqual(result, expected)

    def test_count_letters_empty_line(self):
        text = ""
        result = self.do_count_letters(text)
        expected = 0
        self.assertEqual(result, expected)

    def test_count_letters_ignore_single_quote(self):
        text = "I'm"
        result = self.do_count_letters(text)
        expected = 2
        self.assertEqual(result, expected)

    def test_count_digit_as_letters(self):
        text ="123"
        result = self.do_count_letters(text)
        expected = 3
        self.assertEqual(result, expected)

    def test_avg_letter_single_line(self):
        text =  "This is a good test"
        result = self.do_avg_letters(text)
        expected = 3.0
        self.assertEqual(result, expected)

    def test_avg_letter_multi_line(self):
        text =  "This is a good\n test\n\n"
        result = self.do_avg_letters(text)
        expected = 3.0
        self.assertEqual(result, expected)

    def test_avg_unicode(self):
        text = "Thíś íś ṕŕéttӳ fúń.\n "
        expected = 3.8
        result = self.do_avg_letters(text)
        self.assertEqual(result, expected)

    def test_avg_no_decimal(self):
        text = "Thíś íś ṕŕéttӳ fúń.\n "
        expected = 3
        result = self.do_avg_letters(text, precision=0)
        self.assertEqual(result, expected)

    def test_avg_emtpy_file(self):
        text = ""
        expected = 0
        result = self.do_avg_letters(text)
        self.assertEqual(result, expected)


class TestCountWords(TestCase):
    def setUp(self):
        self.stattext = Stattext()

    def do_count_words(self, text):
        file_content = io.StringIO(text)
        return self.stattext._count_words(file_content)

    def test_count_on_single_line(self):
        text = "This is a test"
        result = self.do_count_words(text)
        expected = 4
        self.assertEqual(result, expected)

    def test_count_on_multi_line(self):
        text = "This is a\n test"
        result = self.do_count_words(text)
        expected = 4
        self.assertEqual(result, expected)

    def test_count_number_as_word(self):
        text = "The 4 is counted as a word"
        result = self.do_count_words(text)
        expected = 7
        self.assertEqual(result, expected)

    def test_ignore_double_spaces(self):
        text = "this text  has \n spaces"
        result = self.do_count_words(text)
        expected = 4
        self.assertEqual(result, expected)

    def test_words_with_single_quote(self):
        text = "it's a quote"
        result = self.do_count_words(text)
        expected = 3
        self.assertEqual(result, expected)

    def test_words_with_hyphen(self):
        text = "single-word"
        result = self.do_count_words(text)
        expected = 1
        self.assertEqual(result, expected)

    def test_empty_file(self):
        text = ""
        result = self.do_count_words(text)
        expected = 0
        self.assertEqual(result, expected)

    def test_empty_line(self):
        text = "\n"
        result = self.do_count_words(text)
        expected = 0
        self.assertEqual(result, expected)

    def test_space(self):
        text = " "
        result = self.do_count_words(text)
        expected = 0
        self.assertEqual(result, expected)

    def test_ignore_punctuaction(self):
        text = "this is awesome !!!"
        result = self.do_count_words(text)
        expected = 3
        self.assertEqual(result, expected)

    def test_unicode(self):
        text = "Thíś íś ṕŕéttӳ fúń.\n And more, fun here"
        result = self.do_count_words(text)
        expected = 8
        self.assertEqual(result, expected)

    def test_dots_word(self):
        text = "...just saying"
        result = self.do_count_words(text)
        expected = 2
        self.assertEqual(result, expected)

    def test_word_with_pipe(self):
       text = "this|is a strange word"
       result = self.do_count_words(text)
       expected = 4
       self.assertEqual(result, expected)

    def test_only_signs(self):
        text = "... ,, : !! | \ +-'"
        result = self.do_count_words(text)
        expected = 0
        self.assertEqual(result, expected)


class TestFrequentLetter(TestCase):
    def setUp(self):
        self.stattext = Stattext()

    def do_most_common_letter(self, text):
        file_content = io.StringIO(text)
        return self.stattext.most_common_letter(file_content)

    def test_ascii_count(self):
        text = "a"*2 + "b"*5
        result = self.do_most_common_letter(text)
        expected = "b"
        self.assertEqual(result, expected)

    def test_ascii_count_multi_line(self):
        text = "a"*2 + "b"*5 +"\n"+"a"*5
        result = self.do_most_common_letter(text)
        expected = "a"
        self.assertEqual(result, expected)

    def test_ignore_digits(self):
        text = "a1111\n232"
        result = self.do_most_common_letter(text)
        expected = "a"
        self.assertEqual(result, expected)

    def test_empty_file(self):
        text = ""
        result = self.do_most_common_letter(text)
        self.assertIsNone(result)

    def test_empty_line(self):
        text = "\n\n\n"
        result = self.do_most_common_letter(text)
        self.assertIsNone(result)

    def test_file_only_spaces(self):
        text = "   \n   \r\n"
        result = self.do_most_common_letter(text)
        self.assertIsNone(result)

    def test_ignore_punctuaction(self):
        text = "hello, world:\n?!:;.'"
        result = self.do_most_common_letter(text)
        expected = "l"
        self.assertEqual(result, expected)

    def test_upper_case_ignored(self):
        text = "BBb"
        result = self.do_most_common_letter(text)
        expected = "b"
        self.assertEqual(result, expected)

    def test_many_most_common_letter(self):
        text = "test is done"
        result = self.do_most_common_letter(text)
        expected = ['e','s','t']
        self.assertEqual(sorted(result.replace(" ","")), expected)

    def test_unicode_text(self):
        text = "Thíś íś ṕŕéttӳ fúń"
        result = self.do_most_common_letter(text)
        expected = "t"
        self.assertEqual(result, expected)


class TestCountLines(TestCase):
    def setUp(self):
        self.stattext = Stattext()

    def do_count_lines(self, text):
        file_content = io.StringIO(text)
        return self.stattext._count_lines(file_content)

    def test_empty_file(self):
        result = self.do_count_lines("")
        expected = 0
        self.assertEqual(result, expected)

    def test_single_line(self):
        text = "This is my line"
        result = self.do_count_lines(text)
        expected = 1
        self.assertEqual(result, expected)

    def test_single_line_no_chars(self):
        text = "\n"
        result = self.do_count_lines(text)
        expected = 1
        self.assertEqual(result, expected)

    def test_single_line_space_char(self):
        text = " "
        result = self.do_count_lines(text)
        expected = 1
        self.assertEqual(result, expected)

    def test_multi_lines(self):
        text = "This \n is \n a 4\nlines "
        result = self.do_count_lines(text)
        expected = 4
        self.assertEqual(result, expected)

    def test_multi_empty_lines(self):
        text = "\n\n\n"
        result = self.do_count_lines(text)
        expected = 3
        self.assertEqual(result, expected)

    def test_escape_char(self):
        text = "This \n is \n a 3\\nlines"
        result = self.do_count_lines(text)
        expected = 3
        self.assertEqual(result, expected)
