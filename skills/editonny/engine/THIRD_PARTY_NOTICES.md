# Third-party notices

First-party editonny code is MIT licensed. The following upstream licenses continue to govern their respective code, fonts, models, and recordings. This document preserves the original resource inventory; it does not claim a fresh legal or provider-terms audit.

## Adapted browser-use/video-use code

The following helpers contain code adapted from https://github.com/browser-use/video-use: transcribe.py, transcribe_batch.py, pack_transcripts.py, render_cut.py, grade.py, and timeline_view.py. Their original attribution comments remain in place.

Original license text:

```
MIT License

Copyright (c) 2026 Browser Use

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Bundled fonts

Fonts under assets/fonts retain complete license files beside each font. They are used for captions, hooks, calls to action, and disclaimers.

| Font | File | Author | License | License file |
| --- | --- | --- | --- | --- |
| Anton | `assets/fonts/anton/Anton-Regular.ttf` | Copyright 2020 The Anton Project Authors | SIL Open Font License 1.1 | `assets/fonts/anton/OFL.txt` |
| Montserrat | `assets/fonts/montserrat/Montserrat-Variable.ttf` | Copyright 2024 The Montserrat.Git Project Authors | SIL Open Font License 1.1 | `assets/fonts/montserrat/OFL.txt` |
| Figtree | `assets/fonts/figtree/Figtree-Variable.ttf` | Copyright 2022 The Figtree Project Authors | SIL Open Font License 1.1 | `assets/fonts/figtree/OFL.txt` |
| Caveat | `assets/fonts/caveat/Caveat-Variable.ttf` | Copyright 2014 The Caveat Project Authors | SIL Open Font License 1.1 | `assets/fonts/caveat/OFL.txt` |
| Permanent Marker | `assets/fonts/permanentmarker/PermanentMarker-Regular.ttf` | Copyright (c) 2010 Font Diner, Inc. | Apache License 2.0 | `assets/fonts/permanentmarker/LICENSE.txt` |

SIL Open Font License fonts can be embedded and distributed with software but cannot be sold by themselves. Permanent Marker is a Font Diner, Inc. trademark. The project template also includes Montserrat, Caveat, and JetBrains Mono under SIL OFL 1.1, with their full notices under project-template/assets/fonts. JetBrains Mono is copyright 2020 The JetBrains Mono Project Authors.

## Bundled models

| Model | File | Source | Author | License | License file |
| --- | --- | --- | --- | --- | --- |
| YuNet (face_detection_yunet_2023mar) | `assets/models/face_detection_yunet_2023mar.onnx` | OpenCV Zoo (https://github.com/opencv/opencv_zoo) | Copyright (c) 2020 Shiqi Yu | MIT License | `assets/models/YUNET_LICENSE.txt` |
| MediaPipe Selfie Multiclass Segmentation 256x256 (selfie_multiclass_256x256) | `assets/models/selfie_multiclass_256x256.onnx` | Google MediaPipe (https://ai.google.dev/edge/mediapipe/solutions/vision/image_segmenter) | Google (model-card author: Adel Ahmadyan) | Apache License 2.0 | `assets/models/SELFIE_MULTICLASS_LICENSE.txt` |

YuNet detects faces for safe layout. MediaPipe Selfie Multiclass Segmentation separates the speaker from the background locally. Its model card prohibits surveillance and identity-recognition uses; editonny uses segmentation only.

The original TFLite file was downloaded on 2026-09-16 from https://storage.googleapis.com/mediapipe-models/image_segmenter/selfie_multiclass_256x256/float32/latest/selfie_multiclass_256x256.tflite (SHA-256 c6748b1253a99067ef71f7e26ca71096cd449baefa8f101900ea23016507e0e0). The model-card license is at https://storage.googleapis.com/mediapipe-assets/Model%20Card%20Multiclass%20Segmentation.pdf.

Modification notice under Apache-2.0 section 4b: converted from TFLite to ONNX using tf2onnx 1.17.0, without changing weights. The included ONNX SHA-256 is 35549e14dc62c73b34f0fd04ec1765d9f1577230a2d068cb25c39f600350f477. Full conversion details and Apache license remain in assets/models/SELFIE_MULTICLASS_LICENSE.txt. Google publishes no separate NOTICE for this model.

## Bundled sound effects

Recorded kit sounds are CC0; generated layers and wholly synthetic sounds are first-party MIT. Each receipt under assets/sfx/licenses records source URLs, authors, the recorded license statement, processing, and calibration. The English rebuild preserves waveform bytes and numeric calibration. Credits are not required for CC0 recordings; optional acknowledgment is appreciated by several authors.

| Effect | File | Author | License receipt |
| --- | --- | --- | --- |
| whoosh | `assets/sfx/whoosh.wav` | USC Cinema / Sunset Editorial Collection, published by jscott@archive.org | `assets/sfx/licenses/whoosh.txt` |
| pop | `assets/sfx/pop.wav` | Kenney (Kenney Vleugels, kenney.nl) | `assets/sfx/licenses/pop.txt` |
| click | `assets/sfx/click.wav` | Kenney Vleugels (kenney.nl) | `assets/sfx/licenses/click.txt` |
| tick | `assets/sfx/synthetic/tick.wav` | SHK Soluções Digitais (this project's code) | `assets/sfx/licenses/tick.txt` |
| rise | `assets/sfx/rise.wav` | UnKnownrNone (Wikimedia Commons), own work | `assets/sfx/licenses/rise.txt` |
| cash | `assets/sfx/cash.wav` | Joseph SARDIN (BigSoundBank.com) | `assets/sfx/licenses/cash.txt` |
| coin | `assets/sfx/coin.wav` | DavidGreck, published by BigSoundBank.com | `assets/sfx/licenses/coin.txt` |
| notification | `assets/sfx/notification.wav` | Joseph SARDIN (BigSoundBank.com) | `assets/sfx/licenses/notification.txt` |
| success | `assets/sfx/success.wav` | Kenney Vleugels (kenney.nl) | `assets/sfx/licenses/success.txt` |
| error | `assets/sfx/synthetic/error.wav` | SHK Soluções Digitais (this project's code) | `assets/sfx/licenses/error.txt` |
| count | `assets/sfx/count.wav` | Circlerun (OpenGameArt) | `assets/sfx/licenses/count.txt` |
| keyboard | `assets/sfx/keyboard.wav` | Joseph SARDIN (BigSoundBank.com) | `assets/sfx/licenses/keyboard.txt` |
| snap | `assets/sfx/snap.wav` | Vinrax (OpenGameArt); room-tail processing: SHK Soluções Digitais | `assets/sfx/licenses/snap.txt` |
| mouse_click | `assets/sfx/mouse_click.wav` | Joseph SARDIN (BigSoundBank.com) | `assets/sfx/licenses/mouse_click.txt` |
| bass_drop | `assets/sfx/synthetic/bass_drop.wav` | SHK Soluções Digitais (this project's code) | `assets/sfx/licenses/bass_drop.txt` |
| metal_hit | `assets/sfx/metal_hit.wav` | Pablo BERGEL, published by BigSoundBank.com; bass layer: SHK Soluções Digitais | `assets/sfx/licenses/metal_hit.txt` |
| synth_hit | `assets/sfx/synthetic/synth_hit.wav` | SHK Soluções Digitais (this project's code) | `assets/sfx/licenses/synth_hit.txt` |
| flash | `assets/sfx/synthetic/flash.wav` | SHK Soluções Digitais (this project's code) | `assets/sfx/licenses/flash.txt` |
| charge | `assets/sfx/synthetic/charge.wav` | SHK Soluções Digitais (this project's code) | `assets/sfx/licenses/charge.txt` |
| metal_riser | `assets/sfx/metal_riser.wav` | Joseph SARDIN (BigSoundBank.com); bass layer: SHK Soluções Digitais | `assets/sfx/licenses/metal_riser.txt` |
| wind | `assets/sfx/synthetic/wind.wav` | SHK Soluções Digitais (this project's code) | `assets/sfx/licenses/wind.txt` |
| rewind | `assets/sfx/synthetic/rewind.wav` | SHK Soluções Digitais (this project's code) | `assets/sfx/licenses/rewind.txt` |
| gears | `assets/sfx/gears.wav` | Joseph SARDIN (BigSoundBank.com) and Kenney Vleugels (kenney.nl); bass layer: SHK Soluções Digitais | `assets/sfx/licenses/gears.txt` |
| data | `assets/sfx/synthetic/data.wav` | SHK Soluções Digitais (this project's code) | `assets/sfx/licenses/data.txt` |

Sources include BigSoundBank (Joseph SARDIN, DavidGreck, Pablo BERGEL), Kenney.nl, OpenGameArt (Circlerun and Vinrax), USC Cinema / Sunset Editorial Collection via Internet Archive, and UnKnownrNone via Wikimedia Commons. Recorded sounds remain CC0. Optional credit: "Sound effects: BigSoundBank, Kenney.nl, OpenGameArt, USC Cinema / Sunset Editorial Collection, and UnKnownrNone (CC0)."

Cash layers a drawer and bell; click doubles a single click; count repeats a beep; gears combines ratchet and impact recordings with synthetic bass. Snap, metal_hit, and metal_riser add generated layers to CC0 recordings. Notification is a transposed glass strike, not a proprietary phone notification. Exact preparation recipes and measurements are in the receipts and manifest.

The synthetic folder is generated by helpers/make_sfx.py with fixed seeds. Woven's 35 unchanged sounds are CC0 1.0 Universal; provenance and hashes are in assets/sfx/sfx_woven.json and its original sound-license statement is in assets/sfx/woven/LICENSE.md. Woven source: https://github.com/woven-video/woven-sfx. No Woven application code is bundled.

## Installed dependencies

Dependencies are installed through the locked uv environment rather than bundled into this source directory. Their own licenses and transitive notices continue to apply.

| Dependency | Purpose | License |
| --- | --- | --- |
| numpy | Audio and image calculations | BSD-3-Clause |
| Pillow | Text and image drawing | MIT-CMU / HPND |
| requests | Optional remote-service requests | Apache-2.0 |
| opencv-python-headless | Face detection, optical flow, filters, compositing | Apache-2.0; see its LICENSE-3RD-PARTY.txt |
| onnxruntime | Person segmentation and faster-whisper inference | MIT |
| mlx-whisper | Local transcription on Apple Silicon | MIT |
| faster-whisper | Local transcription on other supported systems | MIT |

Transitive dependencies, including mlx, ctranslate2, flatbuffers, protobuf, coloredlogs, sympy, tokenizers, and huggingface-hub, retain their individual licenses. OpenAI Whisper model weights are MIT licensed and downloaded from Hugging Face on first use.

## Separately installed programs and runtime resources

FFmpeg (https://ffmpeg.org) is LGPL or GPL depending on its build. uv (https://github.com/astral-sh/uv) is MIT or Apache-2.0. HyperFrames (https://github.com/heygen-com/hyperframes) is Apache-2.0 and is fetched at the pinned version through Node/npx. GSAP uses its upstream GreenSock license. The project template fetches required runtime resources during preparation. MediaPipe hand tracking uses its Apache-2.0 model, downloaded when requested. These licenses are not replaced by the first-party MIT license.

## Optional external services

None is required for local cutting, captions, or composition. External media transmission and paid generation require separate authorization.

- Wikimedia Commons receives search text. Each image has its own license; credits.json records author, source, and attribution requirements.
- Pexels receives search text and PEXELS_API_KEY when selected. Its terms are at https://www.pexels.com/license/.
- OpenRouter receives an image-generation prompt and OPENROUTER_API_KEY only when explicitly used. Provider and model terms apply: https://openrouter.ai/terms. Generation can incur charges.
- ElevenLabs receives sound or music prompts and the user's configured credentials when explicitly used. Account plan, commercial-use rules, and generated-media restrictions apply; keep the returned provenance and usage records.
- Hugging Face receives model-download requests for local inference. Repository model licenses and service terms apply.
