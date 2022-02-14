from service.file_service import FileService
from .word import Word
from .word_comparison import WordComparison


class Step:
    legal_answers = ["0", "1", "2"]

    def __init__(self, answer, file=None):
        self.new_constraint = None
        self.file = file

        self.answer = answer
        print(f"Solution proposée: {self.answer}")

        self.comparison = input("Response:")
        self.input_validator()

        self.update_file()

    def input_validator(self):
        if len(self.comparison) != WordComparison.word_length:
            raise Exception(f"Response should be of same length as word")
        for character in self.comparison:
            if character not in Step.legal_answers:
                raise Exception(f"Character is not legal: {character}")

    def update_file(self):
        words = FileService.read_lines(self.file)
        updated_words = list(
            filter(
                lambda word: Word(self.answer).compare_with_word(Word(word)) == self.comparison,
                words
            )
        )
        FileService.write_words_to_file(self.file, updated_words)
