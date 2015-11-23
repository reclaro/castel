from abc import ABCMeta, abstractmethod


class Engine(metaclass=ABCMeta):
    """Abstract class for the definition of the Engine driver.

    This class is an abstract class which defines the four main
    method required to perform the requested statistics.
    The class implements the method to open the file.
    """

    def open_file(self, file_name, encoding="utf-8"):
        return open(file_name, encoding=encoding)

    @abstractmethod
    def get_total_lines(self, text_wrapper):
        pass

    @abstractmethod
    def get_total_words(self, text_wrapper):
        pass

    @abstractmethod
    def most_common_letter(self, text_wrapper):
        pass

    @abstractmethod
    def get_avg_letters_per_word(self, text_wrapper):
        pass
