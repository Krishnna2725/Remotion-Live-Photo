import React from "react";
import {Composition, Folder} from "remotion";
import {projects} from "./projects/registry";

export const RemotionRoot: React.FC = () => (
  <>
    {projects.map((project) => (
      <Folder key={project.slug} name={project.folder}>
        {project.compositions.map((composition) => (
          <Composition
            key={composition.id}
            id={composition.id}
            component={composition.component}
            durationInFrames={composition.durationInFrames}
            fps={composition.fps}
            width={composition.width}
            height={composition.height}
          />
        ))}
      </Folder>
    ))}
  </>
);
