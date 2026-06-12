---
name: sketch-to-android
description: "当用户说“UI还原”“UI 还原”“还原 UI”，并上传或提供本地 `.sketch` 设计稿文件时使用。用于将 Sketch 设计稿像素级还原到 Android 项目，包括提取 Sketch 布局与素材、对比 iOS 实现、修改 Android SDK UI、通过 dolphinai-and 宿主 App 编译安装并用 adb 真机截图验证，最后输出复原报告。如果没有本地设计稿文件，必须先向用户索要 `.sketch` 文件后再执行。"
---

# Sketch To Android

## 触发条件

当用户同时满足以下条件时使用本 skill：

- 明确提到 `UI还原`、`UI 还原`、`还原 UI`、`sketch 还原 Android` 等意图。
- 上传了本地 `.sketch` 文件，或提供了本地 `.sketch` 文件绝对路径。

如果用户只说要 UI 还原，但没有上传或提供本地 `.sketch` 设计稿文件，必须先停止并向用户索要设计稿文件：

```text
请先上传本地 `.sketch` 设计稿文件，或提供它的绝对路径。我拿到设计稿后再开始 UI 还原流程。
```

在拿到本地 `.sketch` 文件前，不要开始读取 Android/iOS 代码、不要改代码、不要编译。

## 目标

将 Sketch 设计稿像素级还原到 Android 项目，并形成完整验证闭环：

- 通过 Sketch MCP 提取设计稿的精确 UI 信息。
- 读取并分析当前 Android SDK 实现。
- 读取并分析对应 iOS 实现，在需要时以 iOS 作为对齐基准。
- 按项目现有架构实现 Android UI。
- 通过 `../dolphinai-and` 宿主 App 编译、安装到 adb 真机并截图对比。
- 为每张设计图和最终结果保存复原记录。

这是一个执行型 workflow，不是简单的 Sketch 转代码工具。

## 项目路径约定

默认从 `siuper-sdk-android` 仓库根目录执行。

相关项目路径：

- Android SDK 修改目标：`.`
- Android 宿主 App 编译与真机验证项目：`../dolphinai-and`
- iOS 参考项目：`../../Siuper_ios`

开始执行前必须确认路径存在：

```bash
test -d ../dolphinai-and
test -d ../../Siuper_ios
```

Android UI 代码修改发生在当前 `siuper-sdk-android` 仓库中。
编译、安装、真机截图验证必须从 `../dolphinai-and` 执行。
iOS 对照实现默认从 `../../Siuper_ios` 读取。

## 信息源优先级

当 Sketch、iOS、Android 当前实现不一致时，按照下面规则处理：

| UI 类型 | 处理规则 |
| --- | --- |
| 文案 | iOS 与 Sketch 不一致时，使用 iOS 文案，并记录差异。 |
| icon / 素材 | 优先使用 iOS 真实资源；否则从 Sketch 导出真实资源；如果拿不到真实资源，禁止手绘或相似替代，只记录问题等待用户统一解决。 |
| 布局、尺寸、间距、字体、颜色、圆角、阴影、状态 | iOS 有真实实现时，像素级对齐 iOS；否则使用 Sketch 提取值。 |
| Android 项目架构 | 在不影响视觉还原的前提下，优先复用已有组件、token、样式和数据流。 |
| Sketch / iOS 无法判断的冲突 | 不要每张图都打断用户，先记录，等所有页面处理完后统一让用户确认。 |

## Icon 与素材规则

icon / 素材处理必须遵守以下规则：

1. 优先使用 iOS 项目中能直接定位到的真实资源。
2. 如果 iOS 没有可直接复用资源，再尝试从 Sketch MCP 导出真实图层资源。
3. 如果 iOS 和 Sketch 都无法拿到可确认的真实素材，禁止手绘、禁止凭理解重画、禁止用相似 icon 替代。
4. 遇到无法获取素材的 icon，必须：
   - 保留当前 Android 资源或临时占位，不做主观还原。
   - 在单图报告中记录 icon 名称、所在页面、图层 ID、截图位置、尝试过的资源路径。
   - 在 `FINAL_REPORT.md` 的“需要用户协助解决的问题”中列出。
   - 等用户统一提供或确认资源后再处理。

素材导出规则：

- 简单纯矢量图案，且不依赖透明、阴影、复杂渐变、蒙版时，可以导出 SVG 或转换为 Android vector。
- 包含透明度、位图内容、复杂渐变、蒙版、模糊、阴影的素材，导出 PNG 或 WebP。
- 不允许手绘或临时画一个近似 icon 代替真实资源。

## 必要输入

开始实现前，需要确认或自行解析以下信息：

- 本地 `.sketch` 设计稿文件：用户上传的文件，或用户提供的本地绝对路径。
- Android SDK 中对应页面、组件或入口代码。
- iOS 中对应页面或组件代码。
- 设计图处理范围：全部处理、只处理指定图、或过滤某些图。
- adb 已连接的真机，用于最终截图验证。
- `../dolphinai-and` 可正常以源码模式依赖当前 SDK。

如果某项依赖缺失，但不阻塞当前阶段，可以继续执行，并在报告中记录限制。

## 预检流程

1. 检查当前仓库路径、分支和 `git status`。
2. 确认 `../dolphinai-and` 和 `../../Siuper_ios` 存在。
3. 确认 `../dolphinai-and/local.properties` 包含：

```properties
siuperSourceMode=true
siuper.project.dir=../siuper-sdk-android
```

4. 确认 Sketch MCP 可用，再依赖 Sketch 数据。
5. 使用 `adb devices` 确认真机连接。
6. 创建工作目录，例如：
   `work/sketch-to-android/<timestamp>/`
7. 从 Sketch 建立待处理设计图队列。
8. 如果用户指定了过滤规则，先过滤，再开始逐张处理。

在 Sketch 目标、Android 目标和 iOS 参考策略明确前，不要直接改代码。

## 单张设计图处理流程

每次只处理一张 Sketch 图。完成它的提取、分析、实现、代码检查和记录后，再进入下一张。

### 1. 提取 Sketch 数据

通过 Sketch MCP 获取当前 frame 的结构化数据和视觉参考图。

至少需要提取：

- 页面 / frame 名称、ID、尺寸、顺序、截图路径。
- 完整图层结构、可见性、层级顺序、裁剪、蒙版、透明度、transform。
- 相对父容器和绝对坐标下的位置与尺寸。
- Stack / layout 意图、resizing、pinning、约束信息。
- 文本内容、字体、字号、字重、是否加粗、行高、字间距、对齐方式、装饰。
- 颜色值、颜色 token、swatch 名称、library 来源、alpha、渐变、蒙层、blend mode、滤镜、透明度。
- 边框、圆角、阴影、模糊、tint、mask。
- symbol、嵌套 symbol、override、shared style。
- 图片 / icon 图层和可导出素材。

### 2. 分析 Android 当前实现

读取当前 Android 页面或组件实现。

对比并记录：

- 现有组件结构。
- 现有尺寸、margin、padding、constraint。
- 现有文字样式和颜色 token。
- 现有 drawable / icon 资源。
- 控件展示所需的数据条件和状态。

如果项目已有组件、token 或样式可以满足视觉要求，优先复用。

### 3. 分析 iOS 实现

默认从 `../../Siuper_ios` 查找对应页面或组件实现。

优先搜索：

- 页面名称、Sketch frame 名称、业务关键词。
- 文案。
- icon / resource 名称。
- view controller / SwiftUI view / reusable cell / component。
- image asset catalog。

对比 iOS 与 Sketch，并记录：

- 文案差异。
- icon / 资源差异。
- 布局、间距、字体、颜色差异。
- 交互和状态差异。

按照“信息源优先级”决定 Android 最终采用值。无法判断的冲突，记录到待确认列表。

### 4. 实现 Android

只针对当前设计图涉及的页面或组件做改动。

规则：

- 保持 diff 尽量小。
- 遵循项目已有代码风格和架构。
- 优先复用已有组件、token、样式和资源。
- 只有视觉还原需要时才新增资源。
- icon 和图片资源必须按 Icon 与素材规则处理。
- 避免无关重构。
- 如果为了展示 UI 需要临时构造测试数据，必须使用下面注释包裹：

```kotlin
// SKETCH_TO_ANDROID_TEMP_START
// temporary data for Sketch-to-Android visual validation
// SKETCH_TO_ANDROID_TEMP_END
```

### 5. 代码层面自检

进入下一张图前，必须检查当前改动：

- 重新读取改动后的 Android 代码。
- 对比 Sketch / iOS 记录，确认尺寸、颜色、字体、素材引用是否一致。
- 检查资源命名、drawable 引用、颜色和尺寸 token。
- 记录当前仍然存在的差异或风险。

### 6. 保存单图报告

在工作目录中为每张图保存报告，内容包括：

- Sketch 截图和提取摘要。
- Android 修改前后分析。
- iOS 对比分析。
- 最终采用值和原因。
- 导出或复制的素材清单。
- 无法获取的 icon / 素材问题。
- 待确认问题。
- 是否已准备好进入真机验证。

## 编译与安装规则

Android SDK 代码修改完成后，真实设备验证必须构建宿主 App `../dolphinai-and`。

从当前 `siuper-sdk-android` 仓库执行时，使用：

```bash
cd ../dolphinai-and
```

常用命令：

```bash
# 快速源码编译检查
./gradlew :app:compileSitArm64DebugSources

# 构建 debug APK
./gradlew :app:assembleSitArm64Debug

# 安装到 adb 连接的真机
./gradlew :app:installSitArm64Debug
```

预期 APK 路径：

```text
app/build/intermediates/apk/sitArm64/debug/app-sit-arm64-debug.apk
```

如果构建遇到 `com.hualin.component`、`HLBase`、`HLOfflineWeb`、`offlinewebsdk` 等私有依赖问题，先检查 `../dolphinai-and/tools/maven_local/` 和本机 `~/.m2/repository`，不要立即判断为 UI 代码问题。

## 所有设计图处理完成后

1. 运行当前模块适用的格式化、lint 或编译检查。
2. 进入 `../dolphinai-and`。
3. 编译 `:app:assembleSitArm64Debug` 或直接执行 `:app:installSitArm64Debug`。
4. 通过项目代码分析目标页面进入链路。
5. 使用 adb 操作真机进入对应页面。
6. 如果因为缺少数据导致控件不显示，可以临时构造测试数据，但必须使用 `SKETCH_TO_ANDROID_TEMP` 注释。
7. 为每个目标页面截图。

## 真机截图对比

对每个页面逐个执行：

1. 将真机截图与 Sketch 参考图、单图目标记录进行对比。
2. 重点检查布局、位置、尺寸、字体、颜色、圆角、阴影、icon、可见性和状态。
3. 发现差异后修复，并重复：
   编译 -> 安装 -> 进入页面 -> 截图 -> 对比。
4. 同一张图最多修复 3 轮。
5. 如果 3 轮后仍无法符合预期，记录问题并跳过，等待用户介入。

## 临时测试数据清理

最终完成前必须：

- 搜索 `SKETCH_TO_ANDROID_TEMP`。
- 删除所有临时测试数据。
- 如果临时测试数据影响编译结果，删除后重新构建。
- 最终报告中必须说明是否添加过临时测试数据，并确认已全部删除。

## 最终报告

在工作目录中创建 `FINAL_REPORT.md`。

内容包括：

- 已处理设计图列表。
- 被跳过设计图列表和原因。
- 每张图的复原状态。
- 真机截图路径。
- 剩余视觉差异。
- Sketch / iOS 冲突项。
- 无法获取的 icon / 素材清单。
- 需要用户协助确认的问题。
- 页面进入链路、数据缺失、adb 或设备问题。
- 构建和安装验证结果。
- 临时测试数据是否已全部删除。

只有最终报告写完后，才通知用户。
