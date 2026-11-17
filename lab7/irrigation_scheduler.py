"""Input-safe irrigation calculations used by the Lab 7 fuzz tests.

Invalid inputs raise ValueError with a readable message. The interactive
entry point catches those errors so one bad field does not terminate the app.
"""
import math


def _require_text(value, field):
    if not isinstance(value, str):
        raise ValueError(f"{field} must be a string")
    if not value.strip():
        raise ValueError(f"{field} cannot be empty")
    return value.strip()


def _finite_number(value, field):
    try:
        number = float(value)
    except (TypeError, ValueError, OverflowError):
        raise ValueError(f"{field} must be a number") from None
    if not math.isfinite(number):
        raise ValueError(f"{field} must be finite")
    return number


def parse_zone(text):
    """Parse 'zone-name:area' and return (title-cased name, area)."""
    raw = _require_text(text, "Zone input")
    if raw.count(":") != 1:
        raise ValueError("Zone input must contain exactly one ':' separator")
    name, area_text = raw.split(":")
    name = name.strip()
    if not name:
        raise ValueError("Zone name cannot be empty")
    area = _finite_number(area_text.strip(), "Area")
    if area <= 0:
        raise ValueError("Area must be greater than zero")
    return name.title(), area


def moisture_average(readings_csv):
    """Return the integer-floor average of comma-separated moisture values."""
    raw = _require_text(readings_csv, "Moisture readings")
    parts = raw.split(",")
    if any(not part.strip() for part in parts):
        raise ValueError("Moisture readings cannot contain empty values")

    values = []
    for part in parts:
        token = part.strip()
        try:
            # Reject decimal notation and other values int() cannot parse.
            value = int(token)
        except (TypeError, ValueError, OverflowError):
            raise ValueError("Each moisture reading must be an integer") from None
        if not 0 <= value <= 100:
            raise ValueError("Moisture readings must be between 0 and 100")
        values.append(value)

    return sum(values) // len(values)


def water_needed(text):
    """Calculate water requirement as max(area * 5 - rainfall, 0)."""
    raw = _require_text(text, "Water input")
    if raw.count("|") != 1:
        raise ValueError("Water input must contain exactly one '|' separator")
    plot_text, rain_text = raw.split("|")
    area = _finite_number(plot_text.strip(), "Plot area")
    rainfall = _finite_number(rain_text.strip(), "Rainfall")
    if area <= 0:
        raise ValueError("Plot area must be greater than zero")
    if rainfall < 0:
        raise ValueError("Rainfall cannot be negative")
    return max(area * 5 - rainfall, 0.0)


def _run_prompt(title, prompt, processor, result_label):
    print(f"==== Running {title} ====")
    try:
        result = processor(input(prompt))
        print(f"{result_label}: {result}")
    except ValueError as exc:
        print(f"Invalid input: {exc}")


def main():
    _run_prompt(
        "parse_zone",
        "Enter zone:area in m2 (e.g. north:120): ",
        parse_zone,
        "Zone and Area",
    )
    print()
    _run_prompt(
        "moisture_average",
        "Enter moisture readings as CSV (e.g. 40,35,50): ",
        moisture_average,
        "Average Moisture",
    )
    print()
    _run_prompt(
        "water_needed",
        "Enter area|rainfall (e.g. 120|8): ",
        water_needed,
        "Water Needed",
    )


if __name__ == "__main__":
    main()
