from model.word import Word
from service.file_service import FileService


class AIService:
    @classmethod
    def compute_best_solution(cls, file):
        words_and_efficiency = cls.compute_solution_efficiency(file)
        return cls.extract_optimal_solution(words_and_efficiency)

    @classmethod
    def compute_solution_efficiency(cls, file):
        words_and_efficiency = {}
        possible_words = FileService.read_lines(file)
        for possible_word in possible_words:
            words_and_efficiency[possible_word] = cls.compute_average_next_turn_number_of_legal_words_for_answer(
                answer=possible_word,
                file=file
            )
        return words_and_efficiency

    @staticmethod
    def extract_optimal_solution(words_and_efficiency):
        minimal_score = min(
            list(
                map(
                    lambda item: item[1],
                    words_and_efficiency.items()
                )
            )
        )
        for key in words_and_efficiency:
            if words_and_efficiency[key] == minimal_score:
                return key

    @staticmethod
    def compute_average_next_turn_number_of_legal_words_for_answer(answer, file):
        next_turn_number_of_legal_words = []
        possible_words = FileService.read_lines(file)
        for solution in possible_words:
            comparison = Word(solution).compare_with_word(Word(answer))
            next_turn_legal_words = list(
                filter(
                    lambda word: Word(answer).compare_with_word(Word(word)) == comparison,
                    possible_words
                )
            )
            next_turn_number_of_legal_words.append(len(next_turn_legal_words))
        return sum(next_turn_number_of_legal_words)/len(next_turn_number_of_legal_words)
