# Hi there 👋

I'm **vollegrewar** — an AI-native builder with a professional QA background. I **vibe-code** working systems: I define requirements and the acceptance bar, orchestrate coding agents, verify every iteration, and own what ships. In my projects the implementation is authored by AI under my direction — the problem framing, course-correction, and quality bar are mine.

Active contributor to **[Hermes Agent](https://github.com/NousResearch/hermes-agent)** (246k ⭐) and **[Hugging Face Hub](https://github.com/huggingface/huggingface_hub)** — often as the Windows side of the story: reproductions, multi-round verification, and patches.

## 🛠 Tech Stack

**What I drive hands-on**

![Agent Orchestration](https://img.shields.io/badge/-Agent_Orchestration-4B0082?style=flat)
![Spec & Prompt Engineering](https://img.shields.io/badge/-Spec_%26_Prompt_Engineering-7E57C2?style=flat)
![QA & Acceptance](https://img.shields.io/badge/-QA_%26_Acceptance-2E7D32?style=flat)
![ComfyUI](https://img.shields.io/badge/-ComfyUI-1A1A2E?style=flat)
![Ollama](https://img.shields.io/badge/-Ollama-000000?style=flat)

**What ships under the hood** — implemented by AI, spec'd & accepted by me

![Python](https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=white&style=flat)
![JavaScript](https://img.shields.io/badge/-JavaScript-F7DF1E?logo=javascript&logoColor=black&style=flat)
![FastAPI](https://img.shields.io/badge/-FastAPI-009688?logo=fastapi&logoColor=white&style=flat)
![CDP Automation](https://img.shields.io/badge/-CDP_Automation-4285F4?logo=googlechrome&logoColor=white&style=flat)
![OpenCV](https://img.shields.io/badge/-OpenCV-5C3EE8?logo=opencv&logoColor=white&style=flat)
![Chrome MV3](https://img.shields.io/badge/-Chrome_MV3-4285F4?logo=googlechrome&logoColor=white&style=flat)
![SQLite](https://img.shields.io/badge/-SQLite-003B57?logo=sqlite&logoColor=white&style=flat)

## 🤝 Open Source

I file bugs with reproduction evidence, verify fixes on real Windows environments, and land patches where I can. Selected contributions:

| Contribution | Note | Status |
|---|---|---|
| [huggingface_hub #4637](https://github.com/huggingface/huggingface_hub/issues/4637) · [#4648](https://github.com/huggingface/huggingface_hub/pull/4648) | `snapshot_download` misreported mirror 308-redirects as missing files — my issue + fix approach **adopted upstream** | ✅ Merged ([#4739](https://github.com/huggingface/huggingface_hub/pull/4739)) |
| [hermes-agent #82581](https://github.com/NousResearch/hermes-agent/pull/82581) · [#74817](https://github.com/NousResearch/hermes-agent/issues/74817) | Windows 11 junction-install reproduction + multi-round retest of the subprocess-isolation fix — maintainer cited "the real Windows 11 junction verification" | ✅ Merged ([#88285](https://github.com/NousResearch/hermes-agent/pull/88285)) |
| [hermes-agent #110721](https://github.com/NousResearch/hermes-agent/pull/110721) | Derive sprite cell size from the atlas grid — 2x-resolution pet atlases now render end-to-end | 🟡 Open PR |
| [hermes-agent #112158](https://github.com/NousResearch/hermes-agent/pull/112158) | My [anysearch plugin](https://github.com/vollegrewar/hermes-plugin-anysearch) proposed to the official plugin catalog | 🟡 Open PR |
| [hermes-agent #109680](https://github.com/NousResearch/hermes-agent/issues/109680) | Stale state + PID reuse fabricated a phantom gateway runtime, silently breaking updates — root-caused | ✅ Fixed |
| [hermes-agent #78981](https://github.com/NousResearch/hermes-agent/issues/78981) | 500k-token session dying permanently after context-compression hangs | ✅ Fixed |
| [hermes-agent #80498](https://github.com/NousResearch/hermes-agent/issues/80498) | Silent tool-call argument loss when a stream dies mid-call (no retry, `write_file` never ran) | ✅ Fixed |
| [hermes-agent #98436](https://github.com/NousResearch/hermes-agent/issues/98436) | Windows `hermes update` silently loses its receipt; console end state looks hung | ✅ Fixed |

> Also on huggingface_hub: a formal review on [#4644](https://github.com/huggingface/huggingface_hub/pull/4644) (preserving query strings through relative redirects) — same fix lineage as the adopted [#4739](https://github.com/huggingface/huggingface_hub/pull/4739).

### Hermes Agent — full log

<!-- CONTRIB_BADGES -->
[![Issues](https://img.shields.io/badge/Issues-11-blue?logo=github&logoColor=white)](https://github.com/NousResearch/hermes-agent/issues?q=author%3Avollegrewar)
[![PRs](https://img.shields.io/badge/PRs-4-brightgreen?logo=github&logoColor=white)](https://github.com/NousResearch/hermes-agent/pulls?q=author%3Avollegrewar)
[![Involved](https://img.shields.io/badge/Involved-34-orange?logo=github&logoColor=white)](https://github.com/NousResearch/hermes-agent/issues?q=involves%3Avollegrewar)
<!-- /CONTRIB_BADGES -->

<details>
<summary><b>All tracked contributions</b> — issues, PRs &amp; verifications, auto-refreshed weekly</summary>

<!-- CONTRIB_TABLE -->
| # | Type | Role | Title | Status |
|--|------|------|-------|--------|
| [#112158](https://github.com/NousResearch/hermes-agent/pull/112158) | PR | Author | catalog: add anysearch (community web search/extract plugin) | 🟢 Open |
| [#110721](https://github.com/NousResearch/hermes-agent/pull/110721) | PR | Author | feat(pets): derive sprite cell size from the atlas grid | 🟢 Open |
| [#109680](https://github.com/NousResearch/hermes-agent/issues/109680) | Issue | Author | [Bug]: stale gateway_state.json + PID reuse fabricates a phantom gateway runtime in the pre-update inventory — update exits 1 (partial) with "no rows" + "never touched" warnings | 🔴 Closed |
| [#108630](https://github.com/NousResearch/hermes-agent/issues/108630) | Issue | Author | [Bug] Auto-archive leaves the canonical "Bot Chat" with no recoverable end_reason — permanent title deadlock not covered by #92687 / #92473 | 🟢 Open |
| [#107823](https://github.com/NousResearch/hermes-agent/pull/107823) | PR | Participant | fix(desktop): restore minimized sessions from sidebar toggle | 🔴 Closed |
| [#103793](https://github.com/NousResearch/hermes-agent/issues/103793) | Issue | Participant | [Bug][Windows] Local STT fails: "Library cublas64_12.dll is not found or cannot be loaded" — fix via CUDA 12 wheels in the venv (GPU) or forcing CPU | 🟢 Open |
| [#102398](https://github.com/NousResearch/hermes-agent/issues/102398) | Issue | Author | [Feature]: Desktop Settings — a visible, per-profile approvals.mode selector | 🔴 Closed |
| [#98436](https://github.com/NousResearch/hermes-agent/issues/98436) | Issue | Author | [Bug][Windows] hermes update hand-off child silently loses its update receipt after the catch-up module purge — console end state also looks hung | 🔴 Closed |
| [#86272](https://github.com/NousResearch/hermes-agent/pull/86272) | PR | Author | [codex] fix desktop profile project gateway routing | 🔴 Closed |
| [#86107](https://github.com/NousResearch/hermes-agent/issues/86107) | Issue | Author | [Bug]: Desktop — single explicit project entry vanishes from sidebar Projects list mid-session; survives restart (backend intact) | 🟢 Open |
| [#83192](https://github.com/NousResearch/hermes-agent/issues/83192) | Issue | Author | Bug: find-in-page bar (Ctrl+F) overlaps native window controls on Windows — verified, covered by #80244 | 🔴 Closed |
| [#82689](https://github.com/NousResearch/hermes-agent/issues/82689) | Issue | Author | kanban: no operator audit on assign + dispatcher executes side-effectful tasks without authorization gate | 🟢 Open |
| [#82635](https://github.com/NousResearch/hermes-agent/issues/82635) | Issue | Author | [Bug]: Desktop Settings → Chat timezone dropdown truncates long IANA option names — popover width pinned to trigger | 🟢 Open |
| [#82581](https://github.com/NousResearch/hermes-agent/pull/82581) | PR | Participant | fix(tools): isolate subprocess Python environments (#74817) | 🔴 Closed |
| [#82505](https://github.com/NousResearch/hermes-agent/pull/82505) | PR | Author | fix(desktop): deterministic title for untitled chat sessions | 🟢 Open |
| [#80542](https://github.com/NousResearch/hermes-agent/issues/80542) | Issue | Author | [Feature]: Desktop — untitled sessions are unidentifiable (86% of sessions have NULL title; no meaningful fallback label) | 🟢 Open |
| [#80498](https://github.com/NousResearch/hermes-agent/issues/80498) | Issue | Author | Tool-call arguments silently replaced with empty object when stream dies mid-call — silent data loss, no retry (write_file never executed) | 🔴 Closed |
| [#80244](https://github.com/NousResearch/hermes-agent/pull/80244) | PR | Participant | fix(desktop): keep the find bar clear of the window controls | 🔴 Closed |
| [#80204](https://github.com/NousResearch/hermes-agent/issues/80204) | Issue | Participant | [Bug]: Hermes Desktop leaves orphaned `hermes serve`, MCP watchdog, and daemon Python processes after exit/update | 🔴 Closed |
| [#80122](https://github.com/NousResearch/hermes-agent/pull/80122) | PR | Participant | fix(agent): handle auxiliary stream stalls and prevent turn ghosting  | 🔴 Closed |
| [#78981](https://github.com/NousResearch/hermes-agent/issues/78981) | Issue | Author | Session permanently dies after repeated context-compression hangs (DeepSeek 500k-token session): stalled stream waits 600s ceiling, interrupted turn never recovers, later messages never start a turn | 🔴 Closed |
| [#77394](https://github.com/NousResearch/hermes-agent/issues/77394) | Issue | Participant | Windows: hermes update still fails on main — paused gateway keeps _rust.pyd locked (fix #73684 does not cover respawned gateways) | 🟢 Open |
| [#77156](https://github.com/NousResearch/hermes-agent/pull/77156) | PR | Participant | feat(temperature): add per-session and global sampling temperature control | 🟢 Open |
| [#76886](https://github.com/NousResearch/hermes-agent/issues/76886) | Issue | Participant | read_file reports valid UTF-8 text as binary when the 1000-byte sample cuts a multibyte character (regression in 0.19.1) | 🔴 Closed |
| [#75334](https://github.com/NousResearch/hermes-agent/issues/75334) | Issue | Participant | Bug: Desktop self-update always aborts when a non-Desktop-owned gateway process holds the venv lock (Windows) | 🟢 Open |
| [#74817](https://github.com/NousResearch/hermes-agent/issues/74817) | Issue | Participant | PYTHONPATH leaks into terminal-tool subprocesses on macOS/Linux, can crash unrelated third-party apps | 🔴 Closed |
| [#74443](https://github.com/NousResearch/hermes-agent/pull/74443) | PR | Participant | feat: honor model temperature configuration | 🟢 Open |
| [#67463](https://github.com/NousResearch/hermes-agent/pull/67463) | PR | Participant | fix(desktop): split sidebar into independent Projects + Sessions collapsible sections (#67368) | 🟢 Open |
| [#59041](https://github.com/NousResearch/hermes-agent/pull/59041) | PR | Participant | fix: prevent credential pool poisoning from model-not-found 401s and api_mode persistence | 🔴 Closed |
| [#51893](https://github.com/NousResearch/hermes-agent/pull/51893) | PR | Participant | fix(desktop): handle notification action indexes | 🔴 Closed |
| [#51444](https://github.com/NousResearch/hermes-agent/issues/51444) | Issue | Participant | [Bug]: Approval from notification doesn't work | 🔴 Closed |
| [#46169](https://github.com/NousResearch/hermes-agent/issues/46169) | Issue | Participant | Desktop should support Ctrl+F/Cmd+F find across chat and UI editors | 🔴 Closed |
| [#41165](https://github.com/NousResearch/hermes-agent/pull/41165) | PR | Participant | [Feature] Add AnySearch as a built-in web search provider (search + extract) | 🔴 Closed |
| [#29457](https://github.com/NousResearch/hermes-agent/issues/29457) | Issue | Participant | [Feature]: Kanban task request for approval | 🟢 Open |
<!-- /CONTRIB_TABLE -->

</details>

## 📦 Selected Projects

⭐ **Flagship public project**

> **[ai-writing-pipeline-demo](https://github.com/vollegrewar/ai-writing-pipeline-demo)** — a reproducible 4-phase pipeline for 100K+-character long-form generation (analysis → outline → writing → review): multi-model orchestration with degraded paths, consistency gates, a de-AI-flavor rule system, and corpus data engineering. Distilled from a real long-running project; no content included.

More public repos: [hermes-plugin-anysearch](https://github.com/vollegrewar/hermes-plugin-anysearch) · [dsh-tool-highlight](https://github.com/vollegrewar/dsh-tool-highlight) · [windows-terminal-hygiene](https://github.com/vollegrewar/windows-terminal-hygiene)

**Private builds** — engineering showcase; domain & stack only

| Build | Stack | Engineering I drove |
|---|---|---|
| 🎮 Game rescue automation | Python · CDP · OpenCV · Flask | Event-driven state machine; visual template matching; humanized input (timing jitter, Bézier click paths, real wheel events) with explicit no-spoofing red lines |
| 🕷️ Corpus crawler & data pipeline | Python · requests · BeautifulSoup | UTF-8/Big5 dual-encoding; domain-level proxy routing; resumable error recovery; forum adapter |
| 🌐 Local writing client & E2E harness | FastAPI · HTMX · Playwright | Project/chapter registry API; human-like Playwright E2E suite |
| 🖼️ Generation-pipeline tooling | ComfyUI · Ollama | Node-level workflows; 9-state sprite-sheet pipeline with pixel-level QA (feeds the upstream renderer fix [#110721](https://github.com/NousResearch/hermes-agent/pull/110721)) |

## 📊 GitHub Stats

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://github-readme-stats.vercel.app/api?username=vollegrewar&show_icons=true&theme=dark&hide_border=true&count_private=true&include_all_commits=true" />
    <img src="https://github-readme-stats.vercel.app/api?username=vollegrewar&show_icons=true&theme=default&hide_border=true&count_private=true&include_all_commits=true" height="160" alt="GitHub Stats" />
  </picture>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://github-readme-stats.vercel.app/api/top-langs/?username=vollegrewar&layout=compact&theme=dark&hide_border=true&langs_count=6" />
    <img src="https://github-readme-stats.vercel.app/api/top-langs/?username=vollegrewar&layout=compact&theme=default&hide_border=true&langs_count=6" height="160" alt="Top Languages" />
  </picture>
</p>

---

*Contribution log auto-refreshed weekly via GitHub Actions.*
