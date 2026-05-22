from constants import OFFSET, TOTAL_DEGREES


def load_raw_values(filepath: str) -> list[float]:
    """Read a file in index=value format and return 360 floats."""
    values = [0.0] * TOTAL_DEGREES
    with open(filepath, encoding="utf-8-sig") as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line or "=" not in line:
                continue
            idx_str, val_str = line.split("=", maxsplit=1)
            try:
                values[int(idx_str)] = float(val_str)
            except (ValueError, IndexError) as e:
                raise ValueError(f"Line {lineno} has invalid format ({line!r}): {e}") from e
    return values


def apply_offset_shift(raw: list[float]) -> list[float]:
    """Rotate data by OFFSET degrees using the b_key formula."""
    return [raw[(OFFSET + i) % TOTAL_DEGREES] for i in range(TOTAL_DEGREES)]