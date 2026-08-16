# ProMentor

[中文](README.zh.md)

> Turn any open-source project into an MIT-style hands-on engineering course.

ProMentor is an **AI coding-agent skill**. Once installed, your assistant becomes a mentor: it scans the architecture, writes a leveled chapter plan, walks you through the core logic, grades your labs, and reviews your code against the original design.

**You are not grinding algorithm puzzles. You are learning how a real system is designed.**

Two parallel skills: [`skills/promentor`](skills/promentor) (English) and [`skills/promentor-zh`](skills/promentor-zh) (中文). Install one.

## Golden course

The repo ships a hand-written course that also serves as the quality bar: [`examples/mini-router-en`](examples/mini-router-en). A Python HTTP router under 200 lines (static routes, `:param`, wildcards, middleware), with five lectures, labs, behavior tests, and student stubs.

![How to take the course](examples/mini-router-en/docs/learning-loop.png)

![Course overview](examples/mini-router-en/docs/course-overview.png)

```bash
cd examples/mini-router-en
python3 validate_course.py          # stubs must fail; reference must pass
python3 .promentor/chapters/ch01-static-routes/lab_test.py
```

Open that directory in an agent that supports `/promentor`, then `/promentor learn ch01`. More screenshots: [English course README](examples/mini-router-en).

## Install

### DSH Web GUI dashboard (skip if you are not on DeepSeek Harness)

> DSH only: its dashboard is a **built-in GUI plugin** (Codex / Claude Code and other agents ship a static page with the skill — skip this section). Prebuilt plugin artifacts ship in the Release zip; this repo does not store them.

**Install (one command)**

```bash
# A (recommended): unzip the Release promentor.zip
cd <unzip-dir>/promentor
bash dsh-plugin/install.sh

# B (from source): clone this repo, then make build
cd /path/to/ProMentor
bash dsh-plugin/install.sh
```

- Uninstall: `bash dsh-plugin/uninstall.sh`

### From the Release zip

1. Download the latest `promentor.zip` from [Releases](https://github.com/xiyiji/ProMentor/releases)

2. Put **one** skill folder in `.{YourAgent}/skills/`:
   - `promentor/` — English
   - `promentor-zh/` — 中文

Do not install both. They are parallel skills; pick the language you want the mentor to teach in.

## Usage

Open your project in DSH (DeepSeek Harness), Codex, Claude Code, or any agent that supports `/promentor`, then:

### 1. Generate the course

```
/promentor init
```

The agent scans the project, proposes an outline, and after you confirm, writes lectures, labs, and behavior tests chapter by chapter.

### 2. Learn

```
/promentor learn ch01
```

The agent teaches from the lecture, walks the annotated source, and points you at the interface you must implement.

### 3. Test

```
/promentor test
```

The agent runs the behavior tests and tells you what passed, what failed, and why.

### 4. Hint

```
/promentor hint
```

The agent reads your code and the latest failures and gives **layered hints for this error**. Direction first, then approach — never the full answer.

### 5. Submit

```
/promentor submit
```

Full test run + locked score. Your code is copied into the submission history.

### 6. AI code review

```
/promentor review
```

The agent diffs your implementation against the original source and explains the design decisions — why they did it that way, and how you could improve.

### 7. Progress

```
/promentor          # course panel
/promentor progress # detailed progress
```

### 8. Dashboard

```
/promentor dashboard
```

**DSH Web GUI panel (preferred):** click the `ProMentor` button above the composer. The panel follows the current session workspace and reads `.promentor/` — no local server. Install: **DSH Web GUI dashboard** above (`bash dsh-plugin/install.sh`).

**Standalone dashboard (fallback for Codex / Claude Code):** reads `.promentor/` and opens a browser page next to the agent chat.

**What you get**

- Home: overall completion, current chapter, completed / in-progress / not-started counts, per-chapter status / score / attempts, missing-content warnings
- Chapter pages: `/dashboard/chapters/<chapter_id>/`, refreshable and shareable
- Sidebar: switch Lecture and Source
- Theme toggle in the top right
- Markdown with syntax highlighting, Mermaid, math, and CJK layout (Streamdown)

**Auto-open**

After `/promentor init` and at the start of `/promentor learn <ch>`, the agent tells you to open the GUI panel (or starts the standalone dashboard and prints the URL if the plugin is missing).

**Architecture**

- DSH plugin: host data gateway (`packages/host/promentor`) + GUI panel (`packages/client/ui-promentor`) in the deepseek-harness repo; this repo's `dsh-plugin/` registers them (`install.sh` / `uninstall.sh`)
- Standalone fallback: one global process, reused on repeat start; the page lives only inside the skill's `dashboard/` and is never copied into the project; the server reads `.promentor/` from the project root

Fallback usage:

```
cd /path/to/project
python3 <promentor-skill>/scripts/serve.py          # start and open the browser
python3 <promentor-skill>/scripts/serve.py status   # running process
python3 <promentor-skill>/scripts/serve.py stop     # stop
```

## Commands

| Command | What it does |
|------|------|
| `/promentor init` | Analyze the project and generate the course |
| `/promentor` | Course panel (outline + progress) |
| `/promentor learn <ch>` | Enter a chapter |
| `/promentor test` | Run behavior tests |
| `/promentor hint` | Layered hints for the current error |
| `/promentor submit` | Official submit and lock the score |
| `/promentor review` | Diff your work against the original source |
| `/promentor progress` | Overall progress |
| `/promentor dashboard` | Web dashboard (completion + current chapter + completeness) |

## Learning model

```
Learn Concept     (AI teaches the lecture)
    ↓
Read Source Code  (AI walks the annotated source)
    ↓
Implement Lab     (you write the core logic)
    ↓
Run Tests         (/promentor test)
    ↓
Submit & Review   (/promentor submit → /promentor review)
    ↓
Master System Design
```

## Why ProMentor

- **A path, not a random walk through the repo:** chapters have dependencies
- **Deeper than a video:** you implement the core, you do not watch someone else type
- **More systematic than a blog:** one system's design philosophy, not scattered tips
- **AI-native:** generate, teach, grade, review. Zero manual content production
