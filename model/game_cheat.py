from model.word import Word
from service.file_service import FileService


class GameCheat:
    current_word_file = "file/current_words.txt"
    all_word_file = "larousse/correct_words.txt"

    def __init__(self):
        self.reset_file()
        self.word_constraint_number = 0
        self.input()

    def reset_file(self):
        words = FileService.read_lines(self.all_word_file)
        FileService.write_words_to_file(self.current_word_file, words)

    def input(self):
        self.word_constraint_number = int(input("Nombre de contraintes manuelles :"))
        for _ in range(self.word_constraint_number):
            word = input("Mot choisi: ")
            comparison = input("Résultat: ")
            self.update_file(word, comparison)
            remaining_words = FileService.number_of_line_in_file(self.current_word_file)
            print(f"Remaining words: {remaining_words}")

    def update_file(self, answer, comparison):
        words = FileService.read_lines(self.current_word_file)
        updated_words = list(
            filter(
                lambda word: Word(answer).compare_with_word(Word(word)) == comparison,
                words
            )
        )
        FileService.write_words_to_file(self.current_word_file, updated_words)
