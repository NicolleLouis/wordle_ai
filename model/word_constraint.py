from service.file_service import FileService


class WordConstraint:
    word_length = len(FileService.read_lines('larousse/correct_words.txt')[0])
    legal_position = range(word_length)

    def __init__(
            self,
            banned_letters=None,
            letters_potential_position=None,
    ):
        self.banned_letters = []
        if banned_letters is not None:
            self.banned_letters = banned_letters
        self.letters_potential_position = {}
        if letters_potential_position is not None:
            self.letters_potential_position = letters_potential_position
        self.data_validator()

    def __str__(self):
        return f"""
        banned letters: {self.banned_letters}
        letters potential position: {self.letters_potential_position}
        """

    def __eq__(self, other):
        if type(other) != WordConstraint:
            raise Exception(f'Can only compare WordConstraint and not: {type(other)}')
        if set(self.banned_letters) != set(other.banned_letters):
            return False
        return self.letters_potential_position == other.letters_potential_position

    def data_validator(
            self,
    ):
        if type(self.banned_letters) is not list:
            raise Exception(f'Banned letters should be a list: {self.banned_letters}')
        for banned_letter in self.banned_letters:
            if type(banned_letter) is not str:
                raise Exception(f'Each Banned letter should be a string: {banned_letter}')
            if len(banned_letter) != 1:
                raise Exception(
                    f'Each Banned letter should be a single character: {banned_letter}'
                )
        if type(self.letters_potential_position) is not dict:
            raise Exception(f'Letters potential position should be a dict: {self.letters_potential_position}')
        for letter_potential_position in self.letters_potential_position:
            if type(letter_potential_position) is not str:
                raise Exception(f'Letter potential position should be a string: {letter_potential_position}')
            if len(letter_potential_position) != 1:
                raise Exception(
                    f'Letter potential position should be a single character: {letter_potential_position}'
                )
            if letter_potential_position in self.banned_letters:
                raise Exception(
                    f'A letter can\'t be both potential and banned: {letter_potential_position}'
                )
            potential_position = self.letters_potential_position[letter_potential_position]
            if type(potential_position) is not list:
                raise Exception(
                    f'Potential position should be a list: {potential_position}'
                )
            if len(potential_position) == 0:
                raise Exception(
                    f'Potential position should have at least 1 possibility: {potential_position}'
                )
            for position in potential_position:
                if position not in WordConstraint.legal_position:
                    raise Exception(
                        f'Position must be legal: {position}'
                    )

    def sum_constraint(
            self,
            word_constraint
    ):
        if type(word_constraint) != WordConstraint:
            raise Exception(
                f"Sum can only be perform with WordConstraint and not: {type(word_constraint)}"
            )
        self.banned_letters.extend(word_constraint.banned_letters)
        for letter_potential_position in word_constraint.letters_potential_position:
            if letter_potential_position not in self.letters_potential_position:
                self.letters_potential_position[letter_potential_position] = \
                    word_constraint.letters_potential_position[letter_potential_position]
            else:
                new_potential_position = []
                for position in WordConstraint.legal_position:
                    if position in self.letters_potential_position[letter_potential_position] and position in \
                            word_constraint.letters_potential_position[letter_potential_position]:
                        new_potential_position.append(position)
                self.letters_potential_position[letter_potential_position] = new_potential_position
        self.data_validator()

    def is_word_legal(self, word):
        if type(word) is not str:
            raise Exception(f"word should be a str: {word}")
        if len(word) != self.word_length:
            return False
        for banned_letter in self.banned_letters:
            if banned_letter in word:
                return False
        for letter in self.letters_potential_position:
            if letter not in word:
                return False
            occurrence = word.count(letter)
            start = 0
            for _i in range(occurrence):
                if word.find(letter, start) not in self.letters_potential_position[letter]:
                    return False
                start = word.find(letter, start) + 1
        return True
