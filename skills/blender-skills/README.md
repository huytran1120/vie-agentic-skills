# Blender Skills in VAS

94 skills imported from [arjun988/blender-skills](https://github.com/arjun988/blender-skills)
at commit `8f778d2405a214b508d4c7d80742be8e43acdd52`, under the upstream MIT license.
Only `.claude/skills` is imported; the equivalent Cursor copy is not duplicated.

```bash
./vas list --category blender
./vas show blender-skills/blender-director
./vas install blender-skills/blender-director blender-skills/blender-modeler --target claude --global
```

Use the full `blender-skills/<name>` identifier to avoid ambiguous skill names.
Each skill retains its own reference files and includes nine shared references
and an MIT notice. Both `--mode copy` and `--mode link` are supported; links require
keeping the VAS source directory in place.

For independent installation, `../references/` paths in runbooks are changed to
`shared-references/`. Three cross-skill links point to the exact upstream revision.
All other imported skill/reference content is unchanged. Original and installed
SHA-256 hashes are recorded in [`data/blender-import.json`](../../data/blender-import.json).

Blender and a compatible Blender MCP connection are separate prerequisites.
Installing this pack does not install Blender, run code, configure a server, or
grant access to your computer. Read the
[upstream setup guide](https://github.com/arjun988/blender-skills#readme) before use;
multi-discipline workflows may require installing additional skills.
