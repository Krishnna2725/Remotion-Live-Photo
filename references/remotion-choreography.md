# Remotion Choreography

## 时间结构

以 75 帧、30fps 为稳妥默认值：

| 阶段 | 帧 | 目标 |
|---|---:|---|
| Recognition | 0-5 | 第 0 帧可观看，快速建立主体 |
| Reveal | 6-48 | 主动作完成，辅助动作错峰抵达 |
| Resolve | 49-59 | 微小运动衰减，画面收束 |
| Poster hold | 60-74 | 完全稳定，供阅读和封面提取 |

短内容可压缩 Reveal，但 Poster hold 不少于 10 帧。

## 动作语法

- 主体：`scale 0.96 → 1`、`translate 20-60px → 0`，只选一种主方向。
- 标题：使用遮罩揭示、字行错峰或轻微 fade-up；不要逐字乱跳。
- 辅助信息：比标题晚 4-10 帧进入，距离更短。
- 光影：低幅位移或透明度变化，最终必须稳定。
- 摄影素材：使用缓慢 Ken Burns 或分层视差；避免明显旋转和过度放大。

## 多张作品的动作差异

为同一系列生成多张 Live Photo 时，每张选择不同的主动作机制，例如：

- kinetic typography：大字切片、遮罩或方向性进入
- editorial collage：图块错层、旋转落位、纸张揭示
- timeline choreography：播放头推进、轨道填充、阶段展开
- ratio morph：画幅变形、重新构图、尺寸关系变化
- cascade：多元素按顺序级联落位
- merge / assembly：多个对象组合成最终对象

系列作品可以共享 timing helpers、字体和颜色 token，但禁止共享完整主构图后只替换内容。最终检查中段帧；如果不同作品在中段具有近似轮廓和运动方向，继续重做。

## 推荐曲线

```tsx
import {Easing, interpolate} from "remotion";

const progress = interpolate(frame, [6, 42], [0, 1], {
  easing: Easing.bezier(0.16, 1, 0.3, 1),
  extrapolateLeft: "clamp",
  extrapolateRight: "clamp",
});
```

- 精确减速：`Easing.bezier(0.16, 1, 0.3, 1)`
- 柔和编辑感：`Easing.bezier(0.45, 0, 0.55, 1)`
- 少量强调弹性：`Easing.bezier(0.34, 1.3, 0.64, 1)`，每个场景最多用于一个焦点

不要用 CSS animation 或 transition。不要依赖随机数；确需随机视觉时使用固定 seed。

## 代码结构

```tsx
const FPS = 30;
const HOLD_START = 60;

const clamp = {
  extrapolateLeft: "clamp" as const,
  extrapolateRight: "clamp" as const,
};

const enter = (frame: number, start: number, end: number) =>
  interpolate(frame, [start, end], [0, 1], {
    ...clamp,
    easing: Easing.bezier(0.16, 1, 0.3, 1),
  });
```

建立：

- `theme.ts`：颜色、字体、半径、阴影
- `timing.ts`：阶段、持续时间、曲线
- `Scene.tsx`：构图与组件编排
- `Root.tsx`：Composition 注册和可参数化 props

简单场景不必为了形式拆出过多文件。

## Live Photo 特有约束

- 第 0 帧不能是空白、全透明或明显残缺状态。
- 最终稳定帧必须是视觉最完整的状态。
- 避免硬切到封面状态；动作应自然收束到封面。
- 除非用户明确要求无缝循环，否则不要让结尾跳回开头。
- 推荐时长为 2-3 秒；单张最长不超过 5 秒。需要超过 5 秒的叙事更适合普通视频。
