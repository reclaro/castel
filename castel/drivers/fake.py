from castel.drivers.engine import Engine

class Fakeengine(Engine):
    # This is a fake engine class used in the tests
    def get_total_words(self, text_wrapper):
            return 1

    def get_total_lines(self, text_wrapper):
        return 2

    def get_avg_letters_per_word(self, test_wrapper):
        return 2

    def most_common_letter(self, text_wrapper):
        return 'a'
