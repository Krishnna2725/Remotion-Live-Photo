# Quality Gate

## 关键帧检查

至少查看开场帧、动作峰值帧和最终封面帧。必要时再检查文字进入和主体落位的临界帧。

### 开场帧

- 第 0 帧可观看，不像加载失败
- 主体已可识别
- 没有文字被裁掉或元素悬在尴尬位置

### 动作峰值帧

- 元素不碰撞、不穿帮、不超出安全区
- 同时运动的焦点不超过三个
- 模糊、发光、阴影没有脏边或明显性能风险

### 最终封面帧

- 单独看像完整海报
- 标题、主体、辅助信息层级明确
- 缩小到 25% 仍可识别
- 没有依赖“正在运动”才能成立的构图

## 审美评分

每项 0-2 分，总分低于 8 分则继续修改：

| 项目 | 0 | 1 | 2 |
|---|---|---|---|
| 焦点 | 混乱 | 可辨 | 一眼明确 |
| 层级 | 扁平 | 基本清楚 | 比例与空间有张力 |
| 一致性 | 风格冲突 | 大致统一 | 材质、字体、色彩统一 |
| 动效 | 装饰性堆叠 | 基本顺畅 | 强化叙事且克制 |
| 封面 | 不能独立成立 | 可用 | 像完成度高的海报 |

## 技术检查

```powershell
npx remotion compositions src/index.ts
npx remotion render livephoto-<project-slug>-<scene-slug> out/<project-slug>/clips/<scene-slug>.mp4 --codec=h264
ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 out/<project-slug>/clips/<scene-slug>.mp4
```

- Composition 可枚举
- 渲染无报错、无缺失素材、无字体闪动
- H.264 输出可播放，单张时长不超过 5 秒
- 封面尺寸与视频尺寸一致
- 转换脚本成功产生目标格式
- 源码、素材和输出遵守 workspace 结构规范

## 交付说明

报告：

- 视觉方向和核心动作，各用一句话说明
- Composition id、尺寸、fps、时长
- 输出文件的绝对路径
- 输出为单文件 Motion Photo 还是 iOS JPEG + MOV
- 实际完成的验证，不夸大平台兼容性
