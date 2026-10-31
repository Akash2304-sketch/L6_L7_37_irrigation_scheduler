"""Branch-coverage tests for every decision in the irrigation scheduler."""
import pytest

from irrigation_scheduler import schedule, should_irrigate, water_volume


@pytest.mark.parametrize(
    "moisture,rain,stage,expected",
    [
        (60, 0, "seedling", False),
        (59, 10, "seedling", False),
        (59, 9, "seedling", False),
        (44, 9, "seedling", True),
        (54, 9, "flowering", True),
        (55, 9, "flowering", False),
        (39, 5, "mature", False),
        (39, 4, "mature", True),
        (40, 4, "mature", False),
    ],
)
def test_all_irrigation_decision_branches(moisture, rain, stage, expected):
    assert should_irrigate(moisture, rain, stage) is expected


@pytest.mark.parametrize("area", [0, -1])
def test_water_volume_invalid_area_branch(area):
    with pytest.raises(ValueError, match="invalid area"):
        water_volume(area, "seedling", 20)


@pytest.mark.parametrize(
    "stage,temperature,expected",
    [
        ("seedling", 20, 2),
        ("flowering", 20, 5),
        ("mature", 20, 4),
        ("seedling", 36, 3),
        ("flowering", 9, 2.5),
        ("mature", 10, 4),
        ("mature", 35, 4),
    ],
)
def test_water_volume_growth_and_temperature_branches(stage, temperature, expected):
    assert water_volume(1, stage, temperature) == expected


def test_schedule_continue_branch_and_successful_append():
    zones = [
        ("SkipWet", 1, 70, 0, "seedling", 20),
        ("SkipRain", 1, 30, 10, "seedling", 20),
        ("Keep", 2, 30, 0, "seedling", 20),
    ]
    assert schedule(zones, 10) == ["Keep"]


def test_schedule_budget_break_branch():
    zones = [
        ("First", 2, 30, 0, "seedling", 20),
        ("OverBudget", 10, 30, 0, "seedling", 20),
        ("AfterBreak", 1, 30, 0, "seedling", 20),
    ]
    assert schedule(zones, 5) == ["First"]


def test_schedule_empty_loop_exit_branch():
    assert schedule([], 0) == []
