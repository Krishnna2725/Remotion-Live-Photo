import type {ComponentType} from "react";

export type LivePhotoComposition = {
  id: string;
  component: ComponentType;
  durationInFrames: number;
  fps: number;
  width: number;
  height: number;
};

export type LivePhotoProject = {
  slug: string;
  folder: string;
  compositions: LivePhotoComposition[];
};
