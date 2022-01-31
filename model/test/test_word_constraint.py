import pytest

from ..word_constraint import WordConstraint


class TestWordConstraint:
    @pytest.mark.parametrize(
        "banned_letters,letters_potential_position",
        [
            ("a", {'d': [0, 1, 2, 3, 4], 'e': [1]}),
            (["a", "b", "c"], "a"),
            ([1, "b", "c"], {'d': [0, 1, 2, 3, 4], 'e': [1]}),
            (["ab", "b", "c"], {'d': [0, 1, 2, 3, 4], 'e': [1]}),
            (["a", "b", "c"], {1: [0, 1, 2, 3, 4], 'e': [1]}),
            (["a", "b", "c"], {'da': [0, 1, 2, 3, 4], 'e': [1]}),
            (["a", "b", "c"], {'a': [0, 1, 2, 3, 4], 'e': [1]}),
            (["a", "b", "c"], {'d': 'a', 'e': [1]}),
            (["a", "b", "c"], {'d': [], 'e': [1]}),
            (["a", "b", "c"], {'d': [0, 1, 2, 3, 4, 5], 'e': [1]}),
        ]
    )
    def test_data_validator_case_fail(self, banned_letters, letters_potential_position):
        with pytest.raises(Exception):
            WordConstraint(
                banned_letters=banned_letters,
                letters_potential_position=letters_potential_position
            )

    def test_data_validator_case_success(self):
        word_constraint = WordConstraint(
            banned_letters=["a", "b", "c"],
            letters_potential_position={'d': [0, 1, 2, 3, 4], 'e': [1]}
        )
        assert type(word_constraint) == WordConstraint

    def test_str(self):
        word_constraint = WordConstraint(
            banned_letters=["a", "b", "c"],
            letters_potential_position={'d': [0, 1, 2, 3, 4], 'e': [1]}
        )
        expected_output = """
        banned letters: ['a', 'b', 'c']
        letters potential position: {'d': [0, 1, 2, 3, 4], 'e': [1]}
        """
        assert str(word_constraint) == expected_output

    def test_sum_constraint_case_banned_letters(
            self,
    ):
        word_constraint_1 = WordConstraint(
            banned_letters=["a"],
            letters_potential_position=None
        )
        word_constraint_2 = WordConstraint(
            banned_letters=["b"],
            letters_potential_position=None
        )
        expected_sum = WordConstraint(
            banned_letters=["a", "b"],
            letters_potential_position=None
        )
        word_constraint_1.sum_constraint(word_constraint_2)
        assert word_constraint_1 == expected_sum

    def test_sum_constraint_case_distinct_letters_potential_position(
            self,
    ):
        word_constraint_1 = WordConstraint(
            banned_letters=None,
            letters_potential_position={"a": [1]}
        )
        word_constraint_2 = WordConstraint(
            banned_letters=None,
            letters_potential_position={"b": [1]}
        )
        expected_sum = WordConstraint(
            banned_letters=None,
            letters_potential_position={"a": [1], "b": [1]}
        )
        word_constraint_1.sum_constraint(word_constraint_2)
        assert word_constraint_1 == expected_sum

    def test_sum_constraint_case_same_letters_potential_position(
            self,
    ):
        word_constraint_1 = WordConstraint(
            banned_letters=None,
            letters_potential_position={"a": [1, 2, 3]}
        )
        word_constraint_2 = WordConstraint(
            banned_letters=None,
            letters_potential_position={"a": [3, 4]}
        )
        expected_sum = WordConstraint(
            banned_letters=None,
            letters_potential_position={"a": [3]}
        )
        word_constraint_1.sum_constraint(word_constraint_2)
        assert word_constraint_1 == expected_sum

    def test_sum_constraint_case_sum_exception(
            self,
    ):
        word_constraint_1 = WordConstraint(
            banned_letters=["b"],
            letters_potential_position={"a": [1, 2, 3]}
        )
        word_constraint_2 = WordConstraint(
            banned_letters=["a"],
            letters_potential_position=None
        )
        with pytest.raises(Exception):
            word_constraint_1.sum_constraint(word_constraint_2)

    def test_equality(self):
        word_constraint_1 = WordConstraint(
            banned_letters=["a"],
            letters_potential_position={"b": [1]}
        )
        word_constraint_2 = WordConstraint(
            banned_letters=["a"],
            letters_potential_position={"b": [1]}
        )
        assert word_constraint_1 == word_constraint_2

    def test_inequality_case_banned_letters(self):
        word_constraint_1 = WordConstraint(
            banned_letters=["a"],
            letters_potential_position={"b": [1]}
        )
        word_constraint_2 = WordConstraint(
            banned_letters=["c"],
            letters_potential_position={"b": [1]}
        )
        assert word_constraint_1 != word_constraint_2

    def test_inequality_case_letters_potential_position_key(self):
        word_constraint_1 = WordConstraint(
            banned_letters=["a"],
            letters_potential_position={"b": [1]}
        )
        word_constraint_2 = WordConstraint(
            banned_letters=["a"],
            letters_potential_position={"c": [1]}
        )
        assert word_constraint_1 != word_constraint_2

    def test_inequality_case_letters_potential_position_value(self):
        word_constraint_1 = WordConstraint(
            banned_letters=["a"],
            letters_potential_position={"b": [1]}
        )
        word_constraint_2 = WordConstraint(
            banned_letters=["a"],
            letters_potential_position={"b": [2]}
        )
        assert word_constraint_1 != word_constraint_2

    def test_is_word_legal_case_success(self):
        word_constraint = WordConstraint(
            banned_letters=["a"],
            letters_potential_position={'l': [1, 2]},
        )
        assert word_constraint.is_word_legal("elles")

    @pytest.mark.parametrize(
        "banned_letters,letters_potential_position,word",
        [
            (["a"], {'b': [0, 1, 2, 3, 4]}, "brouette"),
            (["p"], {'u': [0, 1, 2, 3, 4]}, "pluie"),
            (["a"], {'b': [0, 1, 2, 3, 4]}, "pluie"),
            (["a"], {'l': [0, 2, 3, 4]}, "pluie"),
            (["a"], {'l': [1]}, "elles"),
        ]
    )
    def test_is_word_legal_case_fail(
            self,
            banned_letters,
            letters_potential_position,
            word,
    ):
        word_constraint = WordConstraint(
            banned_letters=banned_letters,
            letters_potential_position=letters_potential_position,
        )
        assert not word_constraint.is_word_legal(word)

    def test_is_word_legal_case_exception(
            self,
    ):
        word_constraint = WordConstraint(
            banned_letters=None,
            letters_potential_position=None,
        )
        with pytest.raises(Exception):
            word_constraint.is_word_legal(1)
