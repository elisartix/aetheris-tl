import asyncio
import struct

from ..errors.common import ScamDetectionError
from ..tl.tlobject import _raise_if_forbidden_serialized_request


# Keep a sender-bound, immutable second line of defence. User modules can replace
# public helpers on tlobject/requeststate, so the final check must not resolve a
# mutable module global when RequestState is constructed.
def _build_outgoing_safety_guard():
    forbidden_constructor_ids = frozenset(
        {
            0xA2C0CF74,  # account.DeleteAccount
            0x418D4E0B,  # account.DeleteAccount (new schema / forged modules)
        }
    )
    legacy_guard = _raise_if_forbidden_serialized_request

    def guard(request, data):
        legacy_guard(request, data)

        if not isinstance(data, (bytes, bytearray, memoryview)):
            return

        raw = bytes(data)
        for offset in range(0, len(raw) - 3, 4):
            if struct.unpack_from("<I", raw, offset)[0] in forbidden_constructor_ids:
                raise ScamDetectionError(
                    "Usage of account.DeleteAccount is forbidden."
                )

    return guard


_OUTGOING_SAFETY_GUARD = _build_outgoing_safety_guard()


class RequestState:
    """
    This request state holds several information relevant to sent messages,
    in particular the message ID assigned to the request, the container ID
    it belongs to, the request itself, the request as bytes, and the future
    result that will eventually be resolved.
    """

    __slots__ = ("container_id", "msg_id", "request", "data", "future", "after")

    def __init__(self, request, after=None):
        self.container_id = None
        self.msg_id = None
        self.request = request
        self.data = bytes(request)
        _OUTGOING_SAFETY_GUARD(request, self.data)
        self.future = asyncio.Future()
        self.after = after
