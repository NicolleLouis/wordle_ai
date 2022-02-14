from service.file_service import FileService


class WordComparison:
    word_length = len(FileService.read_lines('larousse/correct_words.txt')[0])

    def __init__(
            self,
            comparison,
    ):
        self.comparison = str(comparison)

    def __str__(self):
        return f"Comparison: {self.comparison}"

    def __eq__(self, other):
        if type(other) != WordComparison:
            raise Exception(f'Can only compare WordComparison and not: {type(other)}')
        if self.comparison != other.comparison:
            return False
        return True

