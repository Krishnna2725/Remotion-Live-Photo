# Live Photo Motion Recipes

Use this document when implementing motion. It deliberately excludes long-video features such as subtitles, voiceover, audio visualization, maps, multi-scene storytelling, and complex transitions.

The goal is not to add more effects. The goal is to select one strong motion mechanism that makes the resolved poster more expressive.

## 1. Core Implementation Rules

### Separate timing from mapping

Calculate one normalized progress value, then derive visual properties from it:

```tsx
const enter = easeOut(frame, 6, 34);
const y = interpolate(enter, [0, 1], [48, 0]);
const scale = interpolate(enter, [0, 1], [0.96, 1]);
```

Do not create separate interpolations with slightly different timing for every property unless the difference is intentional.

### Use local timelines

Use `<Sequence>` when a component owns a distinct phase. Inside a Sequence, `useCurrentFrame()` starts at zero.

```tsx
<Sequence from={12} durationInFrames={36} premountFor={15} layout="none">
  <TitleReveal />
</Sequence>
```

Always set `premountFor` for Sequences containing images, fonts, or expensive components.

### Prefer transforms and opacity

Animate:

- `transform`
- `opacity`
- `clipPath`
- gradient position
- mask scale

Avoid animating large blur radii, layout dimensions, and large shadow spreads on every frame.

### Keep randomness deterministic

Use Remotion `random()` with a stable seed. Never use `Math.random()`.

```tsx
const x = random(`particle-x-${index}`) * width;
```

For moving texture, include the frame in the seed. For fixed layouts, do not include the frame.

## 2. Timing Vocabulary

Choose timing based on the visual thesis:

| Intent | Curve | Typical duration |
|---|---|---:|
| Precise arrival | `easeOut()` | 18-30 frames |
| Editorial drift | `editorial()` | 30-60 frames |
| One emphasized impact | `emphasized()` or restrained `springProgress()` | 16-26 frames |
| Poster hold | no motion | final 10-15 frames |

Use springs for one focal event only. Do not apply springs to every card, label, and decoration.

## 3. Typography Recipes

### Line mask reveal

Use for editorial headlines and strong Chinese display type.

```tsx
<MaskReveal start={8} end={34} distance={64}>
  <h1>Design the final frame first.</h1>
</MaskReveal>
```

Rules:

- Reveal complete lines or deliberate text blocks.
- Keep the mask container tight to the text.
- Offset headline lines by 2-5 frames when staggered.
- Do not combine with a large scale animation.

### Word stagger

Use for short English headlines or compact statements:

```tsx
<StaggerWords text="Make every frame matter" start={8} stagger={3} />
```

Rules:

- Keep stagger between 2-4 frames.
- Use no more than 8-10 words.
- For Chinese copy, split deliberate phrases manually rather than individual characters.

### Highlight wipe

Use to emphasize one important phrase:

```tsx
<HighlightWipe start={24} color="#d7ff3f">
  Motion
</HighlightWipe>
```

Rules:

- One highlighted phrase per composition.
- Animate the background wipe, not per-character opacity.
- Keep the text fully readable before and after the wipe.

### Kinetic impact word

Use for one large character or word such as “动”:

```tsx
const impact = emphasized(frame, 8, 28);
const scaleX = interpolate(impact, [0, 1], [1.35, 1]);
const scaleY = interpolate(impact, [0, 1], [0.55, 1]);
const tracking = interpolate(impact, [0, 1], [-18, 0]);
```

Add one secondary mechanism only: directional smear, sliced duplicate, or short chromatic offset. Settle completely before the poster hold.

### Typewriter

Use only when typing is part of the concept. Reveal text using string slicing:

```tsx
const visible = text.slice(0, Math.floor(frame / 2));
```

Never render every character and animate its opacity independently.

## 4. Image Recipes

### Restrained Ken Burns

Use `ParallaxImage` for photographic material:

```tsx
<ParallaxImage
  src={staticFile("projects/example/hero.jpg")}
  start={0}
  end={58}
  scaleFrom={1.08}
  scaleTo={1}
  shiftY={28}
/>
```

Rules:

- Scale range should usually stay within `1.00-1.12`.
- Move toward the subject, not toward an arbitrary edge.
- Stop before the final poster hold.

### Layered parallax

Separate foreground, subject, and background. Give each layer a different movement amplitude but the same timing:

```tsx
const drift = editorial(frame, 0, 54);
const backY = interpolate(drift, [0, 1], [18, 0]);
const subjectY = interpolate(drift, [0, 1], [34, 0]);
const frontY = interpolate(drift, [0, 1], [52, 0]);
```

Use at most three depth layers. Large differences feel like a slideshow.

### Cropped image reveal

Wrap the image in an `overflow: hidden` container and animate the image and container in opposite directions. This creates a reveal without changing layout dimensions.

```tsx
const reveal = easeOut(frame, 8, 34);
const clip = interpolate(reveal, [0, 1], [100, 0]);
const imageX = interpolate(reveal, [0, 1], [-42, 0]);

<div style={{clipPath: `inset(0 ${clip}% 0 0)`}}>
  <Img style={{transform: `translateX(${imageX}px)`}} />
</div>
```

### Editorial collage cascade

For multiple user images:

- Give each image a distinct crop and final size.
- Stagger arrivals by 3-6 frames.
- Vary direction and distance slightly.
- Keep one image dominant.
- Avoid making every image the same rounded card.

Before implementation, inspect image dimensions. Use `getImageDimensions()` when the crop depends on the source ratio.

## 5. Light, Material, and Texture Recipes

### Light sweep

Use `LightSweep` over chrome, glass, or a single emphasized surface:

```tsx
<LightSweep start={18} end={44} angle={-22} opacity={0.55} />
```

Use it once. A sweep across the whole composition should not repeat or remain visible during the poster hold.

### Breathing glow

Animate a low-opacity radial gradient with a small translation. Avoid animating a large CSS blur:

```tsx
const glow = editorial(frame, 0, 52);
const x = interpolate(glow, [0, 1], [-20, 16]);
const opacity = interpolate(glow, [0, 0.5, 1], [0.18, 0.28, 0.2]);
```

### Film grain

Use `FilmGrain` at low opacity to reduce sterile gradients and add material texture:

```tsx
<FilmGrain seed="scene-01" opacity={0.06} density={3} />
```

Do not use it as a substitute for composition or hierarchy.

### Chromatic offset

Duplicate one hero word or silhouette into red and cyan layers. Animate offsets from `8-16px` to zero over 8-16 frames. Use `mixBlendMode: "screen"` or restrained opacity. Keep the settled frame clean.

### Scan line

Move one thin gradient line across a surface. Pair it with a subtle local brightness change, not full-screen glitch noise.

## 6. Structural Motion Recipes

### Cascade

Use when several elements establish hierarchy:

```tsx
const item = easeOut(frame, baseStart + index * 4, baseStart + index * 4 + 22);
```

Keep the final silhouette asymmetrical. A cascade should not become a uniform list animation.

### Assembly

Use when pieces combine into one final hero. Animate all pieces toward a shared resolved object, then remove unnecessary seams and decoration before the poster hold.

### Ratio morph

Use for communicating layout flexibility. Animate a frame's width and height using transforms, while the content inside repositions through the same progress. Do not animate DOM layout dimensions if a transform can create the same visual result.

### Directional wipe

Use `clipPath: inset(...)` or a moving mask to reveal a new color field or image. Limit to one direction that supports the composition.

## 7. Font and Text Safety

- Load local fonts with `@remotion/fonts`.
- Load remote Google Fonts with `@remotion/google-fonts` only when network access is appropriate.
- Load only required weights and subsets.
- Validate that fonts are loaded before measuring text.
- Use `measureText()`, `fitText()`, or `fillTextBox()` from `@remotion/layout-utils` when copy length is variable.
- Match measurement properties exactly to rendering properties.
- Do not depend on a system font being installed on the render machine.

## 8. Effect Selection Matrix

| Visual direction | Recommended primary motion | Supporting effect |
|---|---|---|
| Ethereal Glass | depth separation or slow assembly | breathing glow |
| Editorial Luxury | line mask reveal or collage cascade | restrained image drift |
| Soft Structuralism | ratio morph or precise assembly | soft light sweep |
| Neo-Brutalist Poster | kinetic impact word | directional wipe |
| Cinematic Minimalism | Ken Burns or layered parallax | film grain |
| Y2K Chrome | compressed impact word | chromatic offset or light sweep |
| Organic Tactile | collage cascade | paper-like grain |
| Brand Gradient | directional reveal or assembly | controlled glow |

## 9. Performance Boundaries

- Prefer 2D transforms over animated filters.
- Avoid several full-screen blend-mode layers.
- Keep full-screen grain opacity below `0.12`.
- Avoid large animated blur values; use gradients or pre-rendered assets instead.
- Add external Remotion packages only when the visual result justifies the dependency.
- Do not use `HtmlInCanvas`, WebGL, 3D, Lottie, or light-leak packages by default.

## 10. Final Motion Audit

Before rendering, answer:

1. What is the single hero motion?
2. Does every supporting motion reinforce it?
3. Is frame 0 already watchable?
4. Does the motion settle naturally into the strongest poster?
5. Is the final hold completely stable?
6. Would removing any effect improve clarity?
