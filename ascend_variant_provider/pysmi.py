"""
Query all system information by npu-smi.
"""

import re
import subprocess
from typing import Any

ASCEND_INVALID_ERROR = 100001

class AscendSmiError(Exception):
    def __init__(self, code: int = ASCEND_INVALID_ERROR):
        self.code = code
        super().__init__(f"npu-smi backend error {code}")

# General query command
def _npu_info() -> list[dict[str, Any]]:
    out = subprocess.check_output(["npu-smi", "info"], text=True, stderr=subprocess.STDOUT)

    # Get ascend card type
    pat = re.compile(r"^\|\s+(\d+)\s+(\w+).*", re.M)
    devices = []
    for idx, name in pat.findall(out):
        devices.append({
            "device_id": int(idx),
            "type": name,
        })
    return devices

def GetDeviceCount() -> int:
    devs = _npu_info()
    return len(devs)

def GetDeviceType() -> str:
    devs = _npu_info()
    return devs[0]["type"]