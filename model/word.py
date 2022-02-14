class Word:
    dead_character = "@"

    def __init__(self, word):
        self.word = word
        self.chars = self.split()

    def split(self):
        return [char for char in self.word]

    def compare_with_word(self, other_word):
        comparison = ["0" for _ in range(len(self.word))]
        word_copy = self.chars.copy()
        other_word_copy = other_word.chars.copy()
        if len(other_word.word) != len(self.word):
            raise Exception("Not the same length")
        for index in range(len(word_copy)):
            if other_word_copy[index] == word_copy[index]:
                comparison[index] = "2"
                word_copy[index] = self.dead_character
                other_word_copy[index] = self.dead_character
        for index in range(len(word_copy)):
            if word_copy[index] != self.dead_character:
                if word_copy[index] in other_word_copy:
                    comparison[index] = "1"

        return "".join(comparison)
