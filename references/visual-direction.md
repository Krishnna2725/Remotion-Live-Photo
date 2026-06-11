# Live Photo Visual Design Standard

Use this document to turn a style choice into a complete, deliberate visual system. Do not treat a style name as permission to add random effects. Every decision must support one visual thesis.

## Contents

- Design Brief
- Universal Design Principles
- Ratio and Safe-Area System
- Composition Archetypes
- Typography Standard
- Color and Material Standard
- Style Direction Menu
- Anti-Patterns
- Pre-Implementation Design Check

## 1. Design Brief

Before writing JSX, define the following internally:

```text
Subject:
Audience:
Desired feeling:
Primary message:
Selected style:
Composition archetype:
Hero element:
Supporting elements:
Motion thesis:
```

Write the motion thesis as one sentence:

> Use [spatial behavior] and [material behavior] to make [hero element] communicate [desired feeling].

Examples:

- Use slow depth separation and restrained light drift to make the product feel precise and intelligent.
- Use editorial cropping and measured type reveals to make the announcement feel culturally significant.
- Use chromatic compression and sharp scale changes to make the campaign feel loud and immediate.

## 2. Universal Design Principles

### 2.1 Design the Poster First

The resolved frame must work as a static poster without relying on motion.

- Establish one unmistakable hero.
- Use no more than two supporting focal points.
- Keep titles to one or two lines unless the design is intentionally typographic.
- Make the primary message readable at 25% preview scale.
- Reserve negative space intentionally; do not fill every region.

### 2.2 Use Contrast Deliberately

Create hierarchy with at least three of these:

- scale contrast
- weight contrast
- value contrast
- color contrast
- density contrast
- sharpness contrast
- spatial depth

Do not make every object medium-sized, medium-weight, and equally visible.

### 2.3 Limit the Visual Vocabulary

For each Live Photo, select:

- one dominant background behavior
- one material language
- one primary type voice
- one accent behavior
- one hero motion

Avoid mixing glass, chrome, grain, glow, paper, and particles in the same piece.

### 2.4 Build a Designed Collection

When generating multiple Live Photos, preserve a collection system:

- Keep the same type family and core palette.
- Keep margins and title placement related.
- Vary the hero composition and motion signature.
- Rotate between two or three composition archetypes.
- Give every item one distinctive detail without breaking the family.
- Define a separate composition archetype and motion thesis for every item before coding.
- Share tokens and small primitives, but do not share the complete hero layout.

Reject a collection as template swapping when the items share the same:

- hero object shape and position
- title block position and scale
- supporting-card arrangement
- entrance direction and timing
- resolved-frame silhouette

Changing only copy, accent color, index number, or a central symbol does not create meaningful variation.

## 3. Ratio and Safe-Area System

Use an internal spacing unit equal to roughly 1% of the shorter canvas edge.

| Ratio | Recommended Canvas | Outer Safe Area | Preferred Composition |
|---|---:|---:|---|
| 3:4 | 1080 × 1440 | 72-96 px | stacked editorial, asymmetric poster |
| 4:3 | 1440 × 1080 | 72-96 px | split composition, horizontal cascade |
| 1:1 | 1080 × 1080 | 64-80 px | singular monument, centered tension |
| 16:9 | 1920 × 1080 | 96-128 px | cinematic split, wide typography |
| 9:16 | 1080 × 1920 | 80-112 px | vertical monument, top-bottom narrative |

Rules:

- Keep critical text inside the safe area.
- Decorative shapes and photography may bleed beyond the canvas.
- Avoid placing the hero exactly in the geometric center unless using Singular Monument.
- Use an optical center slightly above the mathematical center for portrait ratios.
- Leave enough stable negative space for the motion to breathe.

## 4. Composition Archetypes

### Asymmetric Poster

Place the title and hero on opposing visual axes. Let one element cross the center line to connect the composition.

Best for: campaigns, portraits, announcements, editorial work.

Avoid: equal left/right weights or small scattered objects.

### Singular Monument

Let one object occupy 55-80% of the visual attention. Supporting text behaves like a label, not a competing block.

Best for: products, logos, symbols, single statements.

Avoid: adding cards around the hero to fill space.

### Editorial Split

Create an unequal split, such as 38/62 or 44/56. Use typography and image as contrasting voices.

Best for: stories, culture, fashion, events.

Avoid: a generic 50/50 layout with matching visual weight.

### Z-Axis Cascade

Use two or three depth planes with controlled overlap. Each plane must have a clear role: atmosphere, subject, information.

Best for: product systems, digital experiences, layered photography.

Avoid: more than three major planes or arbitrary card piles.

### Typographic Field

Use expressive type as the primary image. Pair oversized letterforms with one restrained detail layer.

Best for: quotes, launches, titles, music and culture.

Avoid: long paragraphs or multiple decorative fonts.

## 5. Typography Standard

Typography must feel art-directed, not merely formatted.

### Hierarchy

- Display title: dominant, usually 8-18% of canvas height.
- Secondary line: 25-45% of display title size.
- Metadata or eyebrow: 10-16% of display title size.
- Limit the system to three visible type sizes when possible.

### Pairing

- Use one display face and one neutral supporting face at most.
- Pair by contrast: serif + grotesk, condensed + wide, heavy + light.
- For Chinese, prioritize strong weight contrast, disciplined tracking, and clean line breaks over decorative font mixing.
- Never fake luxury with excessive letter spacing on all text.

### Line Breaking

- Break titles by meaning, rhythm, and shape.
- Avoid a single orphan character or word.
- Use line lengths that form an intentional silhouette.
- Let oversized type crop only when the remaining form is still recognizable.

### Recommended Character

- Premium grotesk: Geist, Plus Jakarta Sans, General Sans, Satoshi.
- Editorial serif: PP Editorial New, Cormorant Garamond, Noto Serif SC.
- Condensed display: Bebas Neue, Oswald, or a high-quality local equivalent.
- Avoid generic default-looking combinations and overused dashboard typography.

## 6. Color and Material Standard

### Color Roles

Define colors by role:

```text
Canvas:
Primary ink:
Secondary ink:
Accent:
Atmospheric color:
```

- Use one accent color at a time.
- Keep the strongest saturation near the hero.
- Ensure important text remains readable without relying on glow.
- Use gradients as lighting or depth, not as decorative wallpaper.

### Shadows

- Prefer large, soft, low-opacity ambient shadows.
- Use contact shadows only where objects need physical grounding.
- Avoid generic dark drop shadows and identical shadows on every object.

### Borders

- Use hairlines only when they describe material edges.
- Tint borders toward the surrounding light or material.
- Avoid generic gray 1px borders around every container.

### Texture

- Grain should be subtle enough to disappear at first glance.
- Paper texture should affect the whole visual world, not one arbitrary card.
- Chrome requires controlled highlights and dark reflections.
- Glass requires visible depth separation behind it; transparent rectangles alone are not glass.

## 7. Style Direction Menu

## 01 Ethereal Glass

**Intent:** Intelligent, spatial, quiet, futuristic.

**Palette**

- Canvas: `#050505`, `#090A0F`, or deep blue-black.
- Ink: cool white with restrained secondary gray.
- Accent: choose one family from violet, electric blue, or emerald.
- Atmosphere: low-opacity radial illumination behind the hero.

**Typography**

- Wide or neutral grotesk.
- Large title with disciplined tracking.
- Small technical metadata may use uppercase microtype.

**Composition**

- Prefer Singular Monument or Z-Axis Cascade.
- Use one glass plane around the hero, not a dashboard of glass cards.
- Keep 35-50% of the frame visually quiet.

**Material**

- Dark glass, subtle specular edge, faint volumetric light.
- Use nested shells only for the primary object.

**Motion Signature**

- Slow depth separation, restrained parallax, light drift, precise title resolve.
- No playful bounce.

**Avoid**

- Neon rainbow gradients, excessive blur, generic SaaS card grids, glowing every edge.

## 02 Editorial Luxury

**Intent:** Cultured, deliberate, timeless, tactile.

**Palette**

- Canvas: warm ivory, parchment, espresso, muted burgundy, or deep ink.
- Accent: one restrained jewel tone or metallic warm gray.

**Typography**

- High-contrast serif display paired with a quiet grotesk.
- Use dramatic size differences and intentional line breaks.

**Composition**

- Prefer Editorial Split, Asymmetric Poster, or Typographic Field.
- Allow photography and letterforms to crop beyond the edge.
- Use generous margins and one unexpected alignment.

**Material**

- Fine paper grain, ink-like color, subtle print registration details.
- Avoid obvious digital glass effects.

**Motion Signature**

- Slow image reveal, measured type masks, tiny camera drift, calm settling.

**Avoid**

- Bouncy springs, bright app gradients, rounded UI cards, excessive labels.

## 03 Soft Structuralism

**Intent:** Precise, calm, trustworthy, modern.

**Palette**

- Canvas: white, pearl, silver gray, or cool stone.
- Ink: charcoal rather than pure black.
- Accent: muted blue, sage, coral, or one brand color.

**Typography**

- Bold grotesk display with light supporting text.
- Use clean alignment and generous line height.

**Composition**

- Prefer Singular Monument or an airy Asymmetric Poster.
- Use large simple forms and controlled negative space.

**Material**

- Soft diffused shadows, satin surfaces, subtle inset highlights.
- Rounded forms must feel intentional and geometrically related.

**Motion Signature**

- Precise slide-and-settle, soft scale resolve, subtle object separation.

**Avoid**

- Heavy outlines, hard shadows, busy texture, dramatic rotation.

## 04 Neo-Brutalist Poster

**Intent:** Direct, rebellious, graphic, immediate.

**Palette**

- Use high-contrast pairs: black/acid yellow, cobalt/red, cream/black.
- Limit to two dominant colors plus one neutral.

**Typography**

- Oversized condensed or heavy grotesk.
- Type may become the image through crop, repetition, or stacking.

**Composition**

- Prefer Typographic Field or Asymmetric Poster.
- Use strong blocks, abrupt scale contrast, and purposeful collisions.

**Material**

- Flat color, print marks, halftone, rough but controlled texture.

**Motion Signature**

- Sharp scale compression, decisive directional wipes, fast type locks.
- Motion may be forceful but must land cleanly.

**Avoid**

- Random chaos, illegible type, five-color palettes, fake hand-drawn clutter.

## 05 Cinematic Minimalism

**Intent:** Atmospheric, emotional, premium, restrained.

**Palette**

- Dark neutrals, desaturated photography, one warm or cool light source.
- Preserve deep blacks without crushing the subject.

**Typography**

- Minimal title treatment, often small or medium scale.
- Use refined serif or cinematic grotesk with sparse metadata.

**Composition**

- Prefer Singular Monument or Editorial Split.
- Let photography dominate; text must behave like a film title.

**Material**

- Cinematic grain, subtle vignette, controlled highlight bloom.

**Motion Signature**

- Slow Ken Burns move, atmospheric light drift, gentle depth reveal.

**Avoid**

- Fast UI motion, floating cards, decorative gradients, aggressive bounce.

## 06 Y2K Chrome

**Intent:** Energetic, digital, glossy, provocative.

**Palette**

- Black, silver, white, and one vivid digital accent.
- Use iridescence selectively near reflective surfaces.

**Typography**

- Futuristic display face or stretched grotesk.
- Supporting text stays minimal and technical.

**Composition**

- Prefer Singular Monument or Z-Axis Cascade.
- Build around one chrome hero object or wordmark.

**Material**

- Liquid metal, sharp reflections, lens sparkle, controlled chromatic fringe.

**Motion Signature**

- Reflective sweep, elastic but tight scale settle, crisp rotational reveal.

**Avoid**

- Covering every object in chrome, unreadable distortion, rainbow overload.

## 07 Organic Tactile

**Intent:** Human, warm, grounded, crafted.

**Palette**

- Clay, linen, moss, sand, charcoal, faded botanical tones.
- Use natural contrast rather than maximum saturation.

**Typography**

- Humanist serif or softly shaped grotesk.
- Pair with handwritten details only when genuinely appropriate.

**Composition**

- Prefer Asymmetric Poster or Editorial Split.
- Use imperfect but controlled placement and generous breathing room.

**Material**

- Paper fibers, cloth, pressed shapes, natural shadows, subtle imperfections.

**Motion Signature**

- Gentle layered drift, paper reveal, soft focus transition, calm settling.

**Avoid**

- Artificial neon, sterile glass cards, excessive digital precision.

## 08 Brand Gradient

**Intent:** Recognizable, bright, communicative, social-ready.

**Palette**

- Use the supplied brand gradient or define a disciplined two- or three-stop gradient.
- Pair with a neutral canvas or neutral ink so the gradient remains special.

**Typography**

- Strong, highly readable grotesk.
- Keep the message immediate and suitable for small-screen viewing.

**Composition**

- Prefer Asymmetric Poster or Singular Monument.
- Use gradient as a hero light, shape, or field rather than on every surface.

**Material**

- Smooth color field, restrained glow, crisp brand geometry.

**Motion Signature**

- Gradient drift, shape expansion, clear title reveal, confident settle.

**Avoid**

- Rainbow gradients, low-contrast text, generic social template layouts.

## 09 AI Chooses

Choose according to content:

| Content Type | Preferred Direction |
|---|---|
| AI, software, digital service | Ethereal Glass or Soft Structuralism |
| Fashion, culture, event, premium brand | Editorial Luxury or Cinematic Minimalism |
| Product launch or professional service | Soft Structuralism or Brand Gradient |
| Music, youth campaign, bold announcement | Neo-Brutalist Poster or Y2K Chrome |
| Craft, food, wellness, nature | Organic Tactile or Editorial Luxury |

Do not choose solely by industry. Match the emotional goal and available imagery.

## 8. Anti-Patterns

Reject the design and revise when any of these appear:

- A generic three-card layout or dashboard composition.
- Every object has a border, shadow, glow, or rounded rectangle.
- Multiple unrelated materials compete in one frame.
- All elements enter at the same time and speed.
- The hero is unclear at thumbnail size.
- Text is reduced to decoration and becomes unreadable.
- Motion exists without changing emphasis, depth, or meaning.
- The resolved frame looks like a web section rather than a designed poster.

## 9. Pre-Implementation Design Check

Before implementing motion, confirm:

- The visual thesis can be stated in one sentence.
- The chosen style is expressed through palette, type, composition, material, and motion.
- One composition archetype clearly governs the frame.
- The hero receives the strongest contrast and most meaningful motion.
- The final frame can stand alone as a polished poster.
