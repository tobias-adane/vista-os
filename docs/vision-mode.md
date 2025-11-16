# Vision Mode

Vision Mode delivers continuous spatial awareness while the user holds the screen. It is optimized for two core scenarios: **navigation** (back camera) and **close-up inspection** (front camera).

## Activation Flow
1. User long-presses anywhere on the launcher.
2. Haptic pulse + Iris prompt: "Visual assistance enabled. I'm looking around."
3. Launcher selects camera:
   - Default to back camera when the device is in motion or the gyroscope indicates it is facing away from the user.
   - Switch to front camera if the user recently requested reading assistance or if the device is angled toward the face (>65° pitch).
4. Frames stream to the Vision Engine until the user releases. Releasing triggers "Visual assistance ended" and stops capture immediately.

## Perception Stack
- **Obstacle Detector** (YOLO/DETR variant) prioritizes floor-level hazards (curbs, stairs, drop-offs, furniture edges).
- **Semantic Segmentation** labels navigational surfaces (sidewalk, road, grass) and architectural features (doors, windows, hallways).
- **People + Pose Estimator** identifies humans, facing direction, and approximate distance.
- **Text Spotter** runs OCR + language model to read signs, screens, and labels.
- **Scene Describer** fuses detections + IMU data to produce concise narratives.

## Output Policy

1. **Safety-first**
   - Immediate callouts for obstacles within 2 meters: "Step down ahead", "Door slightly right".
   - Repeated warnings throttle to once every 3 seconds to avoid spam.
2. **Contextual guidance**
   - After the environment is safe, mention secondary elements ("Person approaching from the left", "You are near a crosswalk").
3. **On-demand questions**
   - User queries ("What does that sign say?") re-prioritize OCR results and temporarily suppress other narrations.
4. **Memory snippets**
   - When the user exits Vision Mode, the last 3-5 insights are stored so the user can ask follow-ups ("What did the sign say again?").

## Privacy Controls
- Frames processed on-device by default; optional relay to secure Iris Cloud for heavy models.
- No persistent recording—only lightweight feature maps are cached for <10 seconds.
- Users can say "Forget that" to immediately purge cached snippets.

