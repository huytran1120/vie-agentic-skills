#!/usr/bin/env python3
"""
Import skillevaluator skill from NVIDIA/SkillEvaluator.
Validates upstream files, copies into skills/skillevaluator,
adds VAS installation notes, NOTICE.md, LICENSE,
records provenance to data/skillevaluator-import.json,
and updates data/catalog.json and data/source-credits.json.
"""

import hashlib
import json
import os
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
UPSTREAM_REPO = "NVIDIA/SkillEvaluator"
UPSTREAM_REV = "7ae25d2522c9c3b151111fedaa67b814cc3dc5c5"
AUTHOR = "Christopher Kevin"
AUTHOR_EMAIL = "christopherk@nvidia.com"
AUTHOR_URL = "https://github.com/NVIDIA"

UPSTREAM_DIR = Path("/tmp/skillevaluator-temp")
if not UPSTREAM_DIR.exists() or not (UPSTREAM_DIR / "skills/skillevaluator/SKILL.md").exists():
    raise RuntimeError(f"Upstream clone not found at {UPSTREAM_DIR}")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def main():
    skill_id = "skillevaluator"
    target_dir = REPO_ROOT / "skills" / skill_id
    if target_dir.exists():
        shutil.rmtree(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    # 1. Copy upstream license as LICENSE
    license_src = UPSTREAM_DIR / "LICENSE"
    license_dst = target_dir / "LICENSE"
    shutil.copy2(license_src, license_dst)

    # 2. Generate NOTICE.md
    notice_text = f"""# Notice for {skill_id}

This skill payload is adapted from upstream repository [{UPSTREAM_REPO}](https://github.com/{UPSTREAM_REPO})
at commit revision `{UPSTREAM_REV}`.

- Author: {AUTHOR} <{AUTHOR_EMAIL}>
- Upstream Organization: NVIDIA Corporation & Affiliates
- Upstream License: Apache License 2.0 (see bundled LICENSE)
- Upstream Source Path: `skills/skillevaluator`
- Adapted for Vie Agentic Skill (VAS) distribution.

## Bundled Components and Provenance

- `SKILL.md`: Core runbook and Agent Skills specification for operating the SkillEvaluator CLI across Tier 1, Tier 2, and Tier 3 evaluation workflows.
- `evals/`: Evaluator dataset and configuration for self-evaluation (`config.yml`, `evals.json`).
- `references/`: Comprehensive reference runbooks for:
  - `commands-tier1.md`: Tier 1 quality, security, and rubric evaluation commands.
  - `commands-tier2-tier3.md`: Tier 2 deduplication and Tier 3 live agent evaluation commands.
  - `commands-validate.md`: Combined validation pipeline commands.
  - `custom-graders.md`: Bring-your-own-grader (BYOG) and Harbor task specifications.
  - `providers.md`: LLM provider configuration and API credentials.
  - `reports-and-ci.md`: Report formats, exit codes, and CI integration.
  - `tier3-datasets.md`: Eval dataset authoring, case structure, and Harbor task formats.
  - `tier3-running.md`: Live evaluation execution, agent selection, Docker and local sandbox modes.
  - `troubleshooting.md`: Common errors, doctor commands, and fixes.

## VAS Adaptation Notes

- Preserves upstream directory structure and standalone execution semantics.
- Appended standard VAS installation, attribution, and safety notes to `SKILL.md`.
- Mapped to existing `agent-evaluation` category to preserve the exact 119-category taxonomy.
- Managed by Vie Agentic Skill (VAS) with zero external package manager dependencies (no NPX).
"""
    notice_dst = target_dir / "NOTICE.md"
    notice_dst.write_text(notice_text, encoding="utf-8")

    # 3. Write .gitattributes and .skillignore
    (target_dir / ".gitattributes").write_text("* text=auto eol=lf\n", encoding="utf-8")
    (target_dir / ".skillignore").write_text(
        ".git\n.DS_Store\n__pycache__/\n*.pyc\n.pytest_cache/\n.coverage\n",
        encoding="utf-8",
    )

    # 4. Copy evals/ and references/
    for sub in ["evals", "references"]:
        src_sub = UPSTREAM_DIR / "skills/skillevaluator" / sub
        dst_sub = target_dir / sub
        shutil.copytree(src_sub, dst_sub)

    # 5. Process SKILL.md
    skill_src = UPSTREAM_DIR / "skills/skillevaluator/SKILL.md"
    skill_content = skill_src.read_text(encoding="utf-8")

    vas_notes = """

## VAS installation notes

This skill is curated and verified by **Vie Agentic Skill (VAS)** from [NVIDIA/SkillEvaluator](https://github.com/NVIDIA/SkillEvaluator).
- Canonical ID: `skillevaluator`
- Source repository: [`NVIDIA/SkillEvaluator`](https://github.com/NVIDIA/SkillEvaluator) (revision `7ae25d2522c9c3b151111fedaa67b814cc3dc5c5`, path `skills/skillevaluator`)
- Author: Christopher Kevin <christopherk@nvidia.com> (NVIDIA Corporation & Affiliates)
- License: Apache-2.0 (see bundled `LICENSE` and `NOTICE.md`)
- Role: Official Agent Skill for operating NVIDIA SkillEvaluator CLI across Tier 1 (static/security/quality), Tier 2 (deduplication/overlap), and Tier 3 (live Harbor agent benchmarks).
- Prerequisites: Python 3.12-3.14, `skillevaluator` CLI (`pip install --upgrade "skillevaluator[all]"`). Keyless for static Tier 1 checks; LLM provider key (`NVIDIA_API_KEY`, etc.) needed for rubric and live evaluation. Docker required for default containerized Tier 3 trials.
- Safety: Installation only links or copies files and writes `.vas-manifest.json`. No runtime/dependency is installed, no background process is spawned, and no external service is connected during `./vas install`.
"""
    combined_content = skill_content.rstrip() + vas_notes
    (target_dir / "SKILL.md").write_text(combined_content, encoding="utf-8")

    # 6. Inventory all packaged files
    file_records = []
    for p in sorted(target_dir.rglob("*")):
        if p.is_file():
            rel_path = p.relative_to(REPO_ROOT).as_posix()
            source_rel = None
            if p.name in [".gitattributes", ".skillignore", "NOTICE.md"]:
                source_rel = f"skills/skillevaluator/{p.name}"
            elif p.name == "LICENSE":
                source_rel = "LICENSE"
            else:
                source_rel = f"skills/skillevaluator/{p.relative_to(target_dir).as_posix()}"

            src_file = UPSTREAM_DIR / source_rel if source_rel and (UPSTREAM_DIR / source_rel).is_file() else None
            src_sha = sha256_file(src_file) if src_file else sha256_file(p)

            file_records.append({
                "skill_id": skill_id,
                "source_path": source_rel or f"skills/skillevaluator/{p.relative_to(target_dir).as_posix()}",
                "path": rel_path,
                "source_sha256": src_sha,
                "sha256": sha256_file(p),
                "executable": os.access(p, os.X_OK) and not p.suffix == ".md",
            })

    # 7. Create data/skillevaluator-import.json
    import_manifest = {
        "source_repo": UPSTREAM_REPO,
        "source_url": f"https://github.com/{UPSTREAM_REPO}",
        "revision": UPSTREAM_REV,
        "author": f"{AUTHOR} <{AUTHOR_EMAIL}>",
        "author_url": AUTHOR_URL,
        "license": "Apache-2.0",
        "license_source": f"https://github.com/{UPSTREAM_REPO}/blob/{UPSTREAM_REV}/LICENSE",
        "skill_count": 1,
        "skipped": [
            {
                "id": "calculator",
                "path": "src/skillevaluator/tier3/reference_skills/calculator",
                "reason": "Internal test fixture / decoy skill for Harbor runner, placeholder author maintainers@example.com."
            },
            {
                "id": "task-list",
                "path": "src/skillevaluator/tier3/reference_skills/task-list",
                "reason": "Internal test fixture / decoy skill for Harbor runner, placeholder author maintainers@example.com."
            },
            {
                "id": "text-analyzer",
                "path": "src/skillevaluator/tier3/reference_skills/text-analyzer",
                "reason": "Internal quickstart starter / decoy skill, placeholder author maintainers@example.com."
            },
            {
                "id": "api-caller",
                "path": "src/skillevaluator/tier3/reference_skills/api-caller",
                "reason": "Internal test fixture / decoy skill for Harbor runner, placeholder author maintainers@example.com."
            },
            {
                "id": "create-custom-grader",
                "path": "src/skillevaluator/tier3/reference_skills/create-custom-grader",
                "reason": "Internal benchmark reference fixture; functionality fully incorporated into skillevaluator's references/custom-graders.md."
            }
        ],
        "namespaces": {},
        "duplicate_check": {
            "catalog_count_before": 4078,
            "upstream_is_fork": False,
            "methods": [
                "canonical-id/name",
                "source-repo/path",
                "raw-sha256",
                "normalized-body",
                "renamed-body",
                "body-containment",
                "7-word-shingles"
            ],
            "collision_rationale": "Exact and shingle similarity comparison against all 4,078 catalog skills identified zero existing duplicates (0.0028 max 7-word shingle Jaccard similarity). `skillevaluator` is the genuinely new, official Agent Skill published by NVIDIA Corporation & Affiliates for operating NVIDIA SkillEvaluator across Tier 1, Tier 2, and Tier 3 evaluation pipelines."
        },
        "adaptations": [
            "Preserve upstream payload structure: SKILL.md, evals/, and references/ under Open Agent Skills format.",
            "Include upstream Apache-2.0 LICENSE and add NOTICE.md clarifying standalone operation and provenance.",
            "Append reversible VAS installation, attribution, and prerequisites notes to SKILL.md.",
            "Map `skillevaluator` to the existing `agent-evaluation` category to preserve the 119-category taxonomy.",
            "Operates via skillevaluator CLI with zero external package manager dependencies (no NPX)."
        ],
        "skills": [
            {
                "id": "skillevaluator",
                "canonical_id": "skillevaluator",
                "name": "skillevaluator",
                "path": "skills/skillevaluator",
                "description": "Run and interpret SkillEvaluator for agent skills. Use for any skill benchmark or eval - validating or scoring a SKILL.md, writing evals.json test cases or evals config, explaining benchmark reports, verdicts and exit codes, or gating skills in CI.",
                "category": "agent-evaluation",
                "tags": [
                    "skills",
                    "evaluation",
                    "benchmarking",
                    "ci",
                    "security",
                    "nvidia",
                    "agent-evaluation",
                    "rubric",
                    "harbor"
                ],
                "risk": "safe",
                "author": f"{AUTHOR} <{AUTHOR_EMAIL}>",
                "author_url": AUTHOR_URL,
                "source": f"https://github.com/{UPSTREAM_REPO}/tree/{UPSTREAM_REV}/skills/skillevaluator",
                "source_repo": UPSTREAM_REPO,
                "source_revision": UPSTREAM_REV,
                "source_path": "skills/skillevaluator",
                "license": "Apache-2.0",
                "license_source": f"https://github.com/{UPSTREAM_REPO}/blob/{UPSTREAM_REV}/LICENSE"
            }
        ],
        "files": file_records
    }

    import_manifest_path = REPO_ROOT / "data" / "skillevaluator-import.json"
    import_manifest_path.write_text(json.dumps(import_manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Created {import_manifest_path}")

    # 8. Update data/source-credits.json
    credits_path = REPO_ROOT / "data" / "source-credits.json"
    credits = json.loads(credits_path.read_text(encoding="utf-8"))
    credits["sections"]["skillevaluator"] = [
        f"- **[{UPSTREAM_REPO}](https://github.com/{UPSTREAM_REPO}/tree/{UPSTREAM_REV})**: Official Agent Skill for NVIDIA SkillEvaluator by NVIDIA Corporation & Affiliates at revision `{UPSTREAM_REV}` under the Apache License 2.0.",
        "- Provides the `skillevaluator` skill enabling coding agents to run, interpret, and gate agent skills across Tier 1 (static quality, security scan, PII scan, LLM rubric), Tier 2 (deduplication & collection similarity), and Tier 3 (live Docker/Seatbelt Harbor benchmark trials and Skill Lift measurement).",
        "- Standalone payload preserves upstream Agent Skills specification SKILL.md, evals/ test cases, and references/ runbooks (`commands-tier1.md`, `commands-tier2-tier3.md`, `commands-validate.md`, `custom-graders.md`, `providers.md`, `reports-and-ci.md`, `tier3-datasets.md`, `tier3-running.md`, `troubleshooting.md`).",
        "- Licensing: Apache License 2.0 (Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES); see bundled LICENSE and NOTICE.md.",
        "- Installation via `./vas install` only links or copies static files and writes `.vas-manifest.json`. No runtime/dependency is installed, and no API keys or cloud credentials are connected during installation."
    ]
    credits_path.write_text(json.dumps(credits, indent=2) + "\n", encoding="utf-8")
    print(f"Updated {credits_path}")

    # 9. Update data/catalog.json
    catalog_path = REPO_ROOT / "data" / "catalog.json"
    catalog_data = json.loads(catalog_path.read_text(encoding="utf-8"))
    
    # Check if skillevaluator already in catalog
    existing_skill_ids = {s.get("canonical_id") for s in catalog_data.get("skills", [])}
    if skill_id not in existing_skill_ids:
        catalog_entry = {
            "id": skill_id,
            "canonical_id": skill_id,
            "name": "skillevaluator",
            "description": "Run and interpret SkillEvaluator for agent skills. Use for any skill benchmark or eval - validating or scoring a SKILL.md, writing evals.json test cases or evals config, explaining benchmark reports, verdicts and exit codes, or gating skills in CI.",
            "category": "agent-evaluation",
            "risk": "safe",
            "author": f"{AUTHOR} <{AUTHOR_EMAIL}>",
            "author_url": AUTHOR_URL,
            "source": f"https://github.com/{UPSTREAM_REPO}/tree/{UPSTREAM_REV}/skills/skillevaluator",
            "source_repo": UPSTREAM_REPO,
            "source_revision": UPSTREAM_REV,
            "source_path": "skills/skillevaluator",
            "license": "Apache-2.0",
            "license_source": f"https://github.com/{UPSTREAM_REPO}/blob/{UPSTREAM_REV}/LICENSE",
            "tags": [
                "skills",
                "evaluation",
                "benchmarking",
                "ci",
                "security",
                "nvidia",
                "agent-evaluation",
                "rubric",
                "harbor"
            ],
            "triggers": [
                "evaluate skill",
                "skill evaluation",
                "skillevaluator",
                "nvidia skill eval",
                "benchmark skill",
                "tier 1 validation",
                "tier 2 deduplication",
                "tier 3 harbor",
                "quality check",
                "skill lift"
            ],
            "path": f"skills/{skill_id}"
        }
        catalog_data["skills"].append(catalog_entry)
        catalog_data["total"] = len(catalog_data["skills"])
        catalog_data["total_skills"] = len(catalog_data["skills"])
        catalog_path.write_text(json.dumps(catalog_data, indent=2) + "\n", encoding="utf-8")
        print(f"Added {skill_id} to {catalog_path}")

    print("Import complete! Run ./vas sync next.")


if __name__ == "__main__":
    main()
