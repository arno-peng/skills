---
name: sketch-to-android-ui-restore
description: Use when the user wants to restore or implement Android UI from a local `.sketch` design in any Android project, including extracting Sketch layout/assets, mapping to existing Android View/XML/Compose code, optionally comparing another platform implementation, validating with emulator or adb screenshots, and producing a visual restoration report. If no local `.sketch` file or absolute path is provided, ask for it before implementation.
---

# Sketch To Android UI Restore

## When To Use

Use this skill when the user asks to restore, implement, convert, or align Android UI from a local Sketch design, for example:

- `UI还原`
- `还原这个 Sketch 到 Android`
- `implement this Sketch UI in Android`
- `sketch to android`
- `pixel align this Android UI with Sketch`

If the user has not provided a local `.sketch` file or absolute path, stop and ask for it first. Do not inspect or edit the Android project before the design source is available.

## Goal

Restore Sketch UI into the target Android project with a complete evidence loop:

- Extract Sketch frame screenshots, layout data, typography, colors, effects, symbols, and assets.
- Identify the target Android screen, component, and implementation style.
- Optionally compare iOS, Web, Figma, or existing product behavior when the user provides or the repo contains a clear reference.
- Implement the smallest Android change that matches the design.
- Build, install, and validate on emulator or adb device whenever available.
- Produce a final report with visible design/device comparisons.

This is an execution workflow, not a one-shot code generator.

## Required Configuration

Infer these from the current workspace when safe. Ask only for values that cannot be discovered and are required to proceed.

| Item | Default handling |
| --- | --- |
| Sketch file | Required. Use the provided upload/path. |
| Android project root | Current repository unless the user points elsewhere. |
| Target screen/component | Infer from Sketch names, user text, repo search, route names, strings, or screenshots. |
| Android UI stack | Detect View/XML/Compose/custom drawing before editing. |
| Reference implementation | Optional. Use iOS/Web/current app only when present and relevant. |
| Host app path | Optional. Needed only when the Android module cannot run by itself. |
| Build command | Infer from Gradle tasks and repo docs; otherwise run the narrowest compile task. |
| Install/launch command | Infer from Gradle install tasks, package name, manifest, or user-provided commands. |
| Device target | Prefer connected adb device; emulator is acceptable. If neither exists, do code/build validation and record the limitation. |

Do not hard-code private project names, sibling directories, package names, branches, or Gradle variants.

## Project Path Inference

Before implementation, try to infer and confirm the Android project root, optional iOS reference project, and optional `dolphinai-and` host app path.

Inference order:

1. Android project root: prefer the current working directory. If it is not an Android/Gradle repository, walk upward until a directory containing `settings.gradle`, `settings.gradle.kts`, `build.gradle`, `build.gradle.kts`, or `gradlew` is found.
2. iOS reference project: prefer a user-provided path. Otherwise search nearby workspace roots for likely iOS projects, including sibling directories, names containing `ios`, and directories containing `.xcodeproj`, `.xcworkspace`, or `Package.swift`.
3. `dolphinai-and` host app: prefer a user-provided path. Otherwise search nearby workspace roots for `dolphinai-and`, including `../dolphinai-and`, same-parent/sibling workspaces, and common local workspace roots when accessible. Prefer the candidate that shares the closest parent directory with the Android project.

If the iOS path cannot be inferred and an iOS reference is needed, ask exactly:

```text
请提供 ios项目的地址
```

If the `dolphinai-and` path cannot be inferred and host-app validation requires it, ask exactly:

```text
请提供dolphinai-and项目地址
```

If both paths are missing, ask both questions. If only one is missing, ask only for that path. After the user provides paths, continue and record the resolved paths in `FINAL_REPORT.md`.

## Source Priority

When Sketch, a reference implementation, and current Android behavior disagree:

| UI area | Rule |
| --- | --- |
| Clear visual design in requested scope | Prefer Sketch. |
| Interaction, data conditions, navigation, accessibility | Prefer the current product implementation or the most authoritative reference. |
| Text | Prefer the product source of truth when it clearly exists; otherwise use Sketch and record uncertainty. |
| Icons/assets | Prefer real project/reference assets; otherwise export from Sketch. Do not invent lookalike assets. |
| Android architecture | Reuse existing components, style tokens, data flow, and resources when compatible with the target visual result. |
| Unresolvable conflicts | Continue with the safest visible match and record the conflict in the report. |

If the user explicitly says to align only a specific Sketch area, visible styling inside that area must be judged against Sketch. Do not use legacy code comments or another platform to override a clear Sketch color, weight, icon shape, or layout.

## Asset Rules

For icons, images, and symbols:

1. Search the Android project and any provided reference implementation for real assets first.
2. If no real asset exists, export the exact layer from Sketch.
3. Do not hand-draw, approximate, or use a similar icon unless the user explicitly approves it.
4. If an asset cannot be obtained, keep the current asset or a clearly marked placeholder, then list the issue in the report.

Export guidance:

- Use Android vector/SVG only for simple flat vectors that preserve the exact shape.
- Use PNG/WebP for bitmap content, masks, alpha-heavy art, gradients, blur, shadows, or complex symbols.
- Record exported/copied assets and their destination paths.

## Data Reproduction

When UI states depend on history, search terms, local lists, scroll position, unread counts, permissions, empty states, or runtime data, construct safe test data directly instead of pausing for confirmation.

Ask the user first only when reproduction would:

- Require schema or business logic changes.
- Modify real shared/production data.
- Need private credentials, verification codes, or external service access.
- Change product scope or expected behavior.

If temporary code data is unavoidable, wrap it and remove it before final validation:

```kotlin
// SKETCH_TO_ANDROID_TEMP_START
// temporary data for Sketch-to-Android visual validation
// SKETCH_TO_ANDROID_TEMP_END
```

Prefer non-code reproduction: typing test queries, clearing local history through UI, using emulator data, debug menus, seeded fixtures, or local-only mocks already supported by the project.

## Workflow

### 1. Preflight

1. Check `git status`, current branch, Android project root, and relevant repo docs.
2. Confirm the Sketch file exists and can be read.
3. Check Sketch MCP availability. If MCP fails, use `sketchtool`, unpacked `.sketch` JSON, or another verifiable local extraction fallback.
4. Resolve Android project root, optional iOS reference path, and optional host app path using "Project Path Inference"; ask for missing required paths with the fixed prompts above.
5. Detect Android stack, target module, build system, and likely screen entry.
6. Check `adb devices` or emulator availability.
7. Create a run directory such as `work/sketch-to-android-ui-restore/<timestamp>/`.
8. Build a queue of the requested Sketch frames. If the user narrowed the scope, filter before implementation.

Do not edit code until the target Sketch frames and Android target are clear.

### 2. Extract Sketch

For every target frame, save:

- Frame/page name, ID, size, order, screenshot path.
- Layer hierarchy, visibility, clipping, masks, opacity, transforms, stack/layout intent, resizing, and pinning.
- Absolute and parent-relative coordinates.
- Text content, font, size, weight, line height, letter spacing, color, alignment, decoration, and rich-text spans.
- Fills, borders, radius, shadows, blur, gradients, alpha, blend mode, tints, and color variable names when available.
- Symbols, nested symbols, overrides, shared styles, and asset candidates.

Keep screenshots and structured extraction outputs in the run directory.

### 3. Inspect Android And References

Read the current Android implementation before changing it:

- Screen/component ownership and entry path.
- Existing resources, dimensions, typography, colors, drawables, strings, and accessibility text.
- Data/state conditions required to show each visual state.
- Existing tests, previews, sample data, and debug tools.

If there is a reference implementation, inspect only the relevant files and record how it influenced decisions.

### 4. Implement Android

Change only the files needed for the requested UI scope.

- Match the existing stack: View/XML stays View/XML, Compose stays Compose, and custom drawing stays local unless the project already mixes patterns.
- Reuse project tokens and components when they produce the target visual result.
- Add resources only when visual restoration needs them.
- Preserve behavior, lifecycle, accessibility, insets, keyboard handling, scrolling, and analytics unless the requested UI requires changes.
- Avoid unrelated refactors.

After each meaningful change, reread the affected code and compare against the extracted Sketch values.

### 5. Build And Device Validate

Run the narrowest reliable checks available:

- Formatting/lint/unit tests when they are local and relevant.
- Gradle compile for the touched module.
- Host app build/install when required to display the UI.
- `git diff --check`.

For device validation:

1. Launch or navigate to the target screen.
2. Reproduce each target state.
3. Capture adb/emulator screenshots.
4. Inspect screenshots before using them in the report.
5. If a screenshot is the wrong state, discard and recapture it.
6. If clicks are unstable, use `adb shell uiautomator dump` and tap control centers.
7. Iterate up to 3 rounds per target frame: build -> install -> navigate -> screenshot -> compare -> fix.

If video capture is unavailable, use slowed animations or repeated screenshots and record the fallback.

## Visual Comparison Rules

For each target frame, check:

- Layout, position, dimensions, padding, margins, alignment, and responsive behavior.
- Typography, color, weight, line height, truncation, wrapping, and dynamic rich-text spans.
- Icon source, shape, color, size, spacing, negative margins, and text overlap.
- Images, masks, rounded corners, borders, shadows, blur, opacity, and gradients.
- Empty/loading/error/result states, keyboard/inset behavior, scroll position, and animation keyframes.

Do not mark a frame complete if:

- A design icon is replaced by text or a Unicode character.
- Text is clipped, hidden under an icon, or wrongly ellipsized.
- Rich text differs visibly, such as blue highlight when Sketch expects black bold text.
- Only an entry/helper screenshot exists but the target state itself was not captured.

Save crop or zoom evidence for critical small details when needed; the final report can show scaled images, but validation must inspect the original screenshots.

## Temporary Data Cleanup

Before finishing:

- Search for `SKETCH_TO_ANDROID_TEMP`.
- Remove all temporary code data.
- Rebuild if the removal could affect compilation.
- State in the final report whether temporary code data was used and removed.

## Final Report

Create `FINAL_REPORT.md` in the run directory.

The report should include:

- Summary of handled Sketch frames and validated device states.
- Processed and skipped frames, with reasons.
- Code/resource changes.
- Build/install/test results.
- Device, emulator, adb, or launch limitations.
- A one-to-one comparison table: Sketch image, device image, status, and notes.
- Critical-area checklist covering all areas visible in the requested scope.
- Rich-text/dynamic style validation when relevant.
- Remaining visual differences and questions.
- Asset issues and any user-provided follow-up needed.
- Temporary test data cleanup status.

Report rules:

- Use the user's language when clear; if the user requests Chinese, write the report in Chinese.
- Markdown images must use absolute local paths so previews render reliably.
- Default all report screenshots to `width="400"`.
- Sketch and device screenshots in the same comparison table must use the same display width unless the user explicitly requests otherwise.
- Every target Sketch frame must have a corresponding target device/emulator screenshot or an explicit explanation of why validation was impossible.
- Status and notes must be specific, not generic phrases like "handled" or "pending".

Only notify the user after the final report is written.
