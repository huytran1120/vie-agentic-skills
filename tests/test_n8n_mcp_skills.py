import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_local_project import ROOT, VAS, cli
from test_pages_build import PAGES


class N8nMcpSkillsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.imported = json.loads(
            (ROOT / "data/n8n-mcp-import.json").read_text(encoding="utf-8")
        )
        cls.index = json.loads((ROOT / "skills_index.json").read_text(encoding="utf-8"))
        cls.catalog = json.loads((ROOT / "data/catalog.json").read_text(encoding="utf-8"))
        cls.credits = json.loads((ROOT / "data/source-credits.json").read_text(encoding="utf-8"))
        cls.skills_by_id = {s["id"]: s for s in cls.index}

    def test_exact_identity_metadata_and_skipped_duplicates(self):
        self.assertEqual(self.imported["skill_count"], 1)
        self.assertEqual(len(self.imported["skipped"]), 14)
        self.assertEqual(self.imported["revision"], "1c755c5c8d99eb71faade17753a7f24138f4212c")
        self.assertEqual(self.imported["duplicate_check"]["catalog_count_before"], 3872)
        self.assertFalse(self.imported["duplicate_check"]["upstream_is_fork"])
        self.assertEqual(self.imported["duplicate_check"]["skipped_existing_count"], 14)

        expected_skipped = {
            "n8n-agents",
            "n8n-binary-and-data",
            "n8n-code-javascript",
            "n8n-code-python",
            "n8n-code-tool",
            "n8n-error-handling",
            "n8n-expression-syntax",
            "n8n-mcp-tools-expert",
            "n8n-multi-instance",
            "n8n-node-configuration",
            "n8n-subworkflows",
            "n8n-validation-expert",
            "n8n-workflow-patterns",
            "using-n8n-mcp-skills",
        }
        skipped_ids = {item["id"] for item in self.imported["skipped"]}
        self.assertEqual(skipped_ids, expected_skipped)
        for item in self.imported["skipped"]:
            self.assertEqual(item["reason"], "already_exists_in_catalog")
            self.assertIn(item["id"], self.skills_by_id)
            # Ensure skipped skills were not overwritten with czlonkowski/n8n-mcp source_repo
            self.assertNotEqual(
                self.skills_by_id[item["id"]].get("source_repo"),
                "czlonkowski/n8n-mcp",
            )

        # Check source-credits.json
        self.assertIn("n8nmcp", self.credits["sections"])
        self.assertIn("czlonkowski/n8n-mcp", self.credits["sections"]["n8nmcp"][0])
        self.assertIn("1c755c5c8d99eb71faade17753a7f24138f4212c", self.credits["sections"]["n8nmcp"][0])
        self.assertIn("MIT", self.credits["sections"]["n8nmcp"][0])

        # Verify total count and category taxonomy
        categories = {s.get("category", "general") for s in self.index}
        self.assertEqual(len(categories), 119)
        self.assertEqual(len(self.index), 4073)

        self.assertIn("n8n-self-hosting", self.skills_by_id)
        skill = self.skills_by_id["n8n-self-hosting"]
        self.assertEqual(skill["canonical_id"], "n8n-self-hosting")
        self.assertEqual(skill["category"], "automation")
        self.assertEqual(skill["risk"], "safe")
        self.assertEqual(skill["author"], "Romuald Czlonkowski")
        self.assertEqual(skill["license"], "MIT")
        self.assertEqual(skill["source_repo"], "czlonkowski/n8n-mcp")
        self.assertEqual(skill["source_revision"], "1c755c5c8d99eb71faade17753a7f24138f4212c")
        self.assertEqual(skill["source_path"], "data/skills/n8n-self-hosting/SKILL.md")
        self.assertIn("n8n", skill["tags"])
        self.assertIn("self-hosting", skill["tags"])

        cat_by_id = {s["id"]: s for s in self.catalog["skills"]}
        self.assertIn("n8n-self-hosting", cat_by_id)
        cat_entry = cat_by_id["n8n-self-hosting"]
        self.assertEqual(cat_entry["canonical_id"], "n8n-self-hosting")
        self.assertEqual(cat_entry["category"], "automation")
        self.assertEqual(cat_entry["license"], "MIT")
        self.assertEqual(cat_entry["author"], "Romuald Czlonkowski")

    def test_standalone_file_inventory_and_modes(self):
        records = self.imported["files"]
        self.assertEqual(len(records), 15)

        for r in records:
            file_path = ROOT / r["path"]
            self.assertTrue(file_path.is_file(), f"Missing file: {file_path}")
            st_mode = file_path.stat().st_mode
            if r["executable"]:
                self.assertNotEqual(st_mode & 0o111, 0, f"Script should be executable: {file_path}")
            else:
                self.assertEqual(st_mode & 0o111, 0, f"File should not be executable: {file_path}")

            h = hashlib.sha256()
            with open(file_path, "rb") as f:
                while chunk := f.read(65536):
                    h.update(chunk)
            self.assertEqual(h.hexdigest(), r["sha256"], f"Checksum mismatch for {file_path}")

        s_dir = ROOT / "skills" / "n8n-self-hosting"
        for expected_rel in [
            "SKILL.md",
            "LICENSE",
            "NOTICE.md",
            "README.md",
            "SINGLE_MODE.md",
            "QUEUE_MODE.md",
            "SECURITY.md",
            "CREDENTIAL_OVERWRITES.md",
            "DAY2.md",
            "assets/.env.queue.example",
            "assets/.env.single.example",
            "assets/Caddyfile",
            "assets/docker-compose.queue.yml",
            "assets/docker-compose.single.yml",
            "assets/init-data.sh",
        ]:
            self.assertTrue((s_dir / expected_rel).is_file(), f"Missing {expected_rel}")

        skill_text = (s_dir / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("## VAS installation notes", skill_text)
        self.assertIn("Canonical ID: `n8n-self-hosting`", skill_text)
        self.assertIn("czlonkowski/n8n-mcp", skill_text)

    def test_independent_cli_installation_and_clean_removal(self):
        for mode, target in [("link", "cursor"), ("copy", "claude")]:
            with self.subTest(mode=mode, target=target), tempfile.TemporaryDirectory(prefix=f"vas-n8n-{mode}-") as temp:
                project = Path(temp)
                result = cli(
                    "install", "n8n-self-hosting",
                    "--target", target,
                    "--mode", mode,
                    cwd=project,
                )
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                dest_dir = project / VAS.AGENT_TARGET_MAP[target][0]
                installed = dest_dir / "n8n-self-hosting"
                self.assertTrue(installed.exists())
                self.assertEqual(installed.is_symlink(), mode == "link")
                self.assertTrue((installed / "SKILL.md").is_file())
                self.assertTrue((installed / "LICENSE").is_file())
                self.assertTrue((installed / "NOTICE.md").is_file())
                self.assertTrue((installed / "QUEUE_MODE.md").is_file())
                self.assertTrue((installed / "assets/docker-compose.queue.yml").is_file())
                self.assertTrue((installed / "assets/init-data.sh").is_file())

                receipt_path = dest_dir / ".vas-manifest.json"
                self.assertTrue(receipt_path.exists())
                ledger = json.loads(receipt_path.read_text(encoding="utf-8"))
                self.assertIn("n8n-self-hosting", ledger)
                self.assertEqual(ledger["n8n-self-hosting"]["mode"], mode)

                status_res = cli("status", "--target", target, cwd=project)
                self.assertEqual(status_res.returncode, 0)
                self.assertIn("Total installed: 1", status_res.stdout)

                uninst_res = cli("uninstall", "n8n-self-hosting", "--target", target, cwd=project)
                self.assertEqual(uninst_res.returncode, 0)
                self.assertFalse(installed.exists())

    def test_pages_installation_manifest_integrity(self):
        manifests = PAGES.installation_manifests(ROOT)
        self.assertIn("n8n-self-hosting", manifests)
        m = manifests["n8n-self-hosting"]
        self.assertEqual(m["skill_id"], "n8n-self-hosting")
        self.assertEqual(m["target_name"], "n8n-self-hosting")
        self.assertEqual(m["provenance"]["author"], "Romuald Czlonkowski")
        self.assertEqual(m["provenance"]["source_repo"], "czlonkowski/n8n-mcp")
        self.assertEqual(m["provenance"]["license"], "MIT")

        file_paths = {f["path"]: f for f in m["files"]}
        self.assertEqual(len(file_paths), 15)
        self.assertIn("SKILL.md", file_paths)
        self.assertIn("LICENSE", file_paths)
        self.assertIn("NOTICE.md", file_paths)
        self.assertIn("QUEUE_MODE.md", file_paths)
        self.assertIn("assets/docker-compose.queue.yml", file_paths)
        self.assertIn("assets/.env.queue.example", file_paths)
        self.assertTrue(file_paths["assets/init-data.sh"]["executable"])
        self.assertFalse(file_paths["SKILL.md"]["executable"])


if __name__ == "__main__":
    unittest.main()
