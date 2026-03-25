import pytest
from unittest.mock import MagicMock, patch


def test_uow_calls_commit_on_success():
    uow = MagicMock()
    uow.__enter__ = MagicMock(return_value=uow)
    uow.__exit__ = MagicMock(return_value=False)

    with uow:
        uow.commit()

    uow.commit.assert_called_once()


def test_uow_calls_rollback_on_exception():
    uow = MagicMock()
    uow.__enter__ = MagicMock(return_value=uow)
    uow.__exit__ = MagicMock(return_value=False)

    try:
        with uow:
            raise ValueError("Something went wrong")
    except ValueError:
        uow.rollback()

    uow.rollback.assert_called_once()


def test_uow_repositories_are_initialized():
    uow = MagicMock()
    uow.__enter__ = MagicMock(return_value=uow)
    uow.__exit__ = MagicMock(return_value=False)

    with uow:
        assert uow.users is not None
        assert uow.categories is not None
        assert uow.transactions is not None
        assert uow.budgets is not None
        assert uow.alerts is not None