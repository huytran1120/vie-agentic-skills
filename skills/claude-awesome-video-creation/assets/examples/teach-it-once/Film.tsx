import { CameraMotionBlur } from '@remotion/motion-blur';
import React from 'react';
import { AbsoluteFill, getStaticFiles, Html5Audio, Sequence, staticFile } from 'remotion';
import { C } from './brand/tokens';
import { Captions } from './Captions';
import { Mascot } from './Mascot';
import { FontGate } from './lib/FontGate';
import { S04, S05 } from './scenes/Explain';
import { S06, S07, S08, S09 } from './scenes/Demo';
import { S01, S02, S03 } from './scenes/Open';
import { S10, S11, S12 } from './scenes/Close';
import { SCENE, type SceneId } from './timeline';
import { Grain, KeyLight, Vignette } from './ui';

/** Written by scripts/soundtrack.py. Renders are muted and ffmpeg muxes it. */
export const SOUNDTRACK = 'audio/soundtrack.wav';

export const SCENES: [SceneId, React.FC, string][] = [
  ['s01', S01, 'S01 Cold open'],
  ['s02', S02, 'S02 Title'],
  ['s03', S03, 'S03 The problem'],
  ['s04', S04, 'S04 Anatomy'],
  ['s05', S05, 'S05 Disclosure'],
  ['s06', S06, 'S06 Install'],
  ['s07', S07, 'S07 The prompt'],
  ['s08', S08, 'S08 Render'],
  ['s09', S09, 'S09 Reveal'],
  ['s10', S10, 'S10 Write your own'],
  ['s11', S11, 'S11 Share it'],
  ['s12', S12, 'S12 End card'],
];

/** captions: burn in captions. mb: motion-blur samples per frame (0 = sharp, for previews). */
export type FilmProps = { captions?: boolean; mb?: number };

export const Film: React.FC<FilmProps> = ({ captions = true, mb = 8 }) => {
  const hasScore = getStaticFiles().some((s) => s.name === SOUNDTRACK);
  return (
    <FontGate>
      <AbsoluteFill style={{ background: C.ink }}>
        {SCENES.map(([id, Comp, name]) => (
          <Sequence key={id} from={SCENE[id].from} durationInFrames={SCENE[id].dur} name={name}>
            {mb > 1 ? (
              <CameraMotionBlur shutterAngle={180} samples={mb}>
                <Comp />
              </CameraMotionBlur>
            ) : (
              <Comp />
            )}
            <KeyLight />
          </Sequence>
        ))}
        <Vignette />
        <Mascot />
        {captions && <Captions />}
        <Grain />
        {hasScore && <Html5Audio src={staticFile(SOUNDTRACK)} />}
      </AbsoluteFill>
    </FontGate>
  );
};
