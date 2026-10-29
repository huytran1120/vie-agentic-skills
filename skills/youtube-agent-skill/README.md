# YouTube agent skills for VAS

11 skill YouTube của [Jake Schincariol](https://github.com/Jakeschincariol/youtube-agent-skill),
giấy phép MIT, được nhập từ commit
`a2feb2104981a375ffd4f87ee04f4f5344ac43c6`. Bộ skill tạo bản nháp và phân tích
dữ liệu bạn cung cấp; không kết nối tài khoản hay tự đăng video.

## Install / Cài đặt

Run from the cloned VAS repository. Replace the destination with your actual
project folder; the CLI does not create a YouTube account connection.

```bash
./vas search youtube-agent-skill
./vas show youtube-agent-skill/yt-script
./vas install youtube-agent-skill/yt-script --target claude --mode link --dest /path/to/project/.claude/skills
./vas status --target claude --dest /path/to/project/.claude/skills
```

Use `--mode copy` for an independent copy. Choose another supported VAS agent and
its destination folder when appropriate. For agents without the upstream
`/yt-*` commands, ask the agent to read the installed `SKILL.md` directly.

## Workflows

| Skill | Workflow |
| --- | --- |
| [yt-script](yt-script/SKILL.md) | Video scripts, 21 hook formulas and heuristic hook scoring |
| [yt-package](yt-package/SKILL.md) | Titles and thumbnail text as one pairing |
| [yt-edit](yt-edit/SKILL.md) | Edit decision lists from timestamped transcripts |
| [yt-comment](yt-comment/SKILL.md) | Triage comments and draft replies |
| [yt-plan](yt-plan/SKILL.md) | Content plans sized to the creator's available time |
| [yt-viral](yt-viral/SKILL.md) | Rank supplied public video data by each channel's median |
| [yt-retention](yt-retention/SKILL.md) | Analyze retention CSV exports, optionally with a transcript |
| [yt-shorts](yt-shorts/SKILL.md) | Identify self-contained Shorts in a long transcript |
| [yt-seo](yt-seo/SKILL.md) | Descriptions, tags and search-facing copy |
| [yt-chapters](yt-chapters/SKILL.md) | Draft chapters and check timestamp rules |
| [yt-audit](yt-audit/SKILL.md) | Review a channel and identify the first change to make |

## Setup and boundaries

The six helper tools require only Python 3's standard library. Run their commands
from the installed skill directory. Shared parsers, formulas and scoring tools
are bundled where needed, including when you install only one skill.

The optional [voice template](templates/voice.md) is also included in every
installable folder. The upstream profile location is
`~/.claude/youtube/voice.md`. Create or update that personal file only with the
user's permission; VAS installation does not write it.

Bring your own transcripts, retention exports or public video data. Transcription
and data-collection tools mentioned upstream are optional, separate dependencies.
Hook scores are heuristics, not predictions or promises of views. The original
human publication gates remain in every runbook.

## Provenance

The original [MIT license](LICENSE) is preserved in this collection and every
installable skill. `data/youtube-import.json` records upstream and vendored
SHA-256 hashes and the documented local path adaptations. No plugin marketplace
configuration or account credentials are installed.
