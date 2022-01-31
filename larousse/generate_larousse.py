from service.file_service import FileService


class GenerateLarousse:
    all_french_word_file = "larousse/all_french_word.txt"
    five_letters_words_file = "larousse/five_letters.txt"
    correct_words_file = "larousse/correct_words.txt"

    @staticmethod
    def clean_word(word):
        return word.lower()

    @classmethod
    def filter_five_letter(cls):
        all_words_file = open(cls.all_french_word_file, errors="ignore")
        all_words = all_words_file.read().splitlines()
        all_words_file.close()
        five_letter_words = list(
            filter(
                lambda word: len(word) == 5,
                all_words
            )
        )
        FileService.write_words_to_file(cls.five_letters_words_file, five_letter_words)

    @classmethod
    def clean_five_letter_file(cls):
        five_letter_words_file = open(cls.five_letters_words_file, errors="ignore")
        five_letters_words = five_letter_words_file.read().splitlines()
        five_letter_words_file.close()
        cleaned_word = list(
            map(
                lambda word: cls.clean_word(word),
                five_letters_words
            )
        )
        FileService.write_words_to_file(cls.correct_words_file, cleaned_word)

    @classmethod
    def remove_duplicate(cls):
        words = FileService.read_lines(cls.correct_words_file)
        no_duplicate_words = list(set(words))
        FileService.write_words_to_file(cls.correct_words_file, no_duplicate_words)
