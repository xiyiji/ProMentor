# Scanning and course generation (full spec)

> Detail pulled down from SKILL.md §4. Read this when running `/promentor init`. Example languages are illustrations; the rules are language-agnostic.

## Contents

- [4.1 Four-pass scan](#41-four-pass-scan)
- [4.2 Trimming large repos (>200 files)](#42-trimming-large-repos-200-files)
- [4.3 Difficulty](#43-difficulty)
- [4.4 Chapter generation](#44-chapter-generation)
- [4.5 Test generation](#45-test-generation)
- [4.6 Cross-chapter lab decoupling](#46-cross-chapter-lab-decoupling)

## 4.1 Four-pass scan

**Pass 1: Structure**

```
Goal: size, language, module boundaries

Do:
• File tree (skip .gitignore, vendor, node_modules, test dirs)
• Find main / entry files
• Find package / namespace / module declarations
• Count files and lines

Out: project metadata (language, size, entry points, top-level modules)
```

**Pass 2: Core types**

```
Goal: the core data structures and abstractions

Do:
• Search type / class / interface declarations
• Read full source for the important types
• Note embedding / inheritance / composition
• Mark public API vs internals

Out: type list + relationship sketch
```

**Pass 3: Call chains**

```
Goal: a full request/data lifecycle

Do:
• From the entry point, read the important function bodies
• Trace calls (search name references)
• Note depth and key branches
• Mark extension points (interface impls, callbacks, plugins)

Out: core-flow call chain + key methods
```

**Pass 4: Architecture**

```
Goal: name the patterns; propose a teaching path

Do:
• Fold the first three passes into layers
• Name patterns (middleware chain, route tree, context, factory, …)
• Mark sharp decisions ("why A instead of B")
• Propose chapter boundaries and order

Out: outline + teaching focus per chapter
```

## 4.2 Trimming large repos (>200 files)

When the tree is larger than 200 files, focus:

**Topology:** BFS from the entry point
- First 3 layers: core — read the source
- Layers 4–6: support — signatures + comments
- Layer 7+: skip (deps, helpers)

**Dedup:**
- Many controllers that only differ by route → go deep on one
- Many middleware that only differ by body → go deep on one
- The rest: filename + one sentence

**Priority:**
- P0: entry file, core types, entry method bodies
- P1: core algorithms, key call chains
- P2: helpers, config, constants
- Exclude: test, mock, vendor, generated

## 4.3 Difficulty

| Level | What it looks like |
|------|---------------------|
| `easy` | Obvious idea, short code (<100 lines), idiomatic |
| `mid` | 1–2 design decisions, medium size, some prerequisites |
| `hard` | The project's sharpest design; non-obvious architecture; 2+ prior concepts |

Mark a chapter `hard` when:
- It needs "why A instead of B"
- The data-structure choice is non-trivial
- Understanding it needs two or more prior ideas
- A bug here fails the system in a quiet way

## 4.4 Chapter generation

**lecture.md:**

Input: original source for this chapter + outline context

Must:
1. Open with one sentence: what this chapter teaches
2. Place it in the system
3. One subsection per core idea
4. Each idea gets an original snippet (mark the key lines)
5. Explain the decision: "why this design"
6. End with what the lab must implement

**source.md:**

Input: the original files for this chapter

Must:
1. List key files and line ranges
2. Each block: what it does and why
3. Mark core types, the main algorithm, sharp tricks
4. Only what belongs to this chapter

**lab.json:**

Input: the core interface in the original source

Must:
1. Types and function signatures the student implements
2. Signatures exact (names, types, returns)
3. A `test_command` that actually runs

**lab_test.<ext>:**

Input: the original core logic

Must:
1. Black-box: input/output only, not the implementation
2. The target language's native test runner
3. Cover happy path, edges, errors
4. Import the student's package
5. Live under `.promentor/chapters/{chapter_id}/`
6. Compile and run on their own

**Runnable entry (Final / assemble chapter):**

After the Final chapter wires the top component, generate an entry so the course "runs when you finish":

1. Put it at the course root (`.promentor/main.go`, `main.py`, `index.js`, … — follow the language). Not inside a chapter dir, so it does not clash with the chapter package
2. The entry only: init data, build the top object, start the runtime (CLI/TUI/Web as the project does)
3. Put the run command in `lab.json` notes (`go run .promentor`, `python3 .promentor/main.py`, `node .promentor/index.js`)
4. Check it with the language's build or syntax tool (`go build`, `python3 -m py_compile`, `tsc --noEmit`) so the finished course actually runs

## 4.5 Test generation

**Black-box:** you do not care how they implemented it, only that input/output is right.

**Go example:**

```go
package router_test

import (
    "testing"
    student "github.com/user/project/.promentor/chapters/ch02-router"
)

func TestStaticRoute(t *testing.T) {
    r := student.NewRouter()
    var called bool
    r.AddRoute("GET", "/users", func(w http.ResponseWriter, req *http.Request) {
        called = true
        w.WriteHeader(200)
    })
    handler, _ := r.FindRoute("GET", "/users")
    if handler == nil {
        t.Fatal("GET /users: no handler")
    }
}
```

**Python example:**

```python
import pytest
import sys
sys.path.insert(0, ".promentor/chapters/ch02-router")
from router import Router

def test_static_route():
    r = Router()
    called = False
    def handler(request):
        nonlocal called
        called = True
        return {"status": 200}
    r.add_route("GET", "/users", handler)
    h, params = r.find_route("GET", "/users")
    assert h is not None, "GET /users: no handler"
```

**Constraints:**
- Tests and student code are different packages/modules; tests import the student
- Cover: happy path, params, wrong method, edges, nested params
- Test names describe the scenario

## 4.6 Cross-chapter lab decoupling

Chapters are learned in dependency order. A later chapter's package does not exist until the student finishes it (e.g. Ch4 needs Ch2's store, and Ch5's form is not there yet). When generating labs:

1. **Prerequisites only point at finished chapters.** `prerequisites` must match real module deps. Student code may only import earlier chapters.
2. **Missing later deps go in notes.** If a later chapter is not built yet, say "return self / a stub" in `lab.json` notes. Tests must not cover that path.
3. **Cross-module types live in the current lab.** Messages/types passed between components are defined in the module the student is writing. Tests must not import the real project source.
4. **No cycles.** If A "opens B's page" and B "returns to A," they import each other. Keep A→B only; B's back-action stays on itself or a stub. The full loop is a challenge in notes.
5. **Assert the real behavior.** A black-box assert must not contradict the original design (e.g. still showing the device name after a successful delete), or it will fail a correct solution.
