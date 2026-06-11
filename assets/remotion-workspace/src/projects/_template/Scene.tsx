import React from "react";
import {AbsoluteFill, useCurrentFrame} from "remotion";
import {easeOut} from "../../shared/timing";

export const Scene: React.FC = () => {
  const frame = useCurrentFrame();
  const enter = easeOut(frame, 4, 42);

  return (
    <AbsoluteFill
      style={{
        alignItems: "center",
        background: "#0a0a0a",
        color: "#fff",
        display: "flex",
        fontFamily: "sans-serif",
        justifyContent: "center",
      }}
    >
      <div style={{opacity: enter, transform: `translateY(${(1 - enter) * 50}px)`}}>
        Replace with a designed final frame.
      </div>
    </AbsoluteFill>
  );
};
