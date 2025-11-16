"""Rule-based translator from natural language to Vista action plans."""

from __future__ import annotations

import re
from typing import Any, Dict, List, Optional

from .models import ActionPlan, ActionStep


class ActionEngine:
    """Very small heuristic engine that mirrors the docs' action schema."""

    def __init__(self) -> None:
        self._setting_aliases: Dict[str, str] = {
            "wifi": "wifi",
            "wi-fi": "wifi",
            "bluetooth": "bluetooth",
            "flashlight": "flashlight",
            "torch": "flashlight",
            "volume": "volume",
            "brightness": "brightness",
        }

    def build_plan(self, utterance: str) -> ActionPlan:
        """Create a best-effort ActionPlan from the user's utterance."""

        text = utterance.strip()
        normalized = text.lower()
        handlers = [
            self._handle_send_message,
            self._handle_call,
            self._handle_play_music,
            self._handle_open_app,
            self._handle_read_screen,
            self._handle_toggle_setting,
        ]
        for handler in handlers:
            plan = handler(text, normalized)
            if plan:
                return plan

        return ActionPlan(
            intent="unknown",
            confidence=0.1,
            slots={"raw_text": text},
            steps=[ActionStep(name="clarify", params={"prompt": text})],
            explanation="Fallback: not enough confidence to produce a plan.",
        )

    # Handlers -----------------------------------------------------------------
    def _handle_send_message(self, text: str, normalized: str) -> Optional[ActionPlan]:
        if not any(token in normalized for token in ["message", "text", "whatsapp"]):
            return None

        recipient = self._extract_recipient(normalized)
        content = self._extract_message_body(text)
        app = self._detect_app(normalized)
        slots = {
            "intent": "send_message",
            "app": app,
            "recipient": recipient,
            "content": content,
        }
        steps = [
            ActionStep("open_app", {"app": app}),
            ActionStep("find_contact", {"name": recipient or ""}),
            ActionStep("open_conversation", {}),
            ActionStep("type_message", {"text": content or ""}),
            ActionStep("send", {}),
        ]
        return ActionPlan(
            intent="send_message",
            confidence=0.82,
            slots=slots,
            steps=steps,
            explanation="Detected messaging request via keywords and contact pattern.",
        )

    def _handle_call(self, text: str, normalized: str) -> Optional[ActionPlan]:
        if "call" not in normalized:
            return None

        recipient = self._extract_recipient(normalized) or self._extract_after_keyword(normalized, "call")
        slots = {
            "intent": "make_call",
            "recipient": recipient,
        }
        steps = [
            ActionStep("open_app", {"app": "dialer"}),
            ActionStep("find_contact", {"name": recipient or ""}),
            ActionStep("start_call", {}),
        ]
        return ActionPlan(
            intent="make_call",
            confidence=0.78,
            slots=slots,
            steps=steps,
            explanation="Detected calling intent via keyword match.",
        )

    def _handle_play_music(self, text: str, normalized: str) -> Optional[ActionPlan]:
        if "play" not in normalized and "resume" not in normalized:
            return None
        if not any(token in normalized for token in ["music", "songs", "spotify", "playlist"]):
            return None

        app = "spotify" if "spotify" in normalized else "default_music"
        slots = {
            "intent": "play_music",
            "app": app,
            "context": self._extract_music_context(normalized),
        }
        steps = [
            ActionStep("open_app", {"app": app}),
            ActionStep("resume_playback", {"context": slots["context"]}),
        ]
        return ActionPlan(
            intent="play_music",
            confidence=0.74,
            slots=slots,
            steps=steps,
            explanation="Detected playback intent via play/resume keyword and music token.",
        )

    def _handle_open_app(self, text: str, normalized: str) -> Optional[ActionPlan]:
        if "open" not in normalized and "launch" not in normalized:
            return None

        app = self._extract_after_keyword(normalized, "open") or self._extract_after_keyword(normalized, "launch")
        if not app:
            return None

        slots = {
            "intent": "open_app",
            "app": app,
        }
        steps = [ActionStep("open_app", {"app": app})]
        return ActionPlan(
            intent="open_app",
            confidence=0.6,
            slots=slots,
            steps=steps,
            explanation="Default open/launch handler.",
        )

    def _handle_read_screen(self, text: str, normalized: str) -> Optional[ActionPlan]:
        if "read" not in normalized:
            return None
        if not any(phrase in normalized for phrase in ["screen", "here", "this"]):
            return None

        slots = {"intent": "read_screen"}
        steps = [ActionStep("capture_screen", {}), ActionStep("ocr", {}), ActionStep("narrate", {})]
        return ActionPlan(
            intent="read_screen",
            confidence=0.71,
            slots=slots,
            steps=steps,
            explanation="Screen reading request detected via read + screen keywords.",
        )

    def _handle_toggle_setting(self, text: str, normalized: str) -> Optional[ActionPlan]:
        match = re.search(r"(turn|switch)\s+(on|off)\s+([\w-]+)", normalized)
        if not match:
            match = re.search(r"(enable|disable)\s+([\w-]+)", normalized)
            if not match:
                return None

        action = match.group(2) if match.lastindex and match.lastindex >= 2 else ""
        if match.group(1) in {"enable", "disable"}:
            desired_state = "on" if match.group(1) == "enable" else "off"
            setting = match.group(2)
        else:
            desired_state = action
            setting = match.group(3)

        canonical_setting = self._setting_aliases.get(setting, setting)
        slots = {
            "intent": "toggle_setting",
            "setting": canonical_setting,
            "state": desired_state,
        }
        steps = [ActionStep("set_setting", slots)]
        return ActionPlan(
            intent="toggle_setting",
            confidence=0.69,
            slots=slots,
            steps=steps,
            explanation="Setting toggle detected via turn on/off pattern.",
        )

    # Helpers -------------------------------------------------------------------
    def _extract_recipient(self, normalized: str) -> Optional[str]:
        match = re.search(r"to\s+([a-zA-Z ]+?)(?:\s+(?:saying|that|says|telling)|$)", normalized)
        if match:
            return match.group(1).strip()
        match = re.search(r"call\s+([a-zA-Z ]+)", normalized)
        if match:
            return match.group(1).strip()
        return None

    def _extract_after_keyword(self, normalized: str, keyword: str) -> Optional[str]:
        if keyword not in normalized:
            return None
        after = normalized.split(keyword, 1)[1].strip()
        return after if after else None

    def _extract_message_body(self, text: str) -> Optional[str]:
        normalized = text.lower()
        for delimiter in ["that", "saying", "says", "tell them", "says that"]:
            if delimiter in normalized:
                return text.lower().split(delimiter, 1)[1].strip(" .")
        parts = text.split(".")
        if len(parts) > 1:
            return parts[1].strip()
        return None

    def _extract_music_context(self, normalized: str) -> str:
        if "liked" in normalized:
            return "liked"
        if "playlist" in normalized:
            return "playlist"
        if "some" in normalized and "music" in normalized:
            return "generic_music"
        return "resume"

    def _detect_app(self, normalized: str) -> str:
        for app in ["whatsapp", "telegram", "messages"]:
            if app in normalized:
                return app
        return "default_messaging"
