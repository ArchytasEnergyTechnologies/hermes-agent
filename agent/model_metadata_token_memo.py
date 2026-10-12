"""Release a closed conversation's entries from the per-message token-estimate memo.

``agent.model_metadata._MSG_TOKENS_CACHE`` keys hold every string they fingerprint, so a long-lived process
kept each closed session's message bodies resident until 4096 newer messages pushed them out. Two release
paths cover it:

* by owner: a turn binds its agent (``token_memo_owner``) and every entry inserted under it records that
  owner, so ``close()`` drops the request-time strings no history holds (the ephemeral system-prompt concat,
  prefill rows, prompt-caching and skill-split slices, MoA advisor folds);
* by value: ``forget_message_token_memo`` drops entries holding the long strings of given messages, for
  entries inserted outside a turn and for the bodies compression replaced.
"""

from __future__ import annotations

import contextlib
from collections.abc import Iterator
from contextvars import ContextVar
from typing import Any

_owner_var: ContextVar[int | None] = ContextVar("hermes_token_memo_owner", default=None)


def current_token_memo_owner() -> int | None:
    """The owner new memo entries record: the agent whose turn is running in this context, if any. An id
    reused by a later agent only widens what that agent's close() evicts, never what an estimate returns."""
    return _owner_var.get()


@contextlib.contextmanager
def token_memo_owner(agent: Any) -> Iterator[None]:
    """Record ``agent`` as the owner of every memo entry inserted in this context until exit."""
    token = _owner_var.set(id(agent))
    try:
        yield
    finally:
        _owner_var.reset(token)


def _long_strings(value: Any) -> set[str]:
    found: set[str] = set()
    stack = [value]
    while stack:
        value = stack.pop()
        if type(value) is dict:
            stack.extend(value.values())
        elif type(value) is list or type(value) is tuple:
            stack.extend(value)
        elif type(value) is str and len(value) > 64:  # short values ("assistant", tool names) are shared
            found.add(value)
    return found


def forget_message_token_memo(messages: Any, *, keep: Any = None, owner: Any = None) -> int:
    """Evict memo entries holding any long string of ``messages`` that ``keep`` does not also hold, plus
    every entry ``owner``'s turns inserted; return how many.

    Eviction never changes an estimate: a later lookup recomputes the same value.
    """
    from agent.model_metadata import _MSG_TOKENS_CACHE

    owned = _long_strings(messages)
    if owned and keep is not None:
        owned -= _long_strings(keep)
    owner_id = None if owner is None else id(owner)
    if not owned and owner_id is None:
        return 0
    # Fingerprint keys are nested tuples whose string leaves are the message's own values.
    stale = [key for key, (_text, _images, entry_owner) in list(_MSG_TOKENS_CACHE.items())
             if (owner_id is not None and entry_owner == owner_id) or (owned and not owned.isdisjoint(_long_strings(key)))]
    for key in stale:
        _MSG_TOKENS_CACHE.pop(key, None)
    return len(stale)
