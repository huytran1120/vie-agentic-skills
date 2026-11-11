"""Validate the static guides and their routes into the real VAS catalog.

These checks inspect the delivered HTML. They do not claim browser rendering,
English prerendering or search-engine indexing has been verified.
"""

from html.parser import HTMLParser
import json
import re
import shlex
from pathlib import Path
import unittest
from urllib.parse import parse_qs, unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
PRIMARY = "https://vie-agentic-skills.vercel.app/"
SLUGS = (
    "agent-skills-la-gi",
    "kiem-thu-web-voi-playwright",
    "tao-video-voi-claude-code-remotion",
    "thiet-ke-anh-app-store",
    "quy-trinh-marketing-voi-ai",
    "toi-uu-seo-va-ai-search",
    "trang-so-sanh-va-landing-page-seo",
    "cai-agent-skills-cho-codex",
    "cai-skill-cho-claude-code",
    "agent-khong-nhan-skill",
    "agent-skills-mcp-agents-md",
    "review-pull-request-bang-ai",
    "debug-voi-ai-agent",
    "kiem-thu-dang-nhap-playwright",
    "trien-khai-n8n-docker-compose",
    "tu-readme-den-video-demo",
    "ghi-json-an-toan-nhieu-tien-trinh-python",
    "tao-video-khoa-hoc-manim-3b1b",
    "kien-truc-agentic-ai-agent-skills",
    "van-hanh-google-cloud-an-toan-gcloud-cli",
    "thiet-lap-may-headless-qua-ssh-khong-lo-mat-khau",
    "thu-vien-motion-prompt-192-hieu-ung-canvas-2d",
    "phuong-phap-socratic-cho-ai-agent-gia-su-hoc-tap",
    "ve-so-do-mang-homelab-bang-ai-agent-tu-yaml-den-svg",
    "de-ai-agent-xem-video",
)
LINKED_SKILLS = {
    "webapp-testing",
    "claude-awesome-video-creation",
    "store-screenshots",
    "content-strategy",
    "copywriting",
    "seo",
    "seo-geo",
    "seo-competitor-pages",
    "seo-aeo-landing-page-writer",
    "code-review",
    "systematic-debugging",
    "n8n-self-hosting",
    "research-explainer",
    "manim-composer",
    "manimce-best-practices",
    "pdf",
    "docx",
    "ui-ux-pro-max",
    "gcloud",
    "headless",
    "motion-prompt",
    "socratic-tutor",
    "stack-diagram",
    "animated-motion-diagram",
    "watch",
}
VOID_ELEMENTS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}


class GuideHTML(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.nodes = []
        self.metadata = {}
        self.ids = []
        self.stack = []
        self.text = {"vi": [], "en": []}
        self.title = []
        self.h1_count = 0
        self.h1_text = []
        self.unlinked_mentions = []
        self.structured = []
        self.json_parts = None
        self.examples = {}
        self.example_languages = {}
        self.example_id = None
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.nodes.append((tag, attrs))
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "meta":
            self.metadata[attrs.get("name", attrs.get("property"))] = attrs.get("content", "")
        if tag == "h1":
            self.h1_count += 1
        if tag == "script" and attrs.get("type") == "application/ld+json":
            self.json_parts = []
        if tag == "code" and attrs.get("id") in (
            "debug-before", "debug-after", "skill-architecture-example", "cost-accounting-example",
        ):
            self.example_id = attrs["id"]
            self.examples[self.example_id] = []
            self.example_languages[self.example_id] = attrs.get(
                "data-language", self.stack[-1][1] if self.stack else None,
            )
        if tag not in VOID_ELEMENTS:
            language = attrs.get("data-language", self.stack[-1][1] if self.stack else None)
            self.stack.append((tag, language))

    def handle_data(self, value):
        if self.example_id is not None:
            self.examples[self.example_id].append(value)
        tags = [tag for tag, _ in self.stack]
        if not {"a", "script", "style", "pre", "title"}.intersection(tags):
            self.unlinked_mentions.extend(skill for skill in LINKED_SKILLS
                                          if re.search(r"(?<![\w/-])" + re.escape(skill) + r"(?![\w/-])", value))
        if self.json_parts is not None:
            self.json_parts.append(value)
        if "title" in tags:
            self.title.append(value)
        if "h1" in tags:
            self.h1_text.append(value)
        if self.stack and "script" not in tags and "style" not in tags:
            language = self.stack[-1][1]
            if language in self.text:
                self.text[language].append(value)

    def handle_endtag(self, tag):
        if tag == "code":
            self.example_id = None
        if tag == "script" and self.json_parts is not None:
            self.structured.append(json.loads("".join(self.json_parts)))
            self.json_parts = None
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                del self.stack[index:]
                break


class BlogPagesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pages = [(DOCS / "blog/index.html", "blog/", False)]
        cls.pages.extend((DOCS / "blog" / slug / "index.html", f"blog/{slug}/", True) for slug in SLUGS)
        cls.catalog_ids = {skill["id"] for skill in json.loads((DOCS / "skills.min.json").read_text())}

    def test_index_links_to_each_article_once_as_a_heading(self):
        document = GuideHTML((DOCS / "blog/index.html").read_text())
        # Each article has a title link and a separate "Read guide" link.
        routes = [
            urlsplit(attrs["href"]).path.strip("./")
            for tag, attrs in document.nodes
            if tag == "a" and "data-guide-link" in attrs
        ]
        self.assertEqual(set(routes), set(SLUGS))
        for slug in SLUGS:
            self.assertEqual(routes.count(slug), 2, slug)

    def test_debugging_example_fails_before_and_passes_after_the_fix(self):
        document = GuideHTML((DOCS / "blog/debug-voi-ai-agent/index.html").read_text())
        before = "".join(document.examples["debug-before"])
        after = "".join(document.examples["debug-after"])
        with self.assertRaises(AssertionError):
            exec(compile(before, "blog-debug-before", "exec"), {})
        exec(compile(after, "blog-debug-after", "exec"), {})

    def test_intro_codex_examples_use_current_discovery_for_the_whole_install_lifecycle(self):
        document = GuideHTML((DOCS / "blog/agent-skills-la-gi/index.html").read_text())
        for language in ("vi", "en"):
            commands = [shlex.split(line.strip()) for line in "\n".join(document.text[language]).splitlines()
                        if line.strip().startswith(("./vas install ", "./vas status ", "./vas uninstall "))]
            with self.subTest(language=language):
                self.assertEqual([command[1] for command in commands], ["install", "status", "uninstall"])
                for command in commands:
                    self.assertEqual(command[command.index("--target") + 1], "workspace")
                    self.assertTrue(command[command.index("--dest") + 1].endswith("/.agents/skills"))

    def test_architecture_article_has_navigable_sections_without_draft_artifacts(self):
        source = (DOCS / "blog/kien-truc-agentic-ai-agent-skills/index.html").read_text()
        document = GuideHTML(source)
        headings = {attrs.get("id") for tag, attrs in document.nodes if tag == "h2"}
        fragments = {attrs.get("href") for tag, attrs in document.nodes if tag == "a"}
        for anchor in ("architecture", "boundaries", "disclosure", "cost", "controls", "practice"):
            with self.subTest(anchor=anchor):
                self.assertIn(anchor, headings)
                self.assertIn("#" + anchor, fragments)
        self.assertNotRegex(source, r"(?i)\[\s*cite\s*:|\[image\d+\]|data:image/")

    def test_architecture_examples_are_shared_text_and_skill_metadata_is_well_formed(self):
        document = GuideHTML((DOCS / "blog/kien-truc-agentic-ai-agent-skills/index.html").read_text())
        for example_id in ("skill-architecture-example", "cost-accounting-example"):
            with self.subTest(example=example_id):
                self.assertTrue("".join(document.examples[example_id]).strip())
                self.assertIsNone(document.example_languages[example_id], "Examples must remain available in both languages")
        skill = "".join(document.examples["skill-architecture-example"]).strip()
        frontmatter = re.fullmatch(r"---\n(.*?)\n---\n(.+)", skill, re.DOTALL)
        self.assertIsNotNone(frontmatter, "The illustrative SKILL.md needs frontmatter and a Markdown body")
        fields = dict(line.split(":", 1) for line in frontmatter[1].splitlines() if ":" in line)
        name = fields.get("name", "").strip().strip("\"'")
        description = fields.get("description", "").strip().strip("\"'")
        self.assertRegex(name, r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
        self.assertLessEqual(len(name), 64)
        self.assertTrue(description)
        self.assertLessEqual(len(description), 1024)

    def test_static_pages_have_unique_titles_and_canonical_metadata(self):
        titles = set()
        for page, route, article in self.pages:
            with self.subTest(page=route):
                document = GuideHTML(page.read_text())
                canonical = PRIMARY + route
                self.assertEqual(document.h1_count, 1)
                self.assertTrue("".join(document.h1_text).strip())
                title = "".join(document.title).strip()
                self.assertTrue(title)
                self.assertNotIn(title, titles)
                titles.add(title)
                self.assertEqual([attrs["href"] for tag, attrs in document.nodes if tag == "link" and attrs.get("rel") == "canonical"], [canonical])
                self.assertTrue(document.metadata["description"].strip())
                self.assertEqual(document.metadata["og:url"], canonical)
                self.assertEqual(document.metadata["og:type"], "article" if article else "website")
                for key in ("og:title", "og:description", "twitter:title", "twitter:description"):
                    self.assertTrue(document.metadata[key].strip(), key)
                self.assertEqual(document.metadata["twitter:card"], "summary_large_image")
                self.assertEqual(document.metadata["og:image"], document.metadata["twitter:image"])
                self.assertTrue(document.metadata["og:image"].startswith(PRIMARY))

    def test_articles_have_valid_blogposting_schema(self):
        count = 0
        for page, route, article in self.pages:
            document = GuideHTML(page.read_text())
            with self.subTest(page=route):
                self.assertEqual(len(document.structured), 1)
                schema = document.structured[0]
                self.assertEqual(schema["@context"], "https://schema.org")
                self.assertEqual(schema["url"], PRIMARY + route)
                self.assertEqual(schema["@type"], "BlogPosting" if article else "CollectionPage")
                if article:
                    count += 1
                    self.assertEqual(schema["mainEntityOfPage"], PRIMARY + route)
                    self.assertTrue(schema["headline"].strip())
                    self.assertTrue(schema["author"]["name"].strip())
                    self.assertTrue(schema["publisher"]["name"].strip())
        self.assertEqual(count, len(SLUGS))

    def test_every_blog_page_has_a_native_return_and_linked_skill_mentions(self):
        for page, route, _ in self.pages:
            document = GuideHTML(page.read_text())
            with self.subTest(page=route):
                returns = [attrs for tag, attrs in document.nodes if tag == "a" and "data-library-return" in attrs]
                self.assertEqual(len(returns), 1)
                link = urlsplit(returns[0]["href"])
                self.assertEqual((page.parent / link.path).resolve(), DOCS.resolve())
                self.assertEqual(link.fragment, "catalog")
                self.assertEqual(document.unlinked_mentions, [])
                self.assertTrue(any(tag == "span" and attrs.get("data-catalog-count") == "vi"
                                    for tag, attrs in document.nodes))

    def test_native_catalog_links_use_real_skill_ids(self):
        for page, route, article in self.pages:
            document = GuideHTML(page.read_text())
            links = [attrs for tag, attrs in document.nodes if tag == "a" and "data-catalog-skill" in attrs]
            with self.subTest(page=route):
                if article:
                    self.assertTrue(links, "Every article must offer a native link to its relevant skill")
                for attrs in links:
                    skill_id = attrs["data-catalog-skill"]
                    self.assertIn(skill_id, self.catalog_ids)
                    url = urlsplit(attrs["href"])
                    self.assertFalse(url.scheme)
                    self.assertEqual((page.parent / unquote(url.path)).resolve(), DOCS.resolve())
                    query = parse_qs(url.query)
                    self.assertEqual(query["skill"], [skill_id])
                    self.assertIn(query["lang"][0], ("vi", "en"))
                    self.assertTrue(query["agent"][0])

    def test_local_routes_assets_and_ids_resolve(self):
        for page, route, _ in self.pages:
            document = GuideHTML(page.read_text())
            with self.subTest(page=route):
                self.assertEqual(len(document.ids), len(set(document.ids)), "Duplicate IDs break fragment navigation")
                for tag, attrs in document.nodes:
                    for name in ("href", "src"):
                        if name not in attrs:
                            continue
                        raw = attrs[name]
                        url = urlsplit(raw)
                        if url.scheme or url.netloc:
                            self.assertIn(url.scheme, ("https", "http"), raw)
                            continue
                        target = (page.parent / unquote(url.path)).resolve() if url.path else page.resolve()
                        self.assertTrue(target.is_relative_to(DOCS.resolve()), f"Route escapes published docs: {raw}")
                        self.assertTrue(target.exists(), f"Missing {tag} {name}: {raw}")
                        if target.is_dir():
                            self.assertTrue((target / "index.html").is_file(), f"Missing index page: {raw}")
                        if url.fragment and target == page.resolve():
                            self.assertIn(unquote(url.fragment), document.ids, raw)

    def test_vietnamese_content_is_static_and_english_reading_is_available(self):
        for page, route, article in self.pages:
            document = GuideHTML(page.read_text())
            with self.subTest(page=route):
                root = next(attrs for tag, attrs in document.nodes if tag == "html")
                self.assertEqual(root["lang"], "vi")
                minimum = 150 if article else 50
                for language in ("vi", "en"):
                    self.assertGreater(len(" ".join(document.text[language]).split()), minimum, language)
                self.assertTrue(any(tag == "button" and attrs.get("id") == "blog-language" for tag, attrs in document.nodes))
                self.assertTrue(any(tag == "a" and attrs.get("href") == "#guide-main" for tag, attrs in document.nodes))


if __name__ == "__main__":
    unittest.main()
