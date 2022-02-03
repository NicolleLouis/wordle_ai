from model.word_constraint import WordConstraint
from service.file_service import FileService


class GameCheat:
    current_word_file = "file/current_words.txt"
    all_word_file = "larousse/correct_words.txt"

    def __init__(self):
        self.reset_file()
        self.word_constraint_number = 0
        self.word_constraint = self.input()

    def reset_file(self):
        words = FileService.read_lines(self.all_word_file)
        FileService.write_words_to_file(self.current_word_file, words)

    def input(self):
        self.word_constraint_number = int(input("Nombre de contraintes manuelles :"))
        word_constraint = WordConstraint()
        for _ in range(self.word_constraint_number):
            word = input("Mot choisi: ")
            constraint = input("Résultat: ")
            word_constraint = self.compute_constraint(
                word,
                constraint,
                word_constraint
            )
            self.update_file(word_constraint)
            remaining_words = FileService.number_of_line_in_file(self.current_word_file)
            print(f"Remaining words: {remaining_words}")
        return word_constraint

    @staticmethod
    def compute_constraint(word, constraint, word_constraint):
        banned_letters = []
        letters_potential_position = {}
        for index in range(WordConstraint.word_length):
            if constraint[index] == "0":
                banned_letters.append(word[index])
            if constraint[index] == "2":
                letters_potential_position[word[index]] = [index]
            if constraint[index] == "1":
                letters_potential_position[word[index]] = list(WordConstraint.legal_position)
                letters_potential_position[word[index]].remove(index)

        new_constraint = WordConstraint(
            banned_letters=banned_letters,
            letters_potential_position=letters_potential_position
        )
        word_constraint.sum_constraint(new_constraint)
        return word_constraint

    def update_file(self, word_constraint):
        words = FileService.read_lines(self.current_word_file)
        updated_words = list(
            filter(
                lambda word: word_constraint.is_word_legal(word),
                words
            )
        )
        FileService.write_words_to_file(self.current_word_file, updated_words)
