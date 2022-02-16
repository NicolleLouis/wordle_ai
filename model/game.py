import random

from model.step import Step
from service.ai_service import AIService
from service.file_service import FileService


class Game:
    current_word_file = "file/current_words.txt"
    all_word_file = "larousse/correct_words.txt"

    def __init__(self, auto=False, verbose=False):
        self.reset_file()
        self.turn_number = 0
        self.is_victory = False

        self.auto = auto
        if self.auto:
            self.solution = self.choose_random_word()
        else:
            self.solution = None

        self.verbose = self.should_be_verbose(verbose)

        self.run()

    def run(self):
        while self.should_continue():
            self.step()
        self.conclude()

    def reset_file(self):
        words = FileService.read_lines(self.all_word_file)
        FileService.write_words_to_file(self.current_word_file, words)

    def step(self):
        step = Step(
            solution=self.solution,
            answer=self.choose_word(),
            game=self,
        )
        self.turn_number += 1

        self.is_victory = step.is_victory

    def should_be_verbose(self, verbose):
        if verbose:
            return True
        else:
            if not self.auto:
                return True
        return False

    def should_continue(self):
        remaining_words = FileService.number_of_line_in_file(self.current_word_file)
        if remaining_words == 0:
            raise Exception("No solution was found")
        return not self.is_victory

    def choose_word(self):
        if self.turn_number == 0:
            return "rates"
        words_remaining = len(FileService.read_lines(self.current_word_file))
        if words_remaining > 100:
            return self.choose_precomputed_words()
        return AIService.compute_best_solution(self.current_word_file)

    def choose_random_word(self):
        words = FileService.read_lines(self.current_word_file)
        return random.choice(words)

    def choose_precomputed_words(self):
        chosen_words = [
            "clerc",
            "engin",
        ]
        words_remaining = FileService.read_lines(self.current_word_file)
        for chosen_word in chosen_words:
            if chosen_word in words_remaining:
                return chosen_word

    def conclude(self):
        solution = FileService.read_lines(self.current_word_file)[0]
        if self.verbose:
            print("#####")
            print(f"Solution is: {solution}")
            print(f"Solution found in: {self.turn_number} turns")
