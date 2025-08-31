from datetime import datetime, timedelta
from backend.app.services.conflicts import ConflictService, Assignment


class MockDB:
    def __init__(self):
        now = datetime(2025, 9, 1, 8)
        self.assigns = [
            Assignment(1, 10, "Alice", now, now + timedelta(hours=4), "Light"),
            Assignment(2, 10, "Alice", now + timedelta(hours=2), now + timedelta(hours=5), "Sound"),
            Assignment(3, 11, "Bob", now, now + timedelta(hours=3), "Any"),
        ]
        self._users = [{"id": 11, "name": "Bob"}, {"id": 12, "name": "Chloe"}]

    def fetch_assignments(self, s, e):
        return self.assigns

    def fetch_users(self):
        return self._users

    def fetch_user_assignments(self, uid, s, e):
        return [a for a in self.assigns if a.user_id == uid]

    def replace_assignment(self, mission_id, replacement_user_id):
        return True


def test_find_conflicts_ok():
    svc = ConflictService(MockDB())
    res = svc.find_conflicts(datetime(2025, 9, 1), datetime(2025, 9, 2))
    assert len(res) == 1
    c = res[0]
    assert c.user_name == "Alice"
    assert set(c.mission_ids) == {1, 2}


def test_suggestions_ok():
    svc = ConflictService(MockDB())
    c = svc.find_conflicts(datetime(2025, 9, 1), datetime(2025, 9, 2))[0]
    sugg = svc.suggest_replacements(c)
    assert any(s.user_name == "Chloe" for s in sugg)


def test_resolve_ok():
    svc = ConflictService(MockDB())
    ok = svc.resolve("1-2:10", mission_id=1, replacement_user_id=12)
    assert ok
