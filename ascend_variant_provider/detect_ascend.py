from __future__ import annotations

import functools
from dataclasses import dataclass

from ascend_variant_provider import pysmi

NORMALIZE_TYPE = {
    "910B1": "910B",
    "910B2": "910B",
    "910B3": "910B",
    "910B4": "910B",
}

@dataclass(frozen=True, order=True)
class AscendEnvironment:
    npu_type: str | None

    @classmethod
    @functools.lru_cache(maxsize=1)
    def from_system(cls) -> AscendEnvironment | None:
        try:
            count = pysmi.GetDeviceCount()
            if count == 0:
                return None

            raw_type=pysmi.GetDeviceType()
            return cls(
                npu_type=NORMALIZE_TYPE.get(raw_type.upper(), raw_type).lower(),
            )
        except Exception:
            return None


if __name__ == "__main__":
    print(f"{AscendEnvironment.from_system()=}")