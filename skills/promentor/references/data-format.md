# .promentor/ data format (full spec)

> Detail pulled down from SKILL.md §1. Read this when reading or writing course.json / progress.json / lab.json.

## Contents

- [1.1 Layout](#11-layout)
- [1.2 course.json](#12-coursejson)
- [1.3 progress.json](#13-progressjson)
- [1.4 lab.json](#14-labjson)
- [1.5 lecture.md](#15-lecturemd)
- [1.6 source.md](#16-sourcemd)

## 1.1 Layout

```
.promentor/
├── course.json                  # course metadata
├── progress.json                # learning progress
├── chapters/
│   ├── ch01-<slug>/
│   │   ├── lecture.md           # lecture (Markdown)
│   │   ├── source.md            # source guide (key lines annotated)
│   │   ├── lab.json             # lab: signatures and requirements
│   │   └── lab_test.<ext>       # behavior tests (student must not edit)
│   └── ch02-<slug>/
└── submissions/
    └── ch01-<slug>/
        ├── attempt_1.<ext>
        └── attempt_2.<ext>
```

## 1.2 course.json

```json
{
  "project": "gin",
  "language": "go",
  "generated_at": "2026-07-31T10:00:00Z",
  "chapters": [
    {
      "id": "ch01-http-server",
      "title": "HTTP server basics",
      "difficulty": "mid",
      "prerequisites": [],
      "learning_goals": [
        "Understand the net/http Server lifecycle",
        "See why the Handler interface is shaped this way"
      ],
      "source_files": ["gin.go:1-120"],
      "lab_interface": {
        "package": "httpserver",
        "exports": ["NewServer", "Server.ServeHTTP"]
      }
    }
  ]
}
```

Fields:
- `id`: `ch<NN>-<slug>` — two-digit index, hyphen, English slug
- `difficulty`: `easy` | `mid` | `hard`
- `prerequisites`: ids of earlier chapters
- `source_files`: original files and line ranges for this chapter
- `lab_interface`: the public interface the student implements

## 1.3 progress.json

```json
{
  "project_name": "gin",
  "current_chapter": "ch02-router",
  "chapters": {
    "ch01-http-server": {
      "status": "completed",
      "score": 95.0,
      "attempts": 3,
      "hint_level_reached": 1,
      "completed_at": "2026-07-30T15:04:05Z"
    },
    "ch02-router": {
      "status": "in_progress",
      "score": 0,
      "attempts": 5,
      "hint_level_reached": 2
    }
  }
}
```

- `status`: `not_started` | `in_progress` | `completed`
- `score`: 0-100; set on submit
- `attempts`: submit count
- `hint_level_reached`: highest hint level reached in this chapter

## 1.4 lab.json

```json
{
  "chapter_id": "ch02-router",
  "title": "Router design",
  "description": "Implement a router with path params and HTTP method matching",
  "language": "go",
  "package": "router",
  "files": [
    {
      "path": "router.go",
      "description": "Core router implementation"
    }
  ],
  "interface": {
    "types": [
      {
        "name": "Router",
        "kind": "struct",
        "doc": "HTTP router: stores the table and looks up handlers"
      },
      {
        "name": "Handler",
        "kind": "type",
        "doc": "type Handler func(w http.ResponseWriter, req *http.Request)"
      }
    ],
    "functions": [
      {
        "signature": "func NewRouter() *Router",
        "doc": "Create a Router"
      },
      {
        "signature": "func (r *Router) AddRoute(method, path string, handler Handler)",
        "doc": "Register a route. path may contain :param segments"
      },
      {
        "signature": "func (r *Router) FindRoute(method, path string) (Handler, map[string]string)",
        "doc": "Look up a route. Returns handler and path params. handler is nil on a miss"
      }
    ]
  },
  "test_command": "cd .promentor/chapters/ch02-router && go test -v -json ./..."
}
```

- `interface.functions[].signature` is binding
- `test_command` is a shell command; `{chapter_dir}` is replaced with the chapter directory

## 1.5 lecture.md

Lectures are Markdown.

1. **Lead:** first paragraph says what this chapter teaches and why it matters
2. **Ideas:** one subsection per concept, with snippets
3. **Decisions:** why this design, not the alternative
4. **Hand-off:** end with what to implement and which lecture ideas it uses
5. **Length:** at most 300 lines; stay on the core

## 1.6 source.md

A reading guide over the original source:

```markdown
# Source guide: Router design

## Core file: `gin.go:45-120`

### Data structure (:45-:60)
[Why the Router is shaped this way]

### Registration (:62-:85)
[How AddRoute registers]

### Lookup (:87-:120)
[FindRoute algorithm; mark the key lines]
```

- Only code that belongs to this chapter
- Every block has line numbers
- Explain "why", not only "what"
