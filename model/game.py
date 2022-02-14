import random

from model.step import Step
from service.file_service import FileService


class Game:
    current_word_file = "file/current_words.txt"
    all_word_file = "larousse/correct_words.txt"

    def __init__(self, auto=False):
        self.reset_file()
        self.turn_number = 0
        self.is_victory = False

        self.auto = auto
        if self.auto:
            self.solution = self.choose_word()
        self.run()

    def run(self):
        while self.should_continue():
            self.step()
        self.conclude()

    def reset_file(self):
        words = FileService.read_lines(self.all_word_file)
        FileService.write_words_to_file(self.current_word_file, words)

    def step(self):
        if self.auto:
            step = self.step_auto()
        else:
            step = self.step_manual()
        self.turn_number += 1

        self.is_victory = step.is_victory

    def step_auto(self):
        step = Step(
            solution=self.solution,
            answer=self.choose_word(),
            file=self.current_word_file,
        )
        return step

    def step_manual(self):
        print("######")
        print(f"Turn number: {self.turn_number}")
        step = Step(
            answer=self.choose_word(),
            file=self.current_word_file,
        )
        remaining_words = FileService.number_of_line_in_file(self.current_word_file)
        print(f"Remaining words: {remaining_words}")
        return step

    def should_continue(self):
        remaining_words = FileService.number_of_line_in_file(self.current_word_file)
        if remaining_words == 0:
            raise Exception("No solution was found")
        return not self.is_victory

    def choose_word(self):
        words = FileService.read_lines(self.current_word_file)
        return random.choice(words)

    def conclude(self):
        solution = FileService.read_lines(self.current_word_file)[0]
        print(f"Solution is: {solution}")
        print(f"Solution found in: {self.turn_number} turns")
