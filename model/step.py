from service.file_service import FileService
from .word import Word
from .word_comparison import WordComparison


class Step:
    legal_answers = ["0", "1", "2"]

    def __init__(self, answer, solution=None, game=None):
        self.comparison = None
        self.new_constraint = None
        self.solution = solution
        self.is_victory = False
        self.game = game

        self.answer = answer

        self.prelude()
        self.generate_comparison()
        self.update_is_victory()
        self.update_file()
        self.conclude()

    def prelude(self):
        if self.game.verbose:
            print("######")
            print(f"Turn number: {self.game.turn_number}")
            print(f"Solution proposée: {self.answer}")

    def conclude(self):
        if self.game.verbose:
            remaining_words = FileService.number_of_line_in_file(self.game.current_word_file)
            print(f"Remaining words: {remaining_words}")

    def update_is_victory(self):
        if "0" not in self.comparison and "1" not in self.comparison:
            self.is_victory = True
    
    def generate_comparison(self):
        if self.solution is None:
            self.comparison = input("Response:")
            self.input_validator()
        else:
            self.comparison = Word(self.answer).compare_with_word(Word(self.solution))

    def input_validator(self):
        if len(self.comparison) != WordComparison.word_length:
            raise Exception(f"Response should be of same length as word")
        for character in self.comparison:
            if character not in Step.legal_answers:
                raise Exception(f"Character is not legal: {character}")

    def update_file(self):
        words = FileService.read_lines(self.game.current_word_file)
        updated_words = list(
            filter(
                lambda word: Word(self.answer).compare_with_word(Word(word)) == self.comparison,
                words
            )
        )
        FileService.write_words_to_file(self.game.current_word_file, updated_words)
