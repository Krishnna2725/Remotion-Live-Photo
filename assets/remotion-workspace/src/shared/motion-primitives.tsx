import React from "react";
import {
  Img,
  interpolate,
  random,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import {clamp, easeOut, mapProgress, springProgress} from "./timing";

export const MaskReveal: React.FC<{
  children: React.ReactNode;
  start?: number;
  end?: number;
  distance?: number;
  direction?: "up" | "down" | "left" | "right";
  style?: React.CSSProperties;
}> = ({
  children,
  start = 6,
  end = 30,
  distance = 48,
  direction = "up",
  style,
}) => {
  const frame = useCurrentFrame();
  const progress = easeOut(frame, start, end);
  const vectors = {
    up: [0, distance],
    down: [0, -distance],
    left: [distance, 0],
    right: [-distance, 0],
  } as const;
  const [x, y] = vectors[direction];

  return (
    <div style={{overflow: "hidden", ...style}}>
      <div
        style={{
          opacity: progress,
          transform: `translate3d(${x * (1 - progress)}px, ${y * (1 - progress)}px, 0)`,
        }}
      >
        {children}
      </div>
    </div>
  );
};

export const StaggerWords: React.FC<{
  text: string;
  start?: number;
  stagger?: number;
  duration?: number;
  distance?: number;
  style?: React.CSSProperties;
}> = ({
  text,
  start = 8,
  stagger = 3,
  duration = 22,
  distance = 30,
  style,
}) => {
  const frame = useCurrentFrame();

  return (
    <span style={style}>
      {text.split(" ").map((word, index) => {
        const progress = easeOut(
          frame,
          start + index * stagger,
          start + index * stagger + duration,
        );
        return (
          <React.Fragment key={`${word}-${index}`}>
            <span
              style={{
                display: "inline-block",
                opacity: progress,
                transform: `translateY(${distance * (1 - progress)}px)`,
              }}
            >
              {word}
            </span>
            {index < text.split(" ").length - 1 ? " " : null}
          </React.Fragment>
        );
      })}
    </span>
  );
};

export const ParallaxImage: React.FC<{
  src: string;
  start?: number;
  end?: number;
  scaleFrom?: number;
  scaleTo?: number;
  shiftX?: number;
  shiftY?: number;
  style?: React.CSSProperties;
  imageStyle?: React.CSSProperties;
}> = ({
  src,
  start = 0,
  end = 54,
  scaleFrom = 1.08,
  scaleTo = 1,
  shiftX = 0,
  shiftY = 24,
  style,
  imageStyle,
}) => {
  const frame = useCurrentFrame();
  const progress = easeOut(frame, start, end);
  const scale = interpolate(progress, [0, 1], [scaleFrom, scaleTo], clamp);

  return (
    <div style={{overflow: "hidden", ...style}}>
      <Img
        src={src}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
          transform: `translate3d(${shiftX * (1 - progress)}px, ${shiftY * (1 - progress)}px, 0) scale(${scale})`,
          ...imageStyle,
        }}
      />
    </div>
  );
};

export const LightSweep: React.FC<{
  start?: number;
  end?: number;
  color?: string;
  angle?: number;
  width?: number;
  opacity?: number;
  style?: React.CSSProperties;
}> = ({
  start = 16,
  end = 42,
  color = "rgba(255,255,255,0.65)",
  angle = -18,
  width = 28,
  opacity = 0.7,
  style,
}) => {
  const frame = useCurrentFrame();
  const progress = easeOut(frame, start, end);
  const x = mapProgress(progress, [-140, 140]);

  return (
    <div
      style={{
        position: "absolute",
        inset: "-20%",
        pointerEvents: "none",
        mixBlendMode: "screen",
        opacity: opacity * Math.sin(progress * Math.PI),
        transform: `translateX(${x}%) rotate(${angle}deg)`,
        background: `linear-gradient(90deg, transparent ${50 - width / 2}%, ${color} 50%, transparent ${50 + width / 2}%)`,
        ...style,
      }}
    />
  );
};

export const FilmGrain: React.FC<{
  seed?: string;
  opacity?: number;
  density?: number;
  style?: React.CSSProperties;
}> = ({seed = "live-photo", opacity = 0.08, density = 2, style}) => {
  const frame = useCurrentFrame();
  const x = Math.round(random(`${seed}-x-${frame}`) * 100);
  const y = Math.round(random(`${seed}-y-${frame}`) * 100);

  return (
    <div
      style={{
        position: "absolute",
        inset: 0,
        pointerEvents: "none",
        opacity,
        mixBlendMode: "soft-light",
        backgroundImage:
          "repeating-radial-gradient(circle at 0 0, #fff 0 0.6px, #000 0.8px 1.2px, transparent 1.4px 3px)",
        backgroundPosition: `${x}px ${y}px`,
        backgroundSize: `${density}px ${density}px`,
        ...style,
      }}
    />
  );
};

export const HighlightWipe: React.FC<{
  children: React.ReactNode;
  start?: number;
  durationInFrames?: number;
  color?: string;
  radius?: number;
  style?: React.CSSProperties;
}> = ({
  children,
  start = 18,
  durationInFrames = 20,
  color = "#d7ff3f",
  radius = 8,
  style,
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const progress = springProgress({
    frame,
    fps,
    delay: start,
    durationInFrames,
  });

  return (
    <span style={{position: "relative", display: "inline-block", ...style}}>
      <span
        style={{
          position: "absolute",
          inset: "48% -0.08em -0.02em",
          background: color,
          borderRadius: radius,
          transform: `scaleX(${progress})`,
          transformOrigin: "left center",
        }}
      />
      <span style={{position: "relative"}}>{children}</span>
    </span>
  );
};
