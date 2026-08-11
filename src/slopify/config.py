from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class SlopifyConfig:
    """Controls how aggressively transforms are applied.

    intensity is the master 0-100 dial. Per-transform weights multiply
    against it so individual transforms (e.g. em dashes) can be tuned
    relative to the others without a separate dial for each one.
    """

    intensity: int = 50
    seed: int | None = None
    transform_weights: dict[str, float] = field(default_factory=dict)

    def weight_for(self, transform_name: str) -> float:
        base = self.intensity / 100
        return base * self.transform_weights.get(transform_name, 1.0)
