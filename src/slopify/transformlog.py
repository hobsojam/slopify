from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path


@dataclass
class LogEntry:
    """One transform's before/after text snapshot.

    Storing full snapshots (not diffs) keeps reversal trivial: deslopify
    just walks the entries backwards and swaps `after` back to `before`.
    That's wasteful for long documents but simple, and simple is right
    for v1 exact-inverse deslopify.
    """

    transform: str
    before: str
    after: str


@dataclass
class TransformLog:
    original_text: str
    entries: list[LogEntry] = field(default_factory=list)

    def record(self, transform: str, before: str, after: str) -> None:
        if before == after:
            return
        self.entries.append(LogEntry(transform=transform, before=before, after=after))

    def to_json(self) -> str:
        return json.dumps(
            {
                "original_text": self.original_text,
                "entries": [asdict(e) for e in self.entries],
            },
            indent=2,
        )

    @classmethod
    def from_json(cls, raw: str) -> "TransformLog":
        data = json.loads(raw)
        entries = [LogEntry(**e) for e in data["entries"]]
        return cls(original_text=data["original_text"], entries=entries)

    def save(self, path: str | Path) -> None:
        Path(path).write_text(self.to_json(), encoding="utf-8")

    @classmethod
    def load(cls, path: str | Path) -> "TransformLog":
        return cls.from_json(Path(path).read_text(encoding="utf-8"))

    def reverse(self, text: str) -> str:
        """Undo transforms in reverse order, matching against recorded `after` state."""
        for entry in reversed(self.entries):
            if text != entry.after:
                raise ValueError(
                    f"Text has diverged from the log at transform '{entry.transform}'; "
                    "cannot cleanly reverse."
                )
            text = entry.before
        return text
