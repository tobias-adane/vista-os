# Launcher + Interaction Model

The Launcher is the user's always-on gateway into Vista OS. Its UI is purposefully minimal and optimized for blind and low-vision workflows.

## Screen Layout
- **Greeting text**: "Good morning, Alex" style contextual greeting.
- **Iris orb**: Pulsing when listening or speaking; idle glow otherwise.
- **Hint line**: Rotates through short tips ("Double tap to talk", "Hold for vision", "Single tap to stop").
- No icons, folders, or widgets.

## Gestures + Voice
| Input | Effect |
| --- | --- |
| Double tap anywhere | Start listening immediately. Confirmation tone + "I'm listening". |
| Say "Iris" | Hands-free wake word. |
| Long press (hold) | Enter Vision Mode until release. |
| Single tap | Interrupt speech/output or cancel current action. |

Gestures are global, even when an app is in foreground, by leveraging accessibility overlays.

## Conversation Loop
1. Trigger occurs (double tap or wake word).
2. Iris listens until silence or the user says "stop".
3. Transcript routed to the Action Engine → action plan created.
4. Iris narrates the planned action if confirmation is needed.
5. Accessibility Controller executes while Iris provides progress updates.
6. Iris remains in "follow-up window" for ~8 seconds so the user can issue another request without re-triggering.

## Multimodal Context
- `launcher_context` includes battery level, connectivity, location category (home, transit), and recently used apps.
- Action Engine can factor context ("Play my commute playlist" when `location=commute`).
- Vision Mode availability is surfaced as a state indicator; Iris can say "Hold to enable vision" proactively when sensors detect the user is walking.

## Interrupts + Priority
- Single tap or "Iris, stop" halts speech, cancels pending accessibility actions, and returns to idle.
- Safety-critical alerts (from Vision Mode or device sensors) can pre-empt any interaction. Example: "Obstacle detected ahead" will interrupt music playback.

