# Kit: how the drops are made

- `capture/final.py`: real ZoroPrint Studio states from zoroprint.com/app/studio (Playwright, 2x, mirror off), plus element boxes.
- `video/specs.py`: the 7 videos (shots, camera rects in capture pixels, voice lines, captions, sources).
- `video/tts.py`: voice with Kokoro (`kokoro-onnx`, voice `af_heart`, model files from the kokoro-onnx v1.0 release).
- `video/build.py`: writes one HyperFrames project per video; `render_all.sh` renders (`npx hyperframes@0.8.185 render`) and normalises to -14 LUFS.
- `carousel/render.py` + `style.css`: 1080 × 1350 slides from `carousels.json` (one set works for TikTok photo mode and Instagram).

Media are served from this public repo (`raw.githubusercontent.com/.../main/<folder>/...`), which Metricool copies to its own storage at scheduling.
