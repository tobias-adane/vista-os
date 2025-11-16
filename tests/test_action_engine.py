"""Tests for the Vista Action Engine prototype."""

from vista_action_engine import ActionEngine


def build(text: str):
    return ActionEngine().build_plan(text)


def test_send_message():
    plan = build("Iris send a WhatsApp message to Sam saying I will arrive soon")
    assert plan.intent == "send_message"
    assert plan.slots["recipient"] == "sam"
    assert plan.steps[-1].name == "send"


def test_call():
    plan = build("call my mom")
    assert plan.intent == "make_call"
    assert plan.steps[0].params["app"] == "dialer"


def test_play_music():
    plan = build("play some music on Spotify")
    assert plan.intent == "play_music"
    assert plan.slots["app"] == "spotify"


def test_toggle_setting():
    plan = build("turn on the flashlight")
    assert plan.intent == "toggle_setting"
    assert plan.slots["state"] == "on"


def test_unknown():
    plan = build("remind me later")
    assert plan.intent == "unknown"
    assert plan.steps[0].name == "clarify"
