from unittest import TestCase

import pytest
from _pytest.monkeypatch import MonkeyPatch

from ..word_constraint import WordConstraint
from ..step import Step


class TestStep(TestCase):
    def setUp(self):
        self.monkeypatch = MonkeyPatch()
        self.mock_value = None
        self.monkeypatch.setattr('builtins.input', lambda _: self.mock_value)

    def test_data_validator_case_word_constraint(self):
        with pytest.raises(Exception):
            Step(
                word="Oui",
                word_constraint=None
            )

    def test_data_validator_case_word_type(self):
        with pytest.raises(Exception):
            Step(
                word=1,
                word_constraint=WordConstraint()
            )

    def test_data_validator_case_word_length(self):
        with pytest.raises(Exception):
            Step(
                word="az",
                word_constraint=WordConstraint()
            )

    def test_data_validator_case_word_illegal(self):
        with pytest.raises(Exception):
            Step(
                word="pluie",
                word_constraint=WordConstraint(
                    banned_letters=["u"]
                )
            )

    def test_input_validator_case_length(self):
        self.mock_value = "00"
        with pytest.raises(Exception):
            Step(
                word="pluie",
                word_constraint=WordConstraint()
            )

    def test_input_validator_case_illegal_character(self):
        self.mock_value = "0000a"
        with pytest.raises(Exception):
            Step(
                word="pluie",
                word_constraint=WordConstraint()
            )

    def test_compute_constraint_case_banned_letters(self):
        self.mock_value = "00000"
        step = Step(
            word="pluie",
            word_constraint=WordConstraint()
        )
        expected_constraint = WordConstraint(
            banned_letters=["p", "l", "u", "i", "e"]
        )
        assert expected_constraint == step.word_constraint

    def test_compute_constraint_case_misplaced_letters(self):
        self.mock_value = "11111"
        step = Step(
            word="pluie",
            word_constraint=WordConstraint()
        )
        expected_constraint = WordConstraint(
            letters_potential_position={
                "p": [1, 2, 3, 4],
                "l": [0, 2, 3, 4],
                "u": [0, 1, 3, 4],
                "i": [0, 1, 2, 4],
                "e": [0, 1, 2, 3],
            }
        )
        assert expected_constraint == step.word_constraint

    def test_compute_constraint_case_good_letters(self):
        self.mock_value = "22222"
        step = Step(
            word="pluie",
            word_constraint=WordConstraint()
        )
        expected_constraint = WordConstraint(
            letters_potential_position={
                "p": [0],
                "l": [1],
                "u": [2],
                "i": [3],
                "e": [4],
            }
        )
        assert expected_constraint == step.word_constraint

    def test_compute_sum_constraint(self):
        self.mock_value = "00000"
        step = Step(
            word='aaaaa',
            word_constraint=WordConstraint(
                banned_letters=["b"]
            )
        )
        expected_constraint = WordConstraint(
            banned_letters=["a", "b"]
        )
        assert step.word_constraint == expected_constraint
