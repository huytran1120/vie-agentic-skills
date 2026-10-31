# Engine helper commands

Run helpers with the locked engine environment. Paths and user text may contain Unicode; quote shell arguments. Helpers report validation failures before final publication. Read `--help` for exact positional arguments and options.

```sh
uv run --directory '<ENGINE>' python helpers/<helper>.py --help
```

- `align_words.py`
- `assemble_cut.py`
- `audit_cut.py`
- `audit_data.py`
- `breaths.py`
- `camera_motion.py`
- `captions.py`
- `common.py`
- `compose_final.py`
- `contact_sheet.py`
- `effects.py`
- `export_subtitles.py`
- `face_layout.py`
- `fetch_images.py`
- `filmstrip.py`
- `gen_image.py`
- `gen_music.py`
- `gen_sfx.py`
- `generate_effects.py`
- `grade.py`
- `icloud.py`
- `make_sfx.py`
- `matte.py`
- `measure_reference.py`
- `mix_music.py`
- `music_library.py`
- `noise_check.py`
- `pack_transcripts.py`
- `precise_edges.py`
- `preview_server.py`
- `quality_gate.py`
- `render_cut.py`
- `render_visuals.py`
- `screen_text.py`
- `sound_plan.py`
- `speech_regions.py`
- `style_samples.py`
- `suggest_visuals.py`
- `sync_cameras.py`
- `text_render.py`
- `tighten_cut.py`
- `timeline_view.py`
- `track_faces.py`
- `transcribe.py`
- `transcribe_batch.py`
- `verify_cut.py`
- `voice_check.py`
- `voice_levels.py`
- `watch_preview.py`
- `waveform_cut.py`

These modules have no command line; the helpers above and the CLI import them: `denoise.py`, `elevenlabs_api.py`, `fidelity.py`, `intake.py`, `media_policy.py`, `person_cutout.py`, `project_contract.py`, `render_vfr.py`, `spoken_numbers.py`, `transcript_corrections.py`, `workspace.py`.

The generated project has a separate build CLI, documented in [project-template/README.md](../project-template/README.md).
