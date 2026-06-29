"""Tests for the embedded HFP operator catalogue."""

from __future__ import annotations

from hsl_hfp.operators import OPERATORS, iter_operators


class TestIterOperators:
    def test_operator_id_is_four_digit_zero_padded(self):
        ids = {operator_id for operator_id, _, _, _ in iter_operators()}
        assert "0006" in ids   # operator 6 -> '0006'
        assert "0050" in ids   # HKL-Metroliikenne
        assert "0130" in ids   # three-digit number stays width-4
        assert "0195" in ids

    def test_operator_number_matches_padded_id(self):
        for operator_id, operator_number, _, _ in iter_operators():
            assert operator_id == f"{operator_number:04d}"

    def test_every_catalogue_entry_emitted(self):
        emitted = list(iter_operators())
        assert len(emitted) == len(OPERATORS)

    def test_names_are_non_empty(self):
        for _, _, name, _ in iter_operators():
            assert name and name.strip()
