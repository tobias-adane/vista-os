# Action Plan Schema

The Action Engine emits structured plans so that downstream executors can act deterministically, even when the original user request was ambiguous or conversational.

```json
{
  "intent": "send_message",
  "confidence": 0.92,
  "metadata": {
    "app": "WhatsApp",
    "context": "follow_up"
  },
  "slots": {
    "recipient": "Sam",
    "content": "I'll be there in ten minutes."
  },
  "steps": [
    { "op": "open_app", "args": { "name": "WhatsApp" } },
    { "op": "find_contact", "args": { "name": "Sam" } },
    { "op": "open_conversation" },
    { "op": "type_text", "args": { "text": "I'll be there in ten minutes." } },
    { "op": "send" }
  ],
  "confirm": false,
  "follow_up": {
    "expected": true,
    "prompt": "Message sent. Anything else?"
  }
}
```

## Required Fields
- `intent`: Canonical verb phrase (e.g., `send_message`, `call_contact`, `read_screen`).
- `confidence`: Float 0-1 used by Iris to determine whether to confirm or silently execute.
- `metadata`: Execution hints (preferred app, language, device target).
- `slots`: Argument dictionary extracted from the utterance + context.
- `steps`: Ordered list of operations the Accessibility Controller knows how to execute.

## Operations Catalog (initial)

| op | Description | Notes |
| --- | --- | --- |
| `open_app` | Launch an app via package name or deep link | falls back to Accessibility search |
| `find_contact` | Search contacts using local index | uses fuzzy matching + recency |
| `open_conversation` | Focus messaging field in the current app | |
| `type_text` | Type or paste dictated content | text normalized for punctuation |
| `send` | Activate the primary send button | requires UI affordance detection |
| `call_contact` | Start a phone call | may confirm before dialing |
| `toggle_setting` | Change system setting (Wi-Fi, Bluetooth, flashlight, etc.) | includes desired state |
| `read_screen` | Perform OCR + semantics on current screen | returns structured summary |
| `launch_vision_mode` | Switch to Vision Mode | ensures audio prompt fires |

## Confirmation Policy

- Low confidence (<0.7) → Iris summarizes the plan and asks for confirmation.
- High-risk intents (payments, deletions) always require explicit confirmation, even if confidence is high.
- Users can opt into "always confirm" via accessibility settings.

## Error Reporting

Executors send `step_result` events (`success`, `retryable_error`, `fatal_error`). Iris narrates failures with remediation tips ("WhatsApp isn't installed. Should I send via SMS instead?").

