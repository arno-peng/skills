---
name: sketch-to-compose
description: Use when the user wants to convert a Sketch selection or design into Jetpack Compose code, especially for requests like convert to Compose, use Compose to build this UI, or sketch to compose.
---

# Sketch To Compose

Use this skill only when Sketch selection data or screenshots are available.

## Goal

Generate Jetpack Compose UI that closely matches the selected Sketch design.

## Expected Inputs

- a Sketch selection screenshot
- extracted layer data from Sketch
- an optional target file path

If the extracted data is incomplete, fetch missing detail before implementation.

## Workflow

1. Capture the current Sketch selection as an image.
2. Extract accurate layer structure and styling from Sketch.
3. Map the structure into Compose containers and modifiers.
4. Generate Kotlin Compose code.
5. Compare the result against the image and note any deviations.

## Mapping Guidance

- vertical frame/stack -> `Column`
- horizontal frame/stack -> `Row`
- free-positioned frame -> `Box` with offsets or custom layout
- text -> `Text`
- image -> `Image` or `Icon`
- reusable symbol -> reusable `@Composable`
- fills/borders/corners -> `background`, `border`, `RoundedCornerShape`

## Implementation Rules

- Use pure Compose; do not mix in XML layouts.
- Keep dimensions, spacing, font sizes, and ordering aligned with Sketch values.
- Keep modifier ordering readable.
- Extract reusable components when repeated.
- List any required drawable or asset files.
- If exact fidelity is not possible, say where and why.

## Output

If the target path is provided, write the code there. Otherwise present the code and ask where it should go.

Always include:

- complete Compose Kotlin source
- required drawable/resource list
- values worth moving into theme/constants
- known fidelity gaps
