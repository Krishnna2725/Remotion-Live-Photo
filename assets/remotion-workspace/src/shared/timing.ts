import {Easing, interpolate, spring} from "remotion";

export const clamp = {
  extrapolateLeft: "clamp" as const,
  extrapolateRight: "clamp" as const,
};

export const easeOut = (frame: number, start: number, end: number) =>
  interpolate(frame, [start, end], [0, 1], {
    ...clamp,
    easing: Easing.bezier(0.16, 1, 0.3, 1),
  });

export const editorial = (frame: number, start: number, end: number) =>
  interpolate(frame, [start, end], [0, 1], {
    ...clamp,
    easing: Easing.bezier(0.45, 0, 0.55, 1),
  });

export const emphasized = (frame: number, start: number, end: number) =>
  interpolate(frame, [start, end], [0, 1], {
    ...clamp,
    easing: Easing.bezier(0.34, 1.3, 0.64, 1),
  });

export const springProgress = ({
  frame,
  fps,
  delay = 0,
  durationInFrames = 24,
}: {
  frame: number;
  fps: number;
  delay?: number;
  durationInFrames?: number;
}) =>
  spring({
    frame,
    fps,
    delay,
    durationInFrames,
    config: {
      damping: 200,
      mass: 0.8,
      stiffness: 180,
    },
  });

export const mapProgress = (
  progress: number,
  outputRange: readonly [number, number],
) => interpolate(progress, [0, 1], outputRange, clamp);
