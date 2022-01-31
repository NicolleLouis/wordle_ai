class FileService:
    @staticmethod
    def clean_file(file):
        open(file, 'w').close()

    @classmethod
    def write_words_to_file(cls, file, words):
        cls.clean_file(file)
        file = open(file, "a")
        for word in words:
            file.write(word)
            file.write("\n")
        file.close()

    @classmethod
    def number_of_line_in_file(cls, file):
        return len(cls.read_lines(file))

    @staticmethod
    def read_lines(file):
        file = open(file)
        return file.read().splitlines()
