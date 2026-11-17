"""Property-based fuzz tests for the irrigation scheduler.

The tests allow the documented ValueError for malformed input, but fail on
unexpected exceptions such as TypeError, IndexError, ZeroDivisionError or
OverflowError. They also check result invariants for generated valid inputs.
"""
import math

from hypothesis import given, strategies as st

from irrigation_scheduler import parse_zone, moisture_average, water_needed


TEXT_OR_NONE = st.one_of(st.text(), st.none())


@given(TEXT_OR_NONE)
def test_parse_zone_handles_arbitrary_input(value):
    try:
        result = parse_zone(value)
    except ValueError:
        return
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert isinstance(result[0], str) and result[0]
    assert math.isfinite(result[1]) and result[1] > 0


@given(TEXT_OR_NONE)
def test_moisture_average_handles_arbitrary_input(value):
    try:
        result = moisture_average(value)
    except ValueError:
        return
    assert isinstance(result, int)
    assert 0 <= result <= 100


@given(TEXT_OR_NONE)
def test_water_needed_handles_arbitrary_input(value):
    try:
        result = water_needed(value)
    except ValueError:
        return
    assert math.isfinite(result)
    assert result >= 0


@given(
    st.text(alphabet=st.characters(whitelist_categories=("Ll", "Lu")), min_size=1, max_size=20),
    st.floats(min_value=0.01, max_value=1_000_000, allow_nan=False, allow_infinity=False),
)
def test_parse_zone_valid_values(name, area):
    parsed_name, parsed_area = parse_zone(f"{name}:{area}")
    assert parsed_name == name.title()
    assert math.isclose(parsed_area, area, rel_tol=1e-9, abs_tol=1e-9)


@given(st.lists(st.integers(min_value=0, max_value=100), min_size=1, max_size=100))
def test_moisture_average_valid_values(values):
    result = moisture_average(",".join(map(str, values)))
    assert result == sum(values) // len(values)


@given(
    st.floats(min_value=0.01, max_value=1_000_000, allow_nan=False, allow_infinity=False),
    st.floats(min_value=0, max_value=1_000_000, allow_nan=False, allow_infinity=False),
)
def test_water_needed_valid_values(area, rainfall):
    result = water_needed(f"{area}|{rainfall}")
    assert math.isclose(result, max(area * 5 - rainfall, 0.0), rel_tol=1e-9, abs_tol=1e-9)


def test_known_edge_cases_are_rejected():
    for value in (None, "", "north", ":10", "north:0", "north:nan", "north:inf"):
        try:
            parse_zone(value)
        except ValueError:
            pass
        else:
            raise AssertionError(f"parse_zone should reject {value!r}")

    for value in (None, "", "1,,2", "101", "-1", "one,two"):
        try:
            moisture_average(value)
        except ValueError:
            pass
        else:
            raise AssertionError(f"moisture_average should reject {value!r}")

    for value in (None, "", "10", "10|1|2", "0|0", "10|-1", "nan|0"):
        try:
            water_needed(value)
        except ValueError:
            pass
        else:
            raise AssertionError(f"water_needed should reject {value!r}")
