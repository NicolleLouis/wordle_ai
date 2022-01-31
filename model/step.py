from service.file_service import FileService
from .word_constraint import WordConstraint


class Step:
    legal_answers = ["0", "1", "2"]

    def __init__(self, word, word_constraint=None, file=None):
        self.new_constraint = None
        self.file = file
        self.word_constraint = WordConstraint(
            banned_letters=None,
            letters_potential_position=None
        )
        if word_constraint is not None:
            self.word_constraint = word_constraint

        self.word = word
        self.data_validator()
        print(self.word)

        self.user_input = input("Response:")
        self.input_validator()

        self.compute_constraint()
        self.update_file()

    def data_validator(self):
        if type(self.word_constraint) is not WordConstraint:
            raise Exception(f"Word Constraint has a wrong type: {type(self.word_constraint)}")
        if not self.word_constraint.is_word_legal(self.word):
            raise Exception('Word does not match current constraint')

    def input_validator(self):
        if len(self.user_input) != WordConstraint.word_length:
            raise Exception(f"Response should be of same length as word")
        for character in self.user_input:
            if character not in Step.legal_answers:
                raise Exception(f"Character is not legal: {character}")

    def compute_constraint(self):
        banned_letters = []
        letters_potential_position = {}
        for index in range(WordConstraint.word_length):
            if self.user_input[index] == "0":
                banned_letters.append(self.word[index])
            if self.user_input[index] == "2":
                letters_potential_position[self.word[index]] = [index]
            if self.user_input[index] == "1":
                letters_potential_position[self.word[index]] = list(WordConstraint.legal_position)
                letters_potential_position[self.word[index]].remove(index)

        self.new_constraint = WordConstraint(
            banned_letters=banned_letters,
            letters_potential_position=letters_potential_position
        )
        self.word_constraint.sum_constraint(self.new_constraint)

    def update_file(self):
        words = FileService.read_lines(self.file)
        updated_words = list(
            filter(
                lambda word: self.word_constraint.is_word_legal(word),
                words
            )
        )
        FileService.write_words_to_file(self.file, updated_words)
