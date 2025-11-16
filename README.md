# Vista OS

Vista OS is a minimal, voice-first launcher designed for blind and low-vision users. Iris, the ambient assistant, powers every interaction—from opening apps to navigating the physical world through the cameras.

## Principles
- **Voice first**: Speak naturally; Iris handles the rest.
- **Touch simplified**: Double tap to talk, hold for vision, single tap to stop.
- **Vision aware**: Turn the device into a guide that describes surroundings.
- **Accessibility by default**: Works eyes-closed with concise audio feedback.

## Interaction Layers
1. **Launcher Layer** – Device control, app automation, and assistant tasks. See [`docs/launcher.md`](docs/launcher.md).
2. **Vision Layer** – Environment understanding and navigation guidance. See [`docs/vision-mode.md`](docs/vision-mode.md).

## Natural Language → Action Plans
Iris converts conversational speech into deterministic action plans that the system executes through accessibility APIs and intents. The schema and operation catalog are documented in [`docs/action-plan.md`](docs/action-plan.md).

## System Architecture
A modular stack keeps the system resilient and extensible: Launcher Core, Voice Engine, Action Engine, Accessibility Controller, Vision Engine, Knowledge Store, and Output services. Detailed breakdown lives in [`docs/architecture.md`](docs/architecture.md).

## Example Requests
- “Iris, send a message to Sam. Say that I’ll be there in ten minutes.”
- “Iris, play some music.”
- “Iris, call my mom.”
- “Iris, read what’s on my screen.”
- “What’s in front of me?” (while holding the screen for Vision Mode)

## Roadmap Snapshot
- ✅ Define interaction model and action schema
- 🚧 Prototype Action Engine + accessibility executor
- 🚧 Implement continuous Vision Mode streaming
- ⏳ Hardware partnerships for tactile feedback accessories

## Action Engine Prototype
The repository now ships a tiny rule-based Action Engine that mirrors the plan schema
described in the docs. It is only a bootstrapper but allows us to start iterating on
end-to-end flows before a learning-based model lands.

```bash
python -m vista_action_engine.cli "send a WhatsApp message to Sam saying I will arrive soon"
```

This prints a structured `ActionPlan` JSON object with the inferred intent, slots, and
step list. Unit tests cover the initial set of supported commands (messaging, calls,
music playback, open app, read screen, and toggle settings).

## Launcher Prototype (HTML)
Need to **see and feel** the gestures before the Android build exists? Spin up the static
launcher mock that mirrors the greeting screen, orb, rotating hints, and Vision Mode card.

```bash
python -m http.server --directory ui/launcher 4173
```

Then open [http://localhost:4173](http://localhost:4173) in a browser. The full screen is
an interaction surface:

- **Single tap** → interrupt / stop Iris.
- **Double tap** → Iris enters listening mode and logs a mock action plan.
- **Long press / hold** → Vision Mode toggles on while held, streaming sample observations.
- **Command input** → Type any utterance to see how the prototype would summarize the plan.

This prototype is deliberately lightweight (vanilla HTML/CSS/JS) so designers can tweak
copy, gradients, or gestures quickly without a bundler.

