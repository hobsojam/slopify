from __future__ import annotations

import random
from dataclasses import dataclass

from slopify.config import SlopifyConfig
from slopify.transforms import DEFAULT_PIPELINE_ORDER, Transform
from slopify.transformlog import TransformLog


@dataclass
class SlopifyResult:
    text: str
    log: TransformLog


class Pipeline:
    def __init__(self, config: SlopifyConfig, transforms: list[Transform] | None = None) -> None:
        self.config = config
        self.transforms = transforms or [cls() for cls in DEFAULT_PIPELINE_ORDER]
        self._rng = random.Random(config.seed)

    def run(self, text: str) -> SlopifyResult:
        log = TransformLog(original_text=text)
        current = text
        for transform in self.transforms:
            weight = self.config.weight_for(transform.name)
            if weight <= 0:
                continue
            before = current
            current = transform.apply(current, weight, self._rng)
            log.record(transform.name, before, current)
        return SlopifyResult(text=current, log=log)
