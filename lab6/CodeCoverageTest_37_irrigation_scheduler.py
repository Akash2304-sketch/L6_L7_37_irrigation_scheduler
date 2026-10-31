"""Line-coverage tests for the irrigation scheduler application."""
import pytest

from irrigation_scheduler import schedule, should_irrigate, water_volume


def test_should_irrigate_wet_soil():
    assert should_irrigate(60, 0, "seedling") is False
    assert should_irrigate(75, 0, "flowering") is False


def test_should_irrigate_heavy_rain():
    assert should_irrigate(30, 10, "seedling") is False


def test_seedling_threshold_both_sides():
    assert should_irrigate(44, 0, "seedling") is True
    assert should_irrigate(45, 0, "seedling") is False


def test_flowering_threshold_both_sides():
    assert should_irrigate(54, 0, "flowering") is True
    assert should_irrigate(55, 0, "flowering") is False


def test_other_stage_rain_and_moisture_rules():
    assert should_irrigate(30, 5, "mature") is False
    assert should_irrigate(39, 4, "mature") is True
    assert should_irrigate(40, 4, "mature") is False


def test_water_volume_rejects_non_positive_area():
    with pytest.raises(ValueError, match="invalid area"):
        water_volume(0, "seedling", 20)
    with pytest.raises(ValueError, match="invalid area"):
        water_volume(-2, "flowering", 20)


def test_water_volume_for_each_growth_stage():
    assert water_volume(10, "seedling", 20) == 20
    assert water_volume(10, "flowering", 20) == 50
    assert water_volume(10, "mature", 20) == 40


def test_water_volume_temperature_adjustments():
    assert water_volume(2, "seedling", 36) == 6
    assert water_volume(2, "flowering", 9) == 5
    assert water_volume(2, "mature", 20) == 8


def test_schedule_adds_irrigated_zones_and_skips_others():
    zones = [
        ("North", 10, 30, 0, "seedling", 20),
        ("Wet", 10, 70, 0, "seedling", 20),
        ("South", 5, 30, 0, "flowering", 20),
    ]
    assert schedule(zones, 100) == ["North", "South"]


def test_schedule_stops_when_budget_is_insufficient():
    zones = [
        ("First", 10, 30, 0, "seedling", 20),
        ("TooLarge", 100, 30, 0, "seedling", 20),
        ("NeverReached", 1, 30, 0, "seedling", 20),
    ]
    assert schedule(zones, 25) == ["First"]


def test_schedule_with_empty_zone_list():
    assert schedule([], 100) == []
