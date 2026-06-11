import {Scene} from "./Scene";
import type {LivePhotoProject} from "../types";

export const project: LivePhotoProject = {
  slug: "replace-project-slug",
  folder: "Replace-Project-Folder",
  compositions: [
    {
      id: "livephoto-replace-scene",
      component: Scene,
      durationInFrames: 90,
      fps: 30,
      width: 1080,
      height: 1440,
    },
  ],
};
