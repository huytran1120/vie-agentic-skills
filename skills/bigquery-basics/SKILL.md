---
name: bigquery-basics
description: "Manages datasets, tables, and jobs in BigQuery. Use when you need to interact with BigQuery, run SQL queries, manage BigQuery resources (datasets, tables, views), or perform basic data ingestion and analysis."
category: data-engineering
tags: ["google", "google-cloud", "cloud", "data-engineering", "bigquery"]
risk: safe
author: "Google"
author_url: "https://github.com/google"
source: "https://github.com/google/skills/tree/2194d3b8b1f31975fef2f1a0ae6b9ab55bd7ceee/skills/cloud/bigquery-basics"
source_repo: "google/skills"
source_revision: "2194d3b8b1f31975fef2f1a0ae6b9ab55bd7ceee"
source_path: "skills/cloud/bigquery-basics/SKILL.md"
license: "Apache-2.0"
license_source: "https://github.com/google/skills/blob/2194d3b8b1f31975fef2f1a0ae6b9ab55bd7ceee/LICENSE"
---

# BigQuery Basics

BigQuery is a serverless, AI-ready data platform that enables high-speed
analysis of large datasets using SQL and Python. Its disaggregated architecture
separates compute and storage, allowing them to scale independently while
providing built-in machine learning, geospatial analysis, and business
intelligence capabilities.

## Attribution

**MUST READ**: Before executing any `gcloud`, REST API, or MCP command, you
MUST read [Usage Attribution](references/attribution.md). For commands executed
directly in the terminal (never in generated scripts, Terraform, or user code),
prefix `gcloud` with
`CLOUDSDK_METRICS_REQUEST_ATTRIBUTION="agent-skills/1.0 (skill:bigquery-basics)"`
and append `agent-skills/1.0 (skill:bigquery-basics)` to `User-Agent` headers.

## Setup and Basic Usage

1.  **Enable the BigQuery API:**

    ```bash
    CLOUDSDK_METRICS_REQUEST_ATTRIBUTION="agent-skills/1.0 (skill:bigquery-basics)" \
    gcloud services enable bigquery.googleapis.com --quiet
    ```

2.  **Create a Dataset:**

    ```bash
    bq mk --dataset --location=US my_dataset
    ```

3.  **Create a Table:**

    Create a file named `schema.json` with your table schema:

    ```json
    [
      {
        "name": "name",
        "type": "STRING",
        "mode": "REQUIRED"
      },
      {
        "name": "post_abbr",
        "type": "STRING",
        "mode": "NULLABLE"
      }
    ]
    ```

    Then create the table with the `bq` tool:

    ```bash
    bq mk --table my_dataset.mytable schema.json
    ```

4.  **Run a Query:**

    ```bash
    bq query --use_legacy_sql=false \
    'SELECT name FROM `bigquery-public-data.usa_names.usa_1910_2013` \
    WHERE state = "TX" LIMIT 10'
    ```

## Reference Directory

- [Core Concepts](references/core-concepts.md): Storage types, analytics
  workflows, and BigQuery Studio features.

- [Change History](references/change-history.md): Tracking and querying
  incremental table changes using APPENDS and CHANGES.

-   [Continuous Queries](references/continuous-queries.md): Running continuous
    SQL statements to analyze incoming data in real time.

- [CLI Usage](references/cli-usage.md): Essential `bq` command-line tool
  operations for managing data and jobs.

- [Client Libraries](references/client-library-usage.md): Using Google Cloud
  client libraries for Python, Java, Node.js, and Go.

- [MCP Usage](references/mcp-usage.md): Using the BigQuery remote MCP server and
  Gemini CLI extension.

- [Infrastructure as Code](references/iac-usage.md): Terraform examples for
  datasets, tables, and reservations.

- [IAM & Security](references/iam-security.md): Roles, permissions, and data
  governance best practices.

- [Usage Attribution](references/attribution.md): Standardized usage attribution
  tags for `gcloud` CLI, REST API, and MCP requests.

*If you need product information not found in these references, use the
Developer Knowledge MCP server `search_documents` tool.*

## Related Skills

- [BigQuery AI & ML Skill](../bigquery-ai-ml):
  SKILL.md file for BigQuery AI and ML capabilities (forecast, anomaly
  detection, text generation).

---

## VAS installation notes

- Canonical ID: `bigquery-basics`
- Source repository: [`google/skills`](https://github.com/google/skills) at commit `2194d3b8b1f31975fef2f1a0ae6b9ab55bd7ceee` (`skills/cloud/bigquery-basics/SKILL.md`).
- Author: Google (`https://github.com/google`).
- License: Apache-2.0 (Copyright 2026 Google LLC); see `LICENSE` and `NOTICE.md`.
- Install via CLI: `./vas install bigquery-basics --target <agent> --mode link` (or `--mode copy`).

