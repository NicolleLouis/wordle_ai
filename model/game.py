import random

from model.step import Step
from service.file_service import FileService


class Game:
    current_word_file = "file/current_words.txt"
    all_word_file = "larousse/correct_words.txt"

    def __init__(self):
        self.reset_file()
        self.turn_number = 0
        self.run()

    def run(self):
        while not self.should_stop():
            self.step()
        self.conclude()

    def reset_file(self):
        words = FileService.read_lines(self.all_word_file)
        FileService.write_words_to_file(self.current_word_file, words)

    def step(self):
        print("######")
        print(f"Turn number: {self.turn_number}")
        Step(
            answer=self.choose_word(),
            file=self.current_word_file,
        )
        remaining_words = FileService.number_of_line_in_file(self.current_word_file)
        print(f"Remaining words: {remaining_words}")

        self.turn_number += 1

    def should_stop(self):
        remaining_words = FileService.number_of_line_in_file(self.current_word_file)
        return remaining_words <= 1

    def choose_word(self):
        words = FileService.read_lines(self.current_word_file)
        return random.choice(words)

    def conclude(self):
        remaining_words = FileService.number_of_line_in_file(self.current_word_file)
        if remaining_words == 0:
            raise Exception("No solution was found")
        solution = FileService.read_lines(self.current_word_file)[0]
        print(f"Solution is: {solution}")
        print(f"Solution found in: {self.turn_number} turns")
