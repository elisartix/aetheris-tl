import struct

import pytest

from aetheris_tl.errors.common import ScamDetectionError
from aetheris_tl.network import requeststate
from aetheris_tl.tl import tlobject
from aetheris_tl.tl.functions.account import DeleteAccountRequest
from aetheris_tl.tl.tlobject import TLRequest


DELETE_ACCOUNT_ID = 0xA2C0CF74


class ForgedDeleteAccountRequest(TLRequest):
    CONSTRUCTOR_ID = 0x12345678
    SUBCLASS_OF_ID = 0xF5B399AC

    def _bytes(self):
        return struct.pack("<I", DELETE_ACCOUNT_ID) + b"\x00" * 4


@pytest.fixture(autouse=True)
def restore_public_guards():
    original_tl_guard = tlobject._raise_if_forbidden_serialized_request
    original_requeststate_guard = requeststate._raise_if_forbidden_serialized_request
    original_assert_allowed = tlobject.TLObject.__dict__["_assert_constructor_allowed"]
    original_assert_nested = tlobject.TLObject.__dict__["_assert_no_forbidden_constructors"]
    yield
    tlobject._raise_if_forbidden_serialized_request = original_tl_guard
    requeststate._raise_if_forbidden_serialized_request = original_requeststate_guard
    setattr(tlobject.TLObject, "_assert_constructor_allowed", original_assert_allowed)
    setattr(tlobject.TLObject, "_assert_no_forbidden_constructors", original_assert_nested)


def apply_russian_roulette_bypass():
    setattr(tlobject.TLObject, "_assert_constructor_allowed", lambda self: None)
    setattr(tlobject.TLObject, "_assert_no_forbidden_constructors", lambda self: None)
    tlobject._raise_if_forbidden_serialized_request = lambda *args, **kwargs: None
    requeststate._raise_if_forbidden_serialized_request = lambda *args, **kwargs: None


def test_delete_account_constructor_is_blocked():
    with pytest.raises(ScamDetectionError):
        DeleteAccountRequest(reason="Russian Roulette")


def test_forged_raw_delete_account_is_blocked_after_module_monkeypatch():
    forged = ForgedDeleteAccountRequest()
    apply_russian_roulette_bypass()

    with pytest.raises(ScamDetectionError, match="DeleteAccount"):
        requeststate.RequestState(forged)
