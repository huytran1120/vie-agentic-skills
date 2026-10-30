---
name: ml-kit-genai-prompt-api
description: >-
  Analyzes Android codebases to implement ML Kit GenAI Prompt API. Use this skill to send natural language requests on-device to Gemini Nano, use structured output with Prompt API, implement prefix caching, optimize the current prompt, or apply best practices.
license: Apache-2.0
metadata:
  author: Google LLC
  last-updated: '2026-09-03'
  keywords:
  - ML Kit
  - Prompt API
  - Structured Output
  - Prefix Caching
  - Gemini Nano
---

This skill provides step-by-step guidance for integrating and optimizing the ML
Kit GenAI Prompt API in Android apps.

## Prerequisites

- Android API level must be 26 or higher. If `minSdk` is below 26, update it to 26.
- Add the ML Kit GenAI Prompt API dependency (`com.google.mlkit:genai-prompt`) to the app-level `build.gradle` file, with version at least `1.0.0-beta4`.
- If `com.google.mlkit:genai-schema-compiler` dependency is used and KSP plugin version is below 2.3.6, update it to 2.3.6.

## Detailed steps

### 1. Prompt optimization

To optimize prompts for use with the ML Kit Prompt API, follow the
[prompt optimization guide](https://developer.android.com/agents/skills/device-ai/prompt-api/references/prompt-optimization).

### 2. Prefix caching optimization

If the prompt is more than 200 words, implement the [prefix caching API](https://developer.android.com/agents/skills/device-ai/prompt-api/references/prefix-caching).

### 3. Lifecycle and best practices

- The model must be fully downloaded and available before calling the first inference. Follow the guide on [implementing a generative model](https://developer.android.com/agents/skills/device-ai/prompt-api/references/get-started) to check that the `FeatureStatus` of a model is `AVAILABLE` before making an inference.
- Release ML Kit instances by calling `close()` when an `Activity`,
  `Fragment`, or `ViewModel` is destroyed. Example:


  ```kotlin
  // Instantiating model in activity, fragment, or ViewModel
      val generativeModel = Generation.getClient()

  // When activity, fragment, or ViewModel is destroyed
      generativeModel.close()
  ```

  <br />

### 4. Structured output

When implementing or refactoring a prompt to use structured output, follow
these rules:

1. **Check for API availability:** Verify Structured Output feature is available on the device with `isStructuredOutputFeatureAvailable()` before using it. Refer to the [Structured Output API guide](https://developer.android.com/agents/skills/device-ai/prompt-api/references/structured-output) for full instructions.
2. **Return type:** Return the `@Generable` typed object from the function
   signature instead of a `String` or JSON string.

   For example:

       fun parseEmail(email: String): String {
           ... 
       }

   should be refactored to:

       fun parseEmail(email: String): ParsedEmail? {
           ...
       }

3. **Example:**

   This is the example code before refactoring:


   ```kotlin
   suspend fun parseEmail(email: String): String {
       val parseEmailPrompt = "Parse this email and return the sender, title, and short summary of the email less than 10 words: "

       val parsedEmail = generativeModel.generateContent(parseEmailPrompt + email)

       return parsedEmail.candidates[0].text
   }
   ```

   <br />

   This is the example code after using Structured Output API:


   ```kotlin
   @Generable
   data class ParsedEmail(
       @Guide(description = "Sender of the email")
       var sender: String = "",

       @Guide(description = "Title of the email")
       var title: String = "",

       @Guide(description = "Summary of the email less than 10 words")
       var summary: String = ""
   )

   suspend fun parseEmail(email: String): ParsedEmail? {
       val parseEmailPrompt =
           "Parse this email: $email"

       val baseRequest = GenerateContentRequest.Builder(TextPart(parseEmailPrompt)).build()
       val typedRequest = generateTypedContentRequest(baseRequest, ParsedEmail::class)
       val typedResponse = generativeModel.generateContent(typedRequest)
       return typedResponse.candidates[0].response
   }
   ```

   <br />


## VAS installation notes

Distributed from android/skills at
`6daa53ef27fa2aa87827d183a85c06cedceca833` under Apache-2.0, by Google LLC and
the Android Open Source Project. Original copyright headers are retained and
the complete upstream LICENSE.txt is included with every standalone skill.
Only the frontmatter description/license formatting and these VAS notes differ;
the original workflow and all supporting files are preserved.

Use the VAS website's Copy Agent Prompt or `./vas install <skill-id> --target <agent>`
with VAS's existing agent-folder mapping. Installing this skill only copies or
links its files and writes the CLI-compatible receipt. It does not install or
update Android CLI, SDK, Gradle, JDK, Python packages, plugins, MCP servers,
models or native binaries, connect to devices/services, run bundled helpers,
collect traces or send app source, credentials or application data.

Before using a workflow, check the project's compatible SDK/JDK/Gradle/library
versions and any required device, emulator, preview access or account. External
documentation, libraries, model weights and services are not bundled snapshots
and may have separate terms. Obtain explicit permission before downloads,
installer execution, package installation, telemetry, network requests, device
changes, sensitive-data processing or paid operations. Review downloaded code
and its provenance before execution; never pipe a network installer into a shell.
Surface missing prerequisites and command failures rather than inventing results.

The r8-analyzer protobuf converter needs a compatible google.protobuf runtime
(the bundled generated module declares version 6.33.4); this dependency is not
installed automatically. Its keep_radius_pb2.py helper is bundled locally.
play-policy-insights includes its scanner, scraper and template_engine helpers;
scraping Play Store pages requires network access and consent, and its report
is assistance, not a guarantee of Google Play approval or legal compliance.
android-profiler includes the upstream Perfetto Python launcher, not native
Perfetto binaries: running it can download/cache and execute a platform binary.
Review its pinned URL/hash and cache destination before approving execution.
Keep upstream executable permissions; the launcher is non-executable upstream
and can be invoked with python3 only after approval. No helpers were run and
no runtime packages or external binaries were installed during this import.
