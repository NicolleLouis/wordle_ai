from model.game import Game
from service.file_service import FileService


class Batch:
    game_length_file = "file/game_length.txt"

    def __init__(self, number_of_run=1000):
        self.number_of_run = number_of_run

        self.reset_file()
        self.run()

    def run(self):
        for _ in range(self.number_of_run):
            self.step()
        self.conclude()

    def reset_file(self):
        FileService.clean_file(self.game_length_file)

    def step(self):
        game = Game(auto=True)
        FileService.append_line_to_file(self.game_length_file, str(game.turn_number))

    def conclude(self):
        raw_turn_number = FileService.read_lines(self.game_length_file)
        raw_turn_number = list(
            map(
                lambda number_as_str: int(number_as_str),
                raw_turn_number
            )
        )

        average = sum(raw_turn_number)/len(raw_turn_number)
        print(f"Average result is: {str(average)} turns")

        for index in range(10):
            if index != 0:
                occurences = raw_turn_number.count(index)
                print(f"Solved in {index} turns: {occurences}")
