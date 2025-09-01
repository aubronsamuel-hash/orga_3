from app.services.conflicts import _normalize_iso_utc


def test_normalize_iso_z_to_offset() -> None:
    d = _normalize_iso_utc("2025-09-02T09:00:00Z")
    assert d.tzinfo is not None
    assert d.isoformat().endswith("+00:00")


def test_normalize_iso_space_ok() -> None:
    d = _normalize_iso_utc("2025-09-02 09:00:00Z")
    assert d.tzinfo is not None

