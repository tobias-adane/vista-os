"""Data models for Vista Action Engine."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass(slots=True)
class ActionStep:
    """Represents a single executable step in an action plan."""

    name: str
    params: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ActionPlan:
    """Structured description of Iris' response to a voice request."""

    intent: str
    confidence: float
    slots: Dict[str, Any]
    steps: List[ActionStep]
    explanation: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert the plan to a JSON-serialisable dict."""

        return {
            "intent": self.intent,
            "confidence": round(self.confidence, 3),
            "slots": self.slots,
            "steps": [
                {
                    "name": step.name,
                    "params": step.params,
                }
                for step in self.steps
            ],
            "explanation": self.explanation,
        }
