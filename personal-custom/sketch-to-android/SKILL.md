---
name: sketch-to-android
description: Use when the user wants to convert a Sketch selection or design into Android Kotlin View code, especially for requests like implement this UI, convert to Android, sketch to code, or generate Android UI from Sketch.
---

# Sketch To Android

Use this skill only when Sketch selection data or screenshots are available.

## Goal

Generate Android UI code that closely matches the selected Sketch design using classic View-based Kotlin, not Compose.

## Expected Inputs

- a Sketch selection screenshot
- extracted layer data from Sketch
- an optional target file path

If the selection data is incomplete, fetch more detail before writing code.

## Workflow

1. Capture the current Sketch selection as an image.
2. Extract precise layer data from Sketch, including frame, text, fills, borders, shadows, radii, stack layout, and symbol expansion.
3. Map the structure into Android Views.
4. Generate Kotlin UI code.
5. Compare the result against the captured image and list any gaps.

## Mapping Guidance

- vertical frame/stack -> `LinearLayout(VERTICAL)`
- horizontal frame/stack -> `LinearLayout(HORIZONTAL)`
- free-positioned frame -> `ConstraintLayout` or `FrameLayout`
- text -> `TextView`
- image -> `ImageView`
- filled shape -> `View` with `GradientDrawable`
- reusable symbol -> custom `View` or helper builder

## Implementation Rules

- Use pure Kotlin View code; do not output XML.
- Keep dimensions and spacing aligned with Sketch values.
- Preserve layer order.
- Put colors into `colors.xml` rather than hard-coding them in Kotlin.
- If design assets are required, list the drawable files that must be created.
- If a detail cannot be reproduced exactly, state it explicitly.

## Output

If the target path is provided, write the code there. Otherwise present the code and ask where it should go.

Always include:

- complete Kotlin source
- required drawable/resource list
- colors or dimensions worth centralizing
- known fidelity gaps

