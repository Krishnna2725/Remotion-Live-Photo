---
name: remotion-livephoto
description: 用 Remotion 独立策划、设计、实现并导出高审美 Live Photo / Motion Photo。适用于用户要求制作 live 图、实况照片、livephoto、小红书动态封面、品牌动态海报、产品微动效或把静态视觉做成高级短循环动图时；覆盖视觉方向、构图、Remotion 帧动画、关键帧验收和单文件或 iOS 双文件交付。
---

# Remotion Live Photo

把 Live Photo 当作一张会呼吸的高级海报：**静态封面先成立，动效只负责增加空间、情绪和注意力。**

## 自主执行原则

- 开始制作前，必须先一次性询问用户画面比例、需要生成的 Live Photo 数量和视觉风格。用户确认后直接完成设计、实现、预览检查、渲染与转换。
- 不要在首次询问用户之前扫描当前目录。用户确认需求后，使用同一个长期复用的 Remotion workspace；第一次初始化一次，后续任务只新增项目模块、素材和输出。
- 新建或修改 Remotion 项目时，遵守确定性渲染：所有动画由 `useCurrentFrame()`、`interpolate()`、`spring()` 或 `Sequence` 驱动。禁止 CSS transition、CSS animation 和 Tailwind animation class。
- 先把最终静态画面设计好，再设计抵达该画面的动作。封面使用最终稳定帧。
- 只用动效强化层级。不要为了“看起来复杂”堆叠粒子、旋转、弹跳或多段转场。

## 第一步：询问用户

在执行任何文件扫描、设计或代码工作前，一次性询问以下三项。必须展示选项，不要只问开放问题。

1. **画面比例**
   - `3:4 竖版（推荐）`：1080 × 1440，适合小红书和社交平台
   - `4:3 横版`：1440 × 1080
   - `1:1 方形`：1080 × 1080
   - `16:9 宽屏`：1920 × 1080
   - `9:16 全屏竖版`：1080 × 1920

2. **生成数量**
   - 明确询问“需要生成多少张 Live Photo？”
   - 提供 `1 张 / 3 张 / 5 张 / 自定义数量`
   - 这里的数量指最终交付的 Live Photo 数量，不是用户提供的素材数量。

3. **视觉风格**
   - `01 Ethereal Glass`：深色玻璃、空间光晕、未来科技
   - `02 Editorial Luxury`：高级杂志、衬线大字、克制留白
   - `03 Soft Structuralism`：银灰极简、柔和结构、产品感
   - `04 Neo-Brutalist Poster`：大胆排版、强烈色块、先锋海报
   - `05 Cinematic Minimalism`：电影质感、暗调摄影、缓慢镜头
   - `06 Y2K Chrome`：液态金属、闪光、高能数字美学
   - `07 Organic Tactile`：自然材质、纸张纹理、温暖手作感
   - `08 Brand Gradient`：品牌渐变、明亮传播、社交媒体友好
   - `09 AI Chooses`：由 agent 根据内容选择最合适的方向

风格菜单的完整设计规则见 [references/visual-direction.md](references/visual-direction.md)。用户已在当前消息明确给出某一项时，只询问缺失项，不重复追问。

首次提问模板：

```text
开始制作前，请确认三个选项：
1. 画面比例：3:4 竖版（推荐）/ 4:3 横版 / 1:1 方形 / 16:9 宽屏 / 9:16 全屏竖版
2. 生成数量：1 张 / 3 张 / 5 张 / 自定义数量
3. 视觉风格：01 Ethereal Glass / 02 Editorial Luxury / 03 Soft Structuralism /
   04 Neo-Brutalist Poster / 05 Cinematic Minimalism / 06 Y2K Chrome /
   07 Organic Tactile / 08 Brand Gradient / 09 AI Chooses
```

## 用户确认后

1. 检查 `node`、`ffmpeg`、`ffprobe`、Python；双文件 iOS Live Photo 还需 `mutagen`。
2. 定位并验证长期复用的 Remotion workspace：
   - 优先使用用户指定的 workspace。
   - 否则查找同时包含 `package.json`、`src/projects/registry.ts` 和 `node_modules` 的目录。
   - 从候选目录执行 `npx remotion compositions src/index.ts`，验证通过后复用。
3. 若 workspace 不存在，使用 skill 内置母版初始化一次：

```powershell
python <skill-dir>/scripts/init_workspace.py <workspace-root>/remotion-livephoto-workspace
Set-Location <workspace-root>/remotion-livephoto-workspace
$env:npm_config_registry="https://registry.npmmirror.com"
npm install
```

4. 后续任务始终复用该 workspace：
   - 源码：`src/projects/<project-slug>/`
   - 素材：`public/projects/<project-slug>/`
   - 输出：`out/<project-slug>/`
5. 将用户素材放进项目素材目录，用 `staticFile()` 引用；图片使用 Remotion 的 `<Img>`。

### Workspace 结构

skill 内的 `assets/remotion-workspace/` 是只读母版。首次复制并安装依赖后，后续所有任务只向长期 workspace 增加项目：

```text
remotion-livephoto-workspace/
├── node_modules/                  # 共享依赖，只安装一次
├── public/
│   ├── fonts/                     # 共享字体
│   └── projects/<project-slug>/   # 当前项目素材
├── src/
│   ├── shared/                    # 真正跨项目复用的小型工具
│   └── projects/
│       ├── registry.ts
│       └── <project-slug>/        # 当前项目场景与 Composition
└── out/<project-slug>/
    ├── checks/start/
    ├── checks/motion/
    ├── checks/final/
    ├── covers/
    ├── clips/
    ├── motion-photos/
    └── ios-live-photo/
```

每次新任务：

1. 使用小写 kebab-case 创建 `<project-slug>`。
2. 创建 `src/projects/<project-slug>/`，并在 `src/projects/registry.ts` 注册。
3. 仅在需要素材时创建 `public/projects/<project-slug>/`。
4. 所有输出写入 `out/<project-slug>/`，不得混入其他项目。
5. Composition id 使用 `livephoto-<project-slug>-<scene-slug>`。
6. 封面和视频使用相同 basename，例如 `01-cover.jpg` 与 `01-cover.mp4`。

### 依赖纪律

- workspace 已初始化时，禁止执行 `npm install`、`npx create-video` 或创建新的独立 Remotion 工程。
- `npx remotion ...` 必须从长期 workspace 目录执行，使其使用共享的本地依赖。
- 不要把“当前工作目录不是 Remotion 项目”误判为“本机没有部署 Remotion”；应定位长期 workspace。
- skill 内的 `assets/remotion-workspace/` 是只读母版，不要直接在母版中制作用户项目或安装依赖。
- 新增第三方 Remotion 包确有必要时，只安装缺失包，并先说明用途。

### 中国大陆网络环境

- 执行 `npm`、`npx`、`pnpm`、`yarn`、`pip`、脚手架或依赖安装时，优先使用国内镜像。
- npm 优先使用命令级参数 `--registry=https://registry.npmmirror.com`，或为当前进程临时设置 `npm_config_registry`。
- pip 优先使用命令级参数 `-i https://pypi.tuna.tsinghua.edu.cn/simple`。
- 不要为了安装依赖默认启用代理，也不要轻易修改 npm、Git、pip 或系统的全局配置。
- 仅当目标本身是海外站点，或国内镜像超时、404、连接失败、资源不完整时，才临时使用用户提供的代理；操作结束后恢复镜像优先策略。
- Remotion 首次执行 Composition 枚举或渲染时，可能从海外地址下载 Chrome Headless Shell。先允许首次下载完成；若国内网络无法连接，再仅为该命令临时使用用户提供的代理。
- workspace 已有可用 `node_modules` 时，不执行任何网络安装命令。

## 工作流

### 1. 定义创意

读取 [references/visual-direction.md](references/visual-direction.md)，根据用户选择的风格建立 design brief、视觉系统和构图原型。若选择 `AI Chooses`，根据内容类型和情绪选择一个方向，并在交付时说明选择。

生成多张时，先为每张分别写出：

- 独立的 composition archetype
- 独立的 motion thesis
- 独立的 hero motion

禁止创建一个主场景组件，然后只替换文案、主题色、序号或中心装饰物来批量生成。系列感应来自字体、内容逻辑和设计系统，而不是六张共享同一模板。

默认规格：

- 竖版社交平台：`1080 × 1440`
- 横版：`1440 × 1080`
- 方形：`1080 × 1080`
- `30fps`，推荐总时长 `60-90` 帧；单张最长不超过 `5s`（150 帧）
- 最后 `10-15` 帧完全稳定，作为封面与阅读停留

### 2. 设计静态终局

先实现最终稳定帧，并检查：

- 1 个主焦点，最多 2 个辅助焦点
- 文案层级清晰，标题通常不超过两行
- 大留白与非对称张力成立
- 色彩、字体、纹理和容器风格属于同一视觉世界
- 缩小到 25% 后仍能快速读懂

不要机械照搬网页 UI。Live Photo 是短时动态海报，不需要导航栏、hover、移动端断点或交互控件。

### 3. 编排动作

读取 [references/remotion-choreography.md](references/remotion-choreography.md)，为场景建立 3 个阶段：

1. **Recognition**：开头短暂停留，让观众识别主体。
2. **Reveal**：用 1 个主动作和 1-2 个辅助动作建立层级。
3. **Resolve**：全部元素落定，保留稳定封面帧。

动作优先级：镜头微推拉 / 主体视差 > 标题揭示 > 光影或纹理呼吸 > 装饰动作。

### 4. 实现 Remotion

- 开始写场景代码前读取 [references/motion-recipes.md](references/motion-recipes.md)，根据视觉方向选择一个主动作配方和最多两个辅助配方。
- 在长期 workspace 内创建 `src/projects/<project-slug>/`，并注册到 `src/projects/registry.ts`。
- Composition id 使用 `livephoto-<project-slug>-<scene-slug>`。
- 不要创建新的 `package.json`、`node_modules`、`src/Root.tsx` 或独立 Remotion 工程。
- 优先复用 `src/shared/motion-primitives.tsx` 中的 `MaskReveal`、`StaggerWords`、`ParallaxImage`、`LightSweep`、`FilmGrain` 和 `HighlightWipe`，再为作品编写独特构图。
- 把视觉 token、时间 token 和组件分离，避免散落魔法数字。
- 共享同一时机的属性先计算一个 `progress`，再映射到 `opacity`、`transform` 等属性。
- 动画优先使用 `transform` 和 `opacity`；避免逐帧改变昂贵的大面积 blur。
- 使用 `@remotion/fonts` 加载本地字体；仅在网络条件合适时使用 `@remotion/google-fonts`。不要依赖系统恰好安装的字体。
- 可变文案存在溢出风险时，使用 `@remotion/layout-utils` 的 `measureText()`、`fitText()` 或 `fillTextBox()`，并确保字体已加载。
- 使用 `<Sequence>` 编排独立阶段时设置 `premountFor`；记住 Sequence 内 `useCurrentFrame()` 从 0 开始。
- 随机视觉必须使用 Remotion `random()` 和稳定 seed，禁止 `Math.random()`。
- 在写主构图前明确字体方案并验证加载成功。中文展示字体不得默认使用微软雅黑、黑体等系统默认字体充当设计字体。
- 让第 0 帧可观看，让最终稳定帧成为最强画面。

### 5. 视觉与技术验收

读取 [references/quality-gate.md](references/quality-gate.md)。至少渲染并检查三个关键帧：

```powershell
npx remotion compositions src/index.ts
npx remotion still livephoto-<project-slug>-<scene-slug> out/<project-slug>/checks/start/<scene-slug>.jpg --frame=0
npx remotion still livephoto-<project-slug>-<scene-slug> out/<project-slug>/checks/motion/<scene-slug>.jpg --frame=36
npx remotion still livephoto-<project-slug>-<scene-slug> out/<project-slug>/checks/final/<scene-slug>.jpg --frame=<最终稳定帧>
```

检查图片时，确认开场不残缺、中段不碰撞、终局可独立当海报。发现问题就修改并重新检查，不要把首次渲染直接交付。

### 6. 渲染与转换

```powershell
npx remotion still livephoto-<project-slug>-<scene-slug> out/<project-slug>/covers/<scene-slug>.jpg --frame=<最终稳定帧>
npx remotion render livephoto-<project-slug>-<scene-slug> out/<project-slug>/clips/<scene-slug>.mp4 --codec=h264
python <skill-dir>/scripts/mp4_to_livephoto.py out/<project-slug>/clips/<scene-slug>.mp4 out/<project-slug>/motion-photos --cover out/<project-slug>/covers/<scene-slug>.jpg --duration 5 --motion-photo
```

默认交付单文件 Motion Photo `clip.jpg`，适用于小红书、Windows 11 照片和多数安卓相册。

iOS 双文件交付时去掉 `--motion-photo`，输出配对的 JPEG + MOV。不要声称已兼容某个平台，除非已在目标平台实际验证；应表述为“按该格式导出”。

不得把不同项目的检查图、封面、MP4 和 Motion Photo 混在同一目录。

## 完成标准

- 静态封面本身像完成度高的设计作品
- 多张作品拥有统一系列语言，但构图和主动作不是模板换皮
- 动效有明确节奏，且不会抢走内容
- 所有帧由 Remotion 确定性驱动
- 开始、中间、封面关键帧均已检查
- Composition 枚举和完整渲染成功
- Live Photo / Motion Photo 转换成功，并明确交付路径与格式
