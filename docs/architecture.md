# Vista OS Architecture

Vista OS is composed of modular services orchestrated by Iris, the ambient assistant. Each module is independently deployable and communicates via an event bus with strongly-typed intents.

## Top-Level Modules

1. **Launcher Core**
   - Replaces the default Android/iOS home screen and manages global gestures (double tap, long press, single tap) and wake-word detection.
   - Maintains the always-on "Iris orb" UI, rotating hint line, and greeting text.
   - Owns session state (e.g., whether Iris is listening, executing, or in vision mode) and routes events to the proper downstream engines.

2. **Voice Engine**
   - Handles speech capture, on-device wake-word spotting ("Iris"), and streaming ASR.
   - Normalizes transcripts (punctuation, entities, contact normalization) before handing them to the Action Engine.

3. **Action Engine**
   - Transforms natural language + contextual metadata (foreground app, last action, available services) into an executable action plan.
   - Uses a hybrid NLU stack: lightweight on-device intent classifier + large reasoning model (cloud or on-device, depending on privacy budget) for complex plans.
   - Emits plans using the shared Action Plan schema (see `docs/action-plan.md`).

4. **Accessibility Controller**
   - Executes steps using Accessibility APIs, Android Intents, or iOS Shortcuts.
   - Performs OCR + layout analysis when an app is unknown to the system.
   - Provides screen-reading ("Read current screen") and interaction primitives (tap, swipe, type, scroll, read selection).

5. **Vision Engine**
   - Streams frames from the front or back camera when Vision Mode is active.
   - Runs perception models for obstacle detection, semantic segmentation, OCR, and spatial grounding.
   - Surfaces prioritized observations (safety > navigation > context) through Iris' speech output.

6. **Knowledge + Memory Store**
   - Captures recent actions, user preferences (e.g., preferred messaging app), and environment snippets for follow-up questions.
   - Accessible to both Action and Vision engines for contextual grounding.

7. **Audio Output + Tactile Feedback Service**
   - Renders Iris' speech responses and optional haptics (e.g., short pulse when Vision mode starts/stops).

## Event Flow Overview

1. Gesture or wake word triggers the Launcher Core.
2. Voice Engine captures/transcribes speech; transcript sent to Action Engine.
3. Action Engine emits an action plan.
4. Accessibility Controller executes steps, reporting progress/failures back to Iris.
5. Iris narrates status and listens for follow-ups without forcing the user to re-trigger.

Vision mode bypasses the voice transcription step once engaged; the Launcher directly routes camera frames to the Vision Engine, which streams prioritized findings back to Iris.

## Reliability + Safety Considerations

- **Watchdog timers** for long-running steps: Iris notifies the user if an action exceeds a configurable timeout.
- **Confirmation for destructive actions** (delete, send money) enforced by the Action Engine.
- **Privacy guardrails**: Vision processing defaults to on-device and never stores frames unless the user explicitly saves a snapshot.

