import os
from .utils import _upgrade, TEST_DB_URL, _mk_account_and_members


def test_mk_account_and_members_twice_without_cleanup() -> None:
    os.environ["ENV"] = "dev"
    _upgrade(TEST_DB_URL)
    _mk_account_and_members(TEST_DB_URL)
    _mk_account_and_members(TEST_DB_URL)
