from service.file_service import FileService


class GenerateLarousse:
    all_french_word_file = "larousse/all_french_word.txt"
    good_length_words_file = "larousse/good_length.txt"
    correct_words_file = "larousse/correct_words.txt"

    @staticmethod
    def clean_word(word):
        replacements = [
            ("é", "e"),
            ("è", "e"),
            ("ê", "e"),
            ("î", "i"),
            ("ï", "i"),
            ("û", "u"),
            ("ù", "u"),
            ("â", "a"),
            ("à", "a"),
            ("ô", "o"),
            ("ç", "c"),
            ("œ", "oe"),
        ]
        word = word.lower()
        for replacement in replacements:
            old, new = replacement
            word = word.replace(old, new)
        return word

    @classmethod
    def filter_letter(cls, length):
        all_words_file = open(cls.all_french_word_file, encoding='latin1')
        all_words = all_words_file.read().splitlines()
        all_words_file.close()
        cleaned_word = list(
            map(
                lambda word: cls.clean_word(word),
                all_words
            )
        )
        good_length_letter_words = list(
            filter(
                lambda word: len(word) == length,
                cleaned_word
            )
        )
        FileService.write_words_to_file(cls.correct_words_file, good_length_letter_words)

    @classmethod
    def remove_duplicate(cls):
        words = FileService.read_lines(cls.correct_words_file)
        no_duplicate_words = list(set(words))
        FileService.write_words_to_file(cls.correct_words_file, no_duplicate_words)
