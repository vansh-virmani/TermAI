from enum import Enum

from pydantic import BaseModel


class SafetyLevel(str, Enum):
    SAFE = "safe"
    WARNING = "warning"
    BLOCKED = "blocked"


class SafetyResult(BaseModel):
    level: SafetyLevel
    reason: str



def validate_command(command: str) -> SafetyResult:
    normalized = " ".join(command.lower().split())

    if normalized in {
        "rm -rf /",
        "rm -rf /*",
    }:
        return SafetyResult(
            level=SafetyLevel.BLOCKED,
            reason="Command attempts recursive deletion from the filesystem root.",
        )

    if "format" in normalized:
        return SafetyResult(
            level=SafetyLevel.BLOCKED,
            reason="Command may format a storage device.",
        )

    if "shutdown" in normalized:
        return SafetyResult(
            level=SafetyLevel.BLOCKED,
            reason="Command shuts down the system.",
        )
    if "stop-computer" in normalized:
        return SafetyResult(
        level=SafetyLevel.BLOCKED,
        reason="Command shuts down the computer.",
    )

    if "remove-item" in normalized:
        return SafetyResult(
            level=SafetyLevel.WARNING,
            reason="Command may delete files or directories.",
        )

    if normalized.startswith("rm "):
        return SafetyResult(
            level=SafetyLevel.WARNING,
            reason="Command may delete files or directories.",
        )

    return SafetyResult(
        level=SafetyLevel.SAFE,
        reason="No known dangerous pattern was detected.",
    )