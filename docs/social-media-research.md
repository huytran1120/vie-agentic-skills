# Social Media Research Skills trong VAS / Social Media Research Skills in VAS

## Tiếng Việt

Đã thêm **13 skill mới / 39 tệp**, không có bản trùng phải bỏ qua.
Upstream: [`ScrapeCreators/social-media-research-skills`](https://github.com/ScrapeCreators/social-media-research-skills) tại revision `64ba7b4dea71e130d2712ffb6c1c1024b3b7c4b2`.
Catalog: **3.872 skill / 119 danh mục**.
Bộ sưu tập kỹ năng phân tích và nghiên cứu mạng xã hội (Social Media Intelligence & Research) dành cho **Google Antigravity**, **OpenAI Codex**, **Claude Code**, **Cursor**, **Windsurf**, **Cline** và **GitHub Copilot CLI** do **ScrapeCreators ([@ScrapeCreators](https://github.com/ScrapeCreators))** phát triển:
cung cấp quy trình phân tích chuyên sâu cho quảng cáo (Ad Library Meta/Google/LinkedIn), bóc tách hồ sơ nhà sáng tạo nội dung, khai phá phản hồi/bình luận (comment mining & voice-of-customer), nghiên cứu đối thủ cạnh tranh, tái sử dụng nội dung (content repurposing), tìm kiếm người có sức ảnh hưởng (influencer prospecting), phát hiện bài viết đột phá (outlier posts), nghiên cứu nhu cầu sản phẩm (Reddit & mạng xã hội), tóm tắt và trích xuất kịch bản video (transcripts intelligence), lắng nghe mạng xã hội (social listening brief) và khám phá xu hướng mới (trend discovery).

Kỹ năng `audience-research` từ upstream được namespace thành `scrapecreators-audience-research` để phân biệt với kỹ năng phân tích đối tượng quảng cáo sẵn có trong catalog.

Tất cả kỹ năng được phát hành theo giấy phép **MIT License**, bản quyền thuộc về **ScrapeCreators**.

### Danh sách 13 kỹ năng Social Media Research

1. `ad-library-teardown`: Bóc tách thông điệp, ưu đãi, hook, CTA và video ads từ thư viện quảng cáo Meta, Google và LinkedIn.
2. `scrapecreators-audience-research`: Đánh giá nhân khẩu học người theo dõi, phân bố địa lý và mức độ phù hợp tài trợ cho creator.
3. `comment-mining`: Đào sâu bình luận và phản hồi để trích xuất tiếng nói khách hàng (VoC), thắc mắc, rào cản mua hàng và ý tưởng sản phẩm.
4. `competitor-social-research`: Phân tích chiến lược mạng xã hội của đối thủ, tìm khoảng trống nội dung và lập chiến lược kênh.
5. `content-repurposing`: Chuyển đổi video dài và transcript thành bài đăng LinkedIn, chuỗi tweet X, kịch bản ngắn, bản tin và carousel.
6. `creator-profile-teardown`: Bóc tách định vị kênh, trụ cột nội dung, bài đăng đột phá và công thức viral của nhà sáng tạo nội dung.
7. `influencer-prospecting`: Tìm kiếm, xếp hạng và lập danh sách creator, influencer tiềm năng cho chiến dịch tiếp thị và UGC.
8. `outlier-post-finder`: Tìm các bài viết có tương tác vượt trội so với trung bình kênh và phân tích lý do thành công.
9. `product-demand-research`: Xác thực ý tưởng sản phẩm, phân tích điểm đau và đo lường nhu cầu từ Reddit và mạng xã hội.
10. `scrapecreators-api`: Tích hợp REST API của ScrapeCreators để trích xuất dữ liệu công khai từ hơn 27 nền tảng xã hội.
11. `social-listening-brief`: Tạo báo cáo tổng hợp dư luận mạng xã hội, phân tích cảm xúc và xu hướng thảo luận về thương hiệu.
12. `transcript-intelligence`: Trích xuất hook, trích dẫn, luận điểm và tóm tắt kịch bản từ video TikTok, YouTube, Reels, Rumble, Reddit.
13. `trend-discovery`: Khám phá chủ đề, hashtag, âm thanh và định dạng đang thịnh hành theo từng ngách ngành.

### Hướng dẫn sử dụng không cần clone repo (Copy Agent Prompt)

Mở trang [Social Media Research trên VAS](https://huytran1120.github.io/vie-agentic-skills/?lang=vi&sources=scrapecreators), chọn agent (Antigravity, Cursor, Claude Code, Codex...), bấm **Copy Agent Prompt** và dán vào cửa sổ chat của dự án.

Agent sẽ đọc manifest `install-manifests/<canonical-id>.json`, xác thực SHA-256 từng tệp, tải trọn gói và lưu vào thư mục dự án cùng receipt `.vas-manifest.json` tương thích với CLI.

### Hướng dẫn sử dụng qua CLI (`./vas`)

Từ thư mục checkout VAS:

```bash
# Tìm kiếm kỹ năng
./vas search scrapecreators
./vas search ad-library-teardown

# Xem chi tiết runbook
./vas show ad-library-teardown
./vas show scrapecreators-audience-research

# Cài đặt vào dự án (chế độ copy độc lập)
./vas install ad-library-teardown --target claude --mode copy --dest "/path/to/project/.claude/skills"

# Cài đặt liên kết (chế độ link symlink)
./vas install trend-discovery --target antigravity --mode link

# Kiểm tra trạng thái cài đặt
./vas status --target claude --dest "/path/to/project/.claude/skills"

# Gỡ bỏ kỹ năng khi hoàn thành dự án
./vas uninstall ad-library-teardown --target claude --dest "/path/to/project/.claude/skills"
```

### Bảng thư mục cài đặt mặc định theo Agent

| Agent | Thư mục cài đặt trong dự án |
|---|---|
| Google Antigravity | `.agents/skills/<skill-id>/` |
| OpenAI Codex | `.codex/skills/<skill-id>/` |
| Claude Code | `.claude/skills/<skill-id>/` |
| Cursor | `.cursor/skills/<skill-id>/` |
| Windsurf | `.windsurf/skills/<skill-id>/` |
| Cline / Roo Code | `.cline/skills/<skill-id>/` |
| GitHub Copilot CLI | `.github/skills/<skill-id>/` |

### Yêu cầu tiên quyết & Lưu ý an toàn

- **Biến môi trường**:
  - Với các tác vụ cào dữ liệu trực tiếp từ API ScrapeCreators, cấu hình biến môi trường `SCRAPECREATORS_API_KEY`.
  - Phân tích offline, sinh kịch bản prompt và các quy trình suy luận chiến lược hoạt động độc lập không cần API key.
- **Quyền riêng tư & An toàn**: Quá trình cài đặt `./vas install` chỉ sao chép hoặc tạo liên kết tệp tin tĩnh và ghi receipt `.vas-manifest.json`. Không tự động chạy mã, không cài đặt runtime/MCP hay mở cổng dịch vụ trong lúc cài đặt.

---

## English

Added **13 new skills / 39 files**, zero duplicates skipped.
Upstream: [`ScrapeCreators/social-media-research-skills`](https://github.com/ScrapeCreators/social-media-research-skills) at revision `64ba7b4dea71e130d2712ffb6c1c1024b3b7c4b2`.
Catalog total: **3,872 skills / 119 categories**.
This is the Social Media Intelligence & Research skill suite for **Google Antigravity**, **OpenAI Codex**, **Claude Code**, **Cursor**, **Windsurf**, **Cline**, and **GitHub Copilot CLI**, authored by **ScrapeCreators ([@ScrapeCreators](https://github.com/ScrapeCreators))**:
providing systematic playbooks for analyzing public social data, competitive ad libraries (Meta, Google, LinkedIn), creator profile breakdowns, comment mining (voice-of-customer & sentiment), competitor strategies, content repurposing into multi-channel formats, influencer prospecting, outlier post detection, product demand validation via Reddit & social forums, video transcript intelligence, executive social listening briefs, and niche trend discovery.

The upstream `audience-research` skill is namespaced as `scrapecreators-audience-research` to avoid colliding with an existing ad targeting skill in the catalog.

All skills are distributed under the **MIT License**, Copyright (c) 2026 ScrapeCreators.

### 13 Social Media Research Skills

1. `ad-library-teardown`: Tear down active ad campaigns from Meta, Google, and LinkedIn ad libraries to extract hooks, offers, and creative angles.
2. `scrapecreators-audience-research`: Analyze creator audience demographics, follower geography, and brand sponsorship fit.
3. `comment-mining`: Mine comments and replies for audience reactions, customer language, objections, and product ideas.
4. `competitor-social-research`: Benchmark competitor social strategies, identify content gaps, and plan social content pillars.
5. `content-repurposing`: Turn long-form social videos and transcripts into LinkedIn posts, X threads, short scripts, and carousels.
6. `creator-profile-teardown`: Analyze a creator or brand account's positioning, content pillars, outlier posts, and viral formats.
7. `influencer-prospecting`: Discover, score, and build prospect lists of niche creators for brand partnerships and UGC campaigns.
8. `outlier-post-finder`: Detect viral and overperforming posts versus account baselines to produce practical swipe files.
9. `product-demand-research`: Validate product concepts and unearth customer pain points from Reddit threads and social conversations.
10. `scrapecreators-api`: Integrate the ScrapeCreators REST API to extract public data across 27+ social platforms.
11. `social-listening-brief`: Synthesize brand sentiment, audience themes, and public discussions into actionable executive briefs.
12. `transcript-intelligence`: Extract hooks, key claims, memorable quotes, and reusable scripts from social video transcripts.
13. `trend-discovery`: Surface trending topics, hashtags, audio, and viral formats within specific industry niches.

### No-Clone Web Quickstart (Copy Agent Prompt)

Open [Social Media Research on VAS](https://huytran1120.github.io/vie-agentic-skills/?lang=en&sources=scrapecreators), pick your coding agent (Antigravity, Cursor, Claude Code, Codex, etc.), click **Copy Agent Prompt**, and paste it into your project chat window.

Your agent reads `install-manifests/<canonical-id>.json`, verifies every SHA-256 hash, downloads the complete payload, and saves the CLI-compatible `.vas-manifest.json` receipt.

### CLI Instructions (`./vas`)

From your local VAS repository checkout:

```bash
# Search for skills
./vas search scrapecreators
./vas search ad-library-teardown

# View skill runbook
./vas show ad-library-teardown
./vas show scrapecreators-audience-research

# Install in copy mode
./vas install ad-library-teardown --target claude --mode copy --dest "/path/to/project/.claude/skills"

# Install in symlink mode
./vas install trend-discovery --target antigravity --mode link

# Check status
./vas status --target claude --dest "/path/to/project/.claude/skills"

# Uninstall skill
./vas uninstall ad-library-teardown --target claude --dest "/path/to/project/.claude/skills"
```

### Default Agent Installation Destinations

| Agent | Default Project Destination |
|---|---|
| Google Antigravity | `.agents/skills/<skill-id>/` |
| OpenAI Codex | `.codex/skills/<skill-id>/` |
| Claude Code | `.claude/skills/<skill-id>/` |
| Cursor | `.cursor/skills/<skill-id>/` |
| Windsurf | `.windsurf/skills/<skill-id>/` |
| Cline / Roo Code | `.cline/skills/<skill-id>/` |
| GitHub Copilot CLI | `.github/skills/<skill-id>/` |

### Prerequisites & Safety Notes

- **Environment Configuration**:
  - Live API scraping operations utilize `SCRAPECREATORS_API_KEY` for accessing the ScrapeCreators REST API.
  - Offline prompt templating, analytical reasoning, and swipe file frameworks run completely standalone without API credentials.
- **Safe Operation**: Installation via `./vas install` only copies or symlinks static markdown files and writes the `.vas-manifest.json` receipt. No executable scripts, runtimes, MCP servers, or background services are executed during installation.
