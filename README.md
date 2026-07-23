# spec-forge

Skill pack for Claude Code and Opencode implementing a staged, file-driven planning workflow.

## Workflows

**Classic pipeline** (structured spec-first):
```
draft.md
  -> /draft-discussion    -> discussion.md (+ discussion-qa.md)
  -> /discussion-analysis -> analysis.md
  -> /analysis-plan       -> plan.md  (review + approve before next step)
  -> /plan-tasks          -> tasks/todo/<prefix>-task-01.md
                             tasks/todo/<prefix>-task-02.md
                             ...
  -> /task-execute        -> implements one task, verifies, moves todo/ -> done/
  -> /code-review         -> (optional) review report (quality, security, performance, spec, tests)
  -> /task-verify         -> (optional) read-only re-check of a task's acceptance criteria
```

**Agile pipeline** (idea-to-vertical-slices):
```
idea
  -> /grill-me            -> grilled-notes.md (idea exploration + codebase grounding)
  -> /to-prd              -> prd.md (user stories + acceptance criteria)
  -> /to-issues           -> tasks/todo/<prefix>-task-01.md (vertical slices)
  -> /tdd                 -> code + tests (red-green-refactor loop, moves todo/ -> done/)
  -> /code-review         -> (optional) review report (quality, security, performance, spec, tests)
```

Optional, before either pipeline: `/project-principles` -> overview/principles.md (project-wide rules the pipeline reads)

At session end: `/handoff` -> sessions/<name>.md

After a feature ships (merged and stable): `/graduate o=<feature-dir> p=<prefix>` -> distills a durable `<p>-decision.md`, keeps your original draft, archives the process artifacts under `archive/`

To start a new project: `/bootstrap-spec-project` -> ~/ai-specs/<project>/

**Full orchestration** (automated pipeline):
```
/orchestrate i=<input> o=<output-dir> p=<prefix>
  -> asks which pipeline (Classic or Agile)
  -> chains all skills in sequence
  -> stops at approval gate (Classic: analysis-plan)
  -> runs the execution loop: retries failures (targeted) until Done or Blocked
  -> produces final summary
```

Codebase exploration (any time): `/conversation o=<output>` -> exploration.md + exploration-qa.md (read-only Q&A session; say "save html" to also get exploration.html)

Unattended tasks (while away): see [`sf-scheduler/`](sf-scheduler/README.md) - drop a task file in a watched folder, a headless agent picks it up and leaves results on disk.

Codebase health check (any time): `/improve-codebase-architecture` -> architecture-report.md

Standalone (not part of a pipeline): `/grilling` -> relentless one-at-a-time interview to stress-test a plan, decision, or idea; `/teach` -> stateful learning workspace (lessons, learning records, references) for a topic over multiple sessions

Coding standards (language-specific): `/coding-principles` (generic) or `/java-coding-standards`, `/go-coding-standards`, `/rust-coding-standards`, `/swift-coding-standards`, `/typescript-coding-standards`, `/python-coding-standards`, `/kotlin-coding-standards`

## Skills

| Skill | Input | Output | Stage |
|-------|-------|--------|-------|
| `grill-me` | idea or draft file | grilled-notes.md | Idea Exploration |
| `draft-discussion` | draft.md | discussion.md + discussion-qa.md | Clarification |
| `discussion-analysis` | discussion.md | analysis.md | Analysis |
| `analysis-plan` | analysis.md | plan.md | Planning (approval gate) |
| `to-prd` | grilled-notes or discussion | prd.md | Requirements |
| `plan-tasks` | plan.md | tasks/todo/*.md (one per task) | Decomposition |
| `to-issues` | prd.md | tasks/todo/*.md (vertical slices) | Decomposition |
| `task-execute` | one task file | code + task moved to tasks/done/ | Execution |
| `tdd` | one task file | code + tests, task moved to tasks/done/ | Execution (TDD) |
| `code-review` | one task file | review report (read-only) | Review |
| `task-verify` | one task file | pass/fail report (read-only) | Verification |
| `grilling` | plan, decision, or idea | shared understanding (interactive) | Interview (standalone) |
| `teach` | topic to learn | teaching workspace (lessons, records, references) | Learning (standalone) |
| `handoff` | session state | sessions/*.md | Continuity |
| `graduate` | shipped feature dir + prefix | decision.md + archive/ | Lifecycle (retire) |
| `project-principles` | project rules | overview/principles.md | Governance |
| `bootstrap-spec-project` | project/feature names | directory tree | Scaffolding |
| `improve-codebase-architecture` | current directory | architecture-report.md | Architecture |
| `orchestrate` | input file + output dir + prefix | full pipeline execution | Orchestration |
| `conversation` | optional existing conversation file | conversation.md + conversation-qa.md (+ conversation.html on request) | Exploration |
| `coding-principles` | any language | guidelines reference | Code Quality |
| `java-coding-standards` | Java code | guidelines reference | Code Quality |
| `go-coding-standards` | Go code | guidelines reference | Code Quality |
| `rust-coding-standards` | Rust code | guidelines reference | Code Quality |
| `swift-coding-standards` | Swift code | guidelines reference | Code Quality |
| `typescript-coding-standards` | TypeScript code | guidelines reference | Code Quality |
| `python-coding-standards` | Python code | guidelines reference | Code Quality |
| `kotlin-coding-standards` | Kotlin code | guidelines reference | Code Quality |

## Arguments

All skills use short argument names:

| Arg | Stands for | Used by |
|-----|-----------|---------|
| `i` | input / source file | grill-me, grilling (optional), draft-discussion, discussion-analysis, analysis-plan, plan-tasks, to-prd, to-issues, task-execute, tdd, code-review, task-verify, conversation (existing conversation to continue) |
| `o` | output file or directory | all writing skills (file; `plan-tasks` and `to-issues` write to a directory; `conversation` writes `<o>.md` and `<o>-qa.md`, plus `<o>.html` if asked; `grilling` optional) |
| `c` | codebase root (optional, brownfield) | grill-me, discussion-analysis, analysis-plan, to-prd, to-issues, tdd, code-review |
| `p` | prefix (artifact filenames + task IDs) / project name | plan-tasks (prefix), to-issues (prefix), orchestrate (prefix), bootstrap-spec-project (project) |
| `f` | feature name | bootstrap-spec-project |
| `n` | next-session purpose | handoff |

## Example invocations

Classic pipeline:
```
/draft-discussion i=inbox/idea.md o=features/auth/discussion.md

/discussion-analysis i=features/auth/discussion.md o=features/auth/analysis.md

/analysis-plan i=features/auth/analysis.md o=features/auth/plan.md

/plan-tasks i=features/auth/plan.md o=features/auth/tasks/todo/ p=auth

/task-execute i=features/auth/tasks/todo/auth-task-01.md

/code-review i=features/auth/tasks/done/auth-task-01.md

/task-verify i=features/auth/tasks/done/auth-task-01.md
```

Agile pipeline:
```
/grill-me i=inbox/idea.md o=features/auth/grilled-notes.md

/to-prd i=features/auth/grilled-notes.md o=features/auth/prd.md

/to-issues i=features/auth/prd.md o=features/auth/tasks/todo/ p=auth

/tdd i=features/auth/tasks/todo/auth-task-01.md

/code-review i=features/auth/tasks/done/auth-task-01.md
```

Conversation (explore and save):
```
/conversation o=features/auth/exploration

/conversation i=features/auth/exploration.md o=features/auth/exploration
```

Other:
```
/orchestrate i=inbox/idea.md o=features/auth/ p=auth

/handoff o=sessions/2026-05-23-auth.md n="Begin auth-task-02 implementation"

/project-principles o=overview/principles.md

/bootstrap-spec-project p=my-app f=user-auth

/improve-codebase-architecture
```

Brownfield (ground analysis/plan in an existing repo):

```
/discussion-analysis i=features/auth/discussion.md o=features/auth/analysis.md c=/path/to/repo

/analysis-plan i=features/auth/analysis.md o=features/auth/plan.md c=/path/to/repo

/to-prd i=features/auth/grilled-notes.md o=features/auth/prd.md c=/path/to/repo
```

## Install modes

**Personal** (`~/.claude/skills/`): skills available in all Claude Code sessions.

**Project** (`<project>/.claude/skills/`): skills available only within that project directory.

See `INSTALL.md` for exact commands.

## Compatibility

**Primary support: Claude Code and OpenCode**

These skills are designed for **Claude Code** and **OpenCode**. Both tools natively scan `~/.claude/skills/<name>/SKILL.md` and `.claude/skills/<name>/SKILL.md`, so installing once covers both. The skills use tool-specific features like automatic invocation (`/skill-name`) and argument parsing (`i=`, `o=`, `c=`).

**Other AI agents**

The core skill content (procedures, rules, templates) is written in standard Markdown and can be used with other AI coding agents (Cursor, Codex, Windsurf, Aider, etc.) by manually referencing the skill files. These tools don't have built-in skill systems, so you'll need to:

1. Include the skill files in your repo or reference them by path
2. Manually invoke them in prompts (e.g., "Read `skills/grill-me.md` and follow its procedure")
3. Provide context and arguments manually instead of using the `i=`, `o=` syntax

The skills will work, but without the automatic invocation and argument handling that Claude Code/OpenCode provide.

## Windows

**Use WSL or Git Bash**

The installation scripts (`install-personal.sh`, `install-project.sh`) and bootstrap script are bash-based and require a Unix-like environment. On Windows, use one of:

- **WSL (Windows Subsystem for Linux)** - Recommended. Full Linux environment.
- **Git Bash** - Lightweight alternative. Comes with Git for Windows.

Both provide full bash compatibility. The skill files themselves (Markdown) are cross-platform and work on any OS.

**Setup:**
1. Install WSL or Git Bash
2. Open WSL/Git Bash terminal
3. Run installation scripts as documented above
4. Use Claude Code/OpenCode within the same environment

Claude Code and OpenCode work best in Unix-like environments, so this approach provides the most reliable experience.

## Workflow guide

### Full orchestration

`/orchestrate` runs the entire pipeline from idea to verified tasks. It:
1. Asks which pipeline (Classic or Agile) and gathers inputs
2. Asks whether to enable code-review and task-verify (both optional, default: off)
3. Chains skills in sequence, passing outputs between them
4. Stops at the approval gate (Classic: `analysis-plan` review)
5. Executes tasks one by one, optionally running `code-review` after each
6. Retries failed tasks via the file-driven loop: `task-execute` reads the persisted `failed_checks` and fixes only those, until the task reaches `Done` or `Blocked` (`Max attempts`)
7. Optionally runs `task-verify` after each task
8. Produces a final summary with all artifacts and their paths

Use `/orchestrate` when you want to run the full pipeline without manually invoking each skill. You still control the process at approval gates and can stop at any time.

### Classic pipeline

1. Write a rough idea in `inbox/` or `features/<name>/inbox/` (no structure required). Unscoped ideas go in `backlog/`.
2. `/draft-discussion` - Claude asks 8-12 clarifying questions, then writes `discussion.md`. The questions and your verbatim answers are saved alongside in `discussion-qa.md`, written after each round.
3. `/discussion-analysis` - Claude reads discussion, separates facts from assumptions, writes `analysis.md`.
4. `/analysis-plan` - Claude sequences work, identifies dependencies, writes `plan.md`, then STOPS for your review and approval before `plan-tasks` runs.
5. `/plan-tasks` - Claude decomposes the approved plan into atomic tasks, writes one file per task into `tasks/todo/`.
6. `/task-execute` - Claude implements a single task, verifies its acceptance criteria, and moves the file from `tasks/todo/` to `tasks/done/`. Run once per task.
7. `/code-review` (optional) - Claude reviews the code changes for quality, security, performance, spec compliance, and test quality. Produces a report with findings by severity. Read-only.
8. `/task-verify` (optional) - read-only re-check of a task's Given/When/Then against the repo. Useful to audit done work.
9. `/handoff` at session end to write a resumable session document.

Optionally seed `overview/principles.md` first with `/project-principles`. When present, `discussion-analysis`, `analysis-plan`, and `task-execute` read it as binding constraints.

### Agile pipeline

1. `/grill-me` - Claude interrogates your idea with 8-15 grouped questions. Can explore the codebase to answer its own questions. Produces `grilled-notes.md` once all branches are resolved.
2. `/to-prd` - Claude converts grilled notes into a PRD with user stories and Given/When/Then acceptance criteria.
3. `/to-issues` - Claude breaks the PRD into vertical slices (tracer-bullet tasks), each delivering end-to-end user-visible value. Writes task files compatible with the rest of the pipeline.
4. `/tdd` - Claude implements one task using red-green-refactor: confirm interface, write one failing test, write minimum code, refactor, repeat. Moves task to `tasks/done/` when all criteria are covered by passing tests.
5. `/code-review` (optional) - Claude reviews the code changes for quality, security, performance, spec compliance, and test quality. Produces a report with findings by severity. Read-only.

### Implementation loop

Execution is a file-driven loop, not a one-shot. State lives on disk so it survives across sessions and tools:

- **Task state** - each task file carries `Status:` (`Draft | Approved | Revise | Done | Blocked`), `Attempts:`, and `Max attempts:`. The folder also signals state: `tasks/todo/` vs `tasks/done/`.
- **Feedback artifacts** - the executor (`task-execute` Classic / `tdd` Agile), `code-review`, and `task-verify` each write a report into `tasks/feedback/` per attempt (`<task-id>-attempt-NN.md`, `<task-id>-review-NN.md`, `<task-id>-verify-NN.md`). Highest `NN` is the latest. The reports carry YAML frontmatter with a `verdict` and a `failed_checks` list.
- **Targeted re-entry** - on a retry, `task-execute` reads the latest review/verify report and fixes only the `failed_checks`. Retries target named failures, they do not redo the whole task.
- **Loop exit** - the loop ends at `Status: Done` (all criteria pass) or `Status: Blocked` (`Attempts` reached `Max attempts`).

One pass through the loop:
```
Approved -> /task-execute            -> Attempts++, writes attempt-NN report
         -> /code-review             -> writes review-NN (verdict + failed_checks)
   PASS  -> Status: Done, todo/ -> done/
   FAIL  -> Status: Revise
         -> /task-execute (reads review-NN, fixes failed_checks only)
         -> ... repeat until Done or Blocked
```

Because every signal (status, attempts, verdicts, failed checks) is a file, a fresh session, OpenCode, or `/orchestrate` can resume the loop by reading the folder. Nothing important lives only in chat. `/orchestrate` drives this loop automatically; you can also run each step by hand for full control.

### Architecture review

`/improve-codebase-architecture` (no arguments) - runs in the current directory. Identifies shallow modules, scattered concepts, and tight coupling. Produces `architecture-report.md` with evidence-backed candidates and specific proposals. No code changes.

Stages before `task-execute` produce no code: each writes a reviewable file, and `analysis-plan` requires your explicit approval before the plan is decomposed into tasks. `task-execute` is the only skill that writes code, and only for one approved task at a time.

## Project structure (ai-specs)

After running `/bootstrap-spec-project p=my-app f=user-auth`:

```
~/ai-specs/my-app/
  README.md
  overview/                 <- project docs (architecture, decisions, context)
    principles.md           <- project-wide rules read by the pipeline (/project-principles)
  backlog/                  <- loose ideas not yet in the planning pipeline
  tasks/
    todo/                   <- tasks that need to be implemented
    done/
    feedback/               <- loop reports per attempt (execute/review/verify)
  features/
    user-auth/
      inbox/
      tasks/
        todo/               <- task files (user-auth-task-01.md, ...)
        done/
        feedback/           <- loop reports: *-attempt-NN.md, *-review-NN.md, *-verify-NN.md
      sessions/             <- feature level sessions
      <feat>-decision.md    <- durable decision record after /graduate (snapshot, not maintained)
      archive/              <- process artifacts moved here by /graduate (draft is kept in place)
  prompts/                  <- custom prompts you might need to use later
  sessions/                 <- app level sessions
```
