# Remotion Live Photo

一个面向 AI Agent 的 Remotion Live Photo / Motion Photo 创作 Skill。

它不只是让 Agent “把图片动起来”，而是指导 Agent 从内容编排、视觉方向、静态海报设计、动作编排、关键帧验收到最终格式转换，完整制作适合小红书、品牌传播和社交媒体发布的高完成度动态卡片。

## 能做什么

- 将文案、图片和品牌信息制作成动态社交媒体卡片
- 在开始制作前让用户选择画幅、数量和视觉风格
- 支持 9 种视觉方向，包括高级杂志、玻璃科技、电影极简、先锋海报等
- 使用 Remotion 编写确定性帧动画，保证预览与最终渲染一致
- 支持用户图片、本地字体、品牌颜色和自定义排版
- 为同一组作品设计不同构图和主动作，避免批量模板换皮
- 输出静态封面、MP4、单文件 Motion Photo 或 iOS Live Photo 文件对
- 单张动效最长不超过 5 秒，并保留稳定终局作为封面

## 工作方式

Agent 使用本 Skill 时，会先询问用户：

1. 画面比例：`3:4`、`4:3`、`1:1`、`16:9` 或 `9:16`
2. 生成数量：需要交付多少张 Live Photo
3. 视觉风格：从预设方向中选择，或由 Agent 根据内容判断

用户确认后，Agent 才会进入设计与制作流程：

```text
内容理解
  ↓
视觉方向与系列编排
  ↓
静态终局海报设计
  ↓
Remotion 动作编排与实现
  ↓
开场 / 动作峰值 / 最终封面关键帧检查
  ↓
渲染封面与 MP4
  ↓
转换为 Motion Photo 或 iOS Live Photo
```

## 技术架构

本项目由四层组成：

### 1. Agent Skill 指令层

[`SKILL.md`](SKILL.md) 定义 Agent 的完整执行流程，包括需求询问、workspace 复用、设计约束、Remotion 实现规范、验收方式和交付格式。

### 2. 视觉与动效规范层

`references/` 包含三份创作规范：

- `visual-direction.md`：视觉方向、排版、字体、颜色、材质和构图规则
- `remotion-choreography.md`：时间结构、动作语法和多图差异化规则
- `quality-gate.md`：关键帧检查、审美评分和技术验收标准

### 3. 可复用 Remotion workspace

`assets/remotion-workspace/` 是一个只读母版。它不是每次创作都要重新安装的完整项目，而是用于首次初始化长期 workspace。

```text
assets/remotion-workspace/
├── package.json
├── public/
│   ├── fonts/
│   └── projects/
├── src/
│   ├── Root.tsx
│   ├── shared/
│   └── projects/
│       ├── registry.ts
│       ├── types.ts
│       └── _template/
└── out/
```

第一次使用时，Agent 将母版复制到用户指定或长期使用的位置，并安装一次依赖。后续所有作品共享同一个 `node_modules`，只新增项目源码、素材和输出：

```text
remotion-livephoto-workspace/
├── node_modules/                  # 所有项目共享，只安装一次
├── public/
│   ├── fonts/                     # 共享字体
│   └── projects/<project-slug>/   # 当前项目素材
├── src/
│   ├── shared/                    # 跨项目工具
│   └── projects/<project-slug>/   # 当前项目场景
└── out/<project-slug>/            # 当前项目全部输出
```

项目通过 `src/projects/registry.ts` 注册，由 `Root.tsx` 统一生成 Remotion Compositions。这样可以长期复用一个轻量工作区，而不是每次创建新的 Remotion 工程。

### 4. Live Photo 格式转换层

[`scripts/mp4_to_livephoto.py`](scripts/mp4_to_livephoto.py) 使用 Python 和 FFmpeg 将 Remotion 渲染的 MP4 转换为：

- **Motion Photo**：视频嵌入 JPEG 的单文件格式，适合多数安卓相册及社交平台
- **iOS Live Photo 文件对**：带匹配元数据的 JPEG + MOV

## 依赖

### 必需环境

| 依赖 | 用途 |
|---|---|
| Node.js 18+ | 运行 Remotion 与 TypeScript 工具链 |
| npm | 安装 workspace 依赖 |
| Python 3.10+ | 初始化 workspace 与转换格式 |
| FFmpeg / ffprobe | 视频转码、裁剪和封面提取 |

### Workspace Node 依赖

母版当前包含：

- `remotion`
- `@remotion/cli`
- `react`
- `react-dom`
- `typescript`
- `@types/react`

版本以 [`assets/remotion-workspace/package.json`](assets/remotion-workspace/package.json) 为准。

### 可选 Python 依赖

导出 iOS Live Photo 文件对时需要：

```powershell
python -m pip install mutagen
```

只导出单文件 Motion Photo 时不需要 `mutagen`。

## 安装为 Agent Skill

克隆仓库后，将仓库目录放到 Agent 可读取的 skills 目录中。例如：

```powershell
git clone https://github.com/Krishnna2725/Remotion-Live-Photo.git remotion-livephoto
```

不同 Agent 的 Skill 目录位置可能不同。安装完成后，可通过类似以下提示调用：

```text
使用 $remotion-livephoto，把这组文案制作成 6 张适合小红书发布的 Live Photo。
```

Skill 会先询问比例、数量和视觉风格，再开始创建内容。

## 首次初始化 Workspace

不要直接在 Skill 内置母版中制作项目或安装依赖。首次使用时，将母版复制到一个长期位置：

```powershell
python <skill-dir>/scripts/init_workspace.py <workspace-root>/remotion-livephoto-workspace
Set-Location <workspace-root>/remotion-livephoto-workspace
npm install
```

安装完成后可验证：

```powershell
npm run typecheck
npm run compositions
npm run studio
```

后续任务应始终复用该 workspace，禁止反复执行 `npm install`、`npx create-video` 或创建新的独立 Remotion 工程。

## 中国大陆网络环境

Agent 在中国大陆环境执行网络命令时，应优先使用国内镜像，并采用**当前命令临时注入**，避免随意修改用户全局配置。

### npm 使用 npmmirror

PowerShell：

```powershell
$env:npm_config_registry="https://registry.npmmirror.com"
npm install
Remove-Item Env:npm_config_registry
```

也可以仅为单次命令指定：

```powershell
npm install --registry=https://registry.npmmirror.com
```

### pip 使用清华镜像

```powershell
python -m pip install mutagen -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Agent 网络规则

1. `npm`、`npx`、`pnpm`、`yarn`、依赖安装和脚手架操作优先使用国内镜像。
2. 不要默认同时启用代理；国内镜像可用时直接使用镜像。
3. 只有目标为海外站点，或国内镜像出现超时、404、连接失败、资源不完整时，才临时启用用户提供的代理。
4. 镜像或代理应尽量只作用于当前命令，不修改全局 npm、Git 或系统网络配置。
5. workspace 已有可用 `node_modules` 时，不应再次安装依赖。

## 创建新项目

每个作品系列都在长期 workspace 中拥有独立项目目录：

```text
src/projects/<project-slug>/
public/projects/<project-slug>/
out/<project-slug>/
```

约束：

- `<project-slug>` 使用小写 kebab-case
- Composition id 使用 `livephoto-<project-slug>-<scene-slug>`
- 用户图片使用 `staticFile()` 和 Remotion `<Img>` 引用
- 所有动画由 `useCurrentFrame()`、`interpolate()`、`spring()` 或 `Sequence` 驱动
- 禁止 CSS transition、CSS animation 和依赖实时状态的非确定性动画
- 多张作品应拥有不同的构图原型、动作命题和主动作

## 常用命令

在长期 workspace 根目录运行：

```powershell
# 查看全部 Composition
npx remotion compositions src/index.ts

# 打开 Remotion Studio
npm run studio

# 检查 TypeScript
npm run typecheck

# 渲染关键帧
npx remotion still livephoto-<project-slug>-<scene-slug> out/<project-slug>/checks/final/<scene-slug>.jpg --frame=60

# 渲染视频
npx remotion render livephoto-<project-slug>-<scene-slug> out/<project-slug>/clips/<scene-slug>.mp4 --codec=h264
```

转换为单文件 Motion Photo：

```powershell
python <skill-dir>/scripts/mp4_to_livephoto.py `
  out/<project-slug>/clips/<scene-slug>.mp4 `
  out/<project-slug>/motion-photos `
  --cover out/<project-slug>/covers/<scene-slug>.jpg `
  --duration 5 `
  --motion-photo
```

转换为 iOS Live Photo 文件对：

```powershell
python <skill-dir>/scripts/mp4_to_livephoto.py `
  out/<project-slug>/clips/<scene-slug>.mp4 `
  out/<project-slug>/ios-live-photo `
  --cover out/<project-slug>/covers/<scene-slug>.jpg `
  --duration 5
```

## 输出结构

```text
out/<project-slug>/
├── checks/
│   ├── start/
│   ├── motion/
│   └── final/
├── covers/
├── clips/
├── motion-photos/
└── ios-live-photo/
```

- `checks/`：设计与动效验收关键帧
- `covers/`：最终稳定帧封面
- `clips/`：Remotion 渲染的 MP4
- `motion-photos/`：单文件 Motion Photo
- `ios-live-photo/`：JPEG + MOV 文件对

## 设计原则

> 先让静态封面成为一张成立的高级海报，再让动效增加空间、情绪和注意力。

本 Skill 强调：

- 一个明确主焦点
- 克制但有表达力的运动
- 可独立成立的最终封面
- 多图之间统一的视觉语言与不同的动作机制
- 可检查、可复现、可稳定渲染的 Remotion 实现

详细规范请阅读 [`SKILL.md`](SKILL.md) 与 `references/`。
