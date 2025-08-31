from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict
from datetime import datetime
import itertools


@dataclass
class Assignment:
    mission_id: int
    user_id: int
    user_name: str
    start: datetime
    end: datetime
    role: str


@dataclass
class Conflict:
    conflict_id: str
    user_id: int
    user_name: str
    mission_ids: List[int]
    start: datetime
    end: datetime
    reason: str = "DOUBLE_BOOKING"


def _overlap(a_start, a_end, b_start, b_end) -> bool:
    return not (a_end <= b_start or b_end <= a_start)


class ConflictService:
    def __init__(self, db):
        self.db = db

    def _load_assignments(self, start: datetime, end: datetime) -> List[Assignment]:
        return self.db.fetch_assignments(start, end)

    def find_conflicts(self, start: datetime, end: datetime) -> List[Conflict]:
        assigns = sorted(self._load_assignments(start, end), key=lambda a: (a.user_id, a.start))
        conflicts: List[Conflict] = []
        for user_id, group in itertools.groupby(assigns, key=lambda a: a.user_id):
            items = list(group)
            for i in range(len(items)):
                for j in range(i + 1, len(items)):
                    a, b = items[i], items[j]
                    if _overlap(a.start, a.end, b.start, b.end):
                        cid = f"{a.mission_id}-{b.mission_id}:{a.user_id}"
                        conflicts.append(
                            Conflict(
                                conflict_id=cid,
                                user_id=a.user_id,
                                user_name=a.user_name,
                                mission_ids=[a.mission_id, b.mission_id],
                                start=max(a.start, b.start),
                                end=min(a.end, b.end),
                            )
                        )
        uniq: Dict[str, Conflict] = {c.conflict_id: c for c in conflicts}
        return list(uniq.values())

    def suggest_replacements(self, conflict: Conflict) -> List[Assignment]:
        all_users = self.db.fetch_users()
        busy_user_ids = {conflict.user_id}
        suggestions: List[Assignment] = []
        for u in all_users:
            if u["id"] in busy_user_ids:
                continue
            user_assigns = self.db.fetch_user_assignments(u["id"], conflict.start, conflict.end)
            if all(not _overlap(a.start, a.end, conflict.start, conflict.end) for a in user_assigns):
                suggestions.append(
                    Assignment(
                        mission_id=conflict.mission_ids[0],
                        user_id=u["id"],
                        user_name=u["name"],
                        start=conflict.start,
                        end=conflict.end,
                        role="any",
                    )
                )
        return suggestions

    def resolve(self, conflict_id: str, mission_id: int, replacement_user_id: int) -> bool:
        return self.db.replace_assignment(mission_id, replacement_user_id)
