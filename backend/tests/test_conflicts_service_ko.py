from datetime import datetime
from backend.app.services.conflicts import ConflictService


class MockEmpty:
    def fetch_assignments(self, s, e):
        return []

    def fetch_users(self):
        return []

    def fetch_user_assignments(self, uid, s, e):
        return []

    def replace_assignment(self, mission_id, replacement_user_id):
        return False


def test_no_conflicts_ko():
    svc = ConflictService(MockEmpty())
    res = svc.find_conflicts(datetime(2025, 9, 1), datetime(2025, 9, 2))
    assert res == []


def test_resolve_ko():
    svc = ConflictService(MockEmpty())
    assert svc.resolve("x", 1, 2) is False
