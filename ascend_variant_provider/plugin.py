from __future__ import annotations

import os
from dataclasses import dataclass
from functools import cache
from typing import Protocol, runtime_checkable

from ascend_variant_provider.detect_ascend import AscendEnvironment


@runtime_checkable
class VariantPropertyType(Protocol):
    @property
    def namespace(self) -> str: ...
    @property
    def feature(self) -> str: ...
    @property
    def value(self) -> str: ...


@dataclass(frozen=True)
class VariantFeatureConfig:
    name: str
    values: list[str]
    multi_value: bool = False


class AscendVariantFeatureKey:
    DeviceType = "npu_type"

    
class AscendVariantPlugin:
    namespace = "ascend"
    dynamic = False

    @classmethod
    @cache
    def get_supported_configs(cls, context=None) -> list[VariantFeatureConfig]:
        npu_type = os.environ.get("ASCEND_VARIANT_PROVIDER_FORCE_NPU_TYPE")
        if npu_type:
            return [
                VariantFeatureConfig(
                    name=AscendVariantFeatureKey.DeviceType,
                    values=[npu_type],
                )
            ]
        try:
            env = AscendEnvironment.from_system()
            if env is None or env.npu_type is None:
                return None
            return [
                VariantFeatureConfig(
                    name=AscendVariantFeatureKey.DeviceType,
                    values=[env.npu_type],
                )
            ]
        except Exception:
            return None

    @classmethod
    @cache
    def get_all_configs(cls, context=None) -> list[VariantFeatureConfig]:
        return cls.get_supported_configs()