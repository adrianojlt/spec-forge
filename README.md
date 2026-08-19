# spec-forge

Skill pack for Claude Code and Opencode implementing a staged, file-driven planning workflow.

## Workflows

One pipeline, two optional entry points and a choice of executor:
```
[optional] /grill-me      -> grilled-notes.md (idea exploration + codebase grounding)
                             |
                             v
draft.md OR grilled-notes.md
  -> /draft-discussion    -> discussion.md (+ discussion-qa.md)
  -> /discussion-analysis -> analysis.md
  -> /analysis-plan       -> plan.md  (review + approve before next step)
  -> /plan-tasks          -> tasks/todo/<prefix>-task-01.md
                             tasks/todo/<prefix>-task-02.md
                             ...
  -> executor choice:
       /task-execute      -> implements one task, verifies, moves todo/ -> done/
       /tdd               -> code + tests (red-green-refactor loop, moves todo/ -> done/)
  -> /task-review         -> (optional) review report (quality, security, performance, spec, tests)
  -> /task-verify         -> (optional) read-only re-check of a task's acceptance criteria
```

Starting from grilled notes is a shortcut, not a different pipeline: `/draft-discussion` detects the grilled-notes format and asks only the themes grilling left unresolved.

Optional, before the pipeline: `/project-principles` -> overview/principles.md (project-wide rules the pipeline reads)

At session end: `/handoff` -> sessions/<name>.md

After a feature ships (merged and stable): `/graduate o=<feature-dir> p=<prefix>` -> distills a durable `<p>-decision.md`, keeps your original draft, archives the process artifacts under `archive/`

To start a new project: `/bootstrap-spec-project` -> ~/ai-specs/<project>/

**Unattended range** (many tasks, one command):
```
/execute-tasks i=<first task.md> to=<last task number> [r=yes] [v=yes] [c=<codebase>] [p=<commit prefix>]
  -> runs a contiguous range of task files, one at a time
  -> each task goes to a fresh subagent (no inherited context)
  -> commits each completed task with the task title as the message
  -> halts on the first blocked task
```

**Full orchestration** (automated pipeline):
```
/orchestrate i=<input> o=<output-dir> p=<prefix>
  -> asks which executor (task-execute or tdd)
  -> chains all skills in sequence
  -> stops at approval gate (analysis-plan)
  -> runs the execution loop: retries failures (targeted) until Done or Blocked
  -> produces final summary
```

Codebase exploration (any time): `/conversation o=<output>` -> exploration.md + exploration-qa.md (read-only Q&A session; say "save html" to also get exploration.html)

Unattended tasks (while away): see [`sf-scheduler/`](sf-scheduler/README.md) - drop a task file in a watched folder, a headless agent picks it up and leaves results on disk.

Codebase health check (any time): `/improve-codebase-architecture` -> architecture-report.md

Standalone (not part of a pipeline): `/grilling` -> relentless one-at-a-time interview to stress-test a plan, decision, or idea; `/teach` -> stateful learning workspace (lessons, learning records, references) for a topic over multiple sessions

Coding standards (language-specific): `/coding-principles` (generic) or `/java-coding-standards`, `/go-coding-standards`, `/rust-coding-standards`, `/swift-coding-standards`, `/typescript-coding-standards`, `/python-coding-standards`, `/kotlin-coding-standards`

Framework review (standalone): `/angular-clean-code` -> reviews Angular code for template side effects, change detection workarounds, state ownership, RxJS leaks, DI scope, and testability; `/react-clean-code` -> reviews React code for purity violations, state structure, hooks, and async handling

## Skills

| Skill | Input | Output | Stage |
|-------|-------|--------|-------|
| `grill-me` | idea or draft file | grilled-notes.md | Optional entry point (idea exploration) |
| `draft-discussion` | draft.md or grilled-notes.md | discussion.md + discussion-qa.md | Clarification |
| `discussion-analysis` | discussion.md | analysis.md | Analysis |
| `analysis-plan` | analysis.md | plan.md | Planning (approval gate) |
| `plan-tasks` | plan.md | tasks/todo/*.md (one per task, vertical slices) | Decomposition |
| `task-execute` | one task file | code + task moved to tasks/done/ | Execution |
| `tdd` | one task file | code + tests, task moved to tasks/done/ | Execution (test-first) |
| `task-review` | one task file | review report (read-only) | Review |
| `task-verify` | one task file | pass/fail report (read-only) | Verification |
| `execute-tasks` | first task file + last task number | a range of tasks executed and committed, one commit per task | Execution (unattended range) |
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
| `angular-clean-code` | Angular code | review findings + safe refactors | Code Quality |
| `react-clean-code` | React code | review findings + safe refactors | Code Quality |

## Arguments

All skills use short argument names:

| Arg | Stands for | Used by |
|-----|-----------|---------|
| `i` | input / source file | grill-me, grilling (optional), draft-discussion, discussion-analysis, analysis-plan, plan-tasks, task-execute, tdd, task-review, task-verify, execute-tasks (first task file of the range), conversation (existing conversation to continue) |
| `o` | output file or directory | all writing skills (file; `plan-tasks` writes to a directory; `conversation` writes `<o>.md` and `<o>-qa.md`, plus `<o>.html` if asked; `grilling` optional) |
| `c` | codebase root (optional, brownfield) | grill-me, discussion-analysis, analysis-plan, tdd, task-review, execute-tasks (forwarded to task-review) |
| `p` | prefix (artifact filenames + task IDs) / project name / commit prefix | plan-tasks (prefix), orchestrate (prefix), bootstrap-spec-project (project), execute-tasks (commit message prefix, optional) |
| `to` | last task number of a range (inclusive) | execute-tasks |
| `r` | run task-review after each task (`r=yes`, default off) | execute-tasks |
| `v` | run task-verify after each task (`v=yes`, default off) | execute-tasks |
| `f` | feature name | bootstrap-spec-project |
| `n` | question count (draft-discussion, `n=<min>-<max>`) / next-session purpose (handoff) | draft-discussion, handoff |

## Example invocations

Pipeline:
```
/draft-discussion i=inbox/idea.md o=features/auth/discussion.md

/discussion-analysis i=features/auth/discussion.md o=features/auth/analysis.md

/analysis-plan i=features/auth/analysis.md o=features/auth/plan.md

/plan-tasks i=features/auth/plan.md o=features/auth/tasks/todo/ p=auth

/task-execute i=features/auth/tasks/todo/auth-task-01.md

/task-review i=features/auth/tasks/done/auth-task-01.md

/task-verify i=features/auth/tasks/done/auth-task-01.md
```

Unattended range (tasks 01 through 05, each committed with an `[auth]` prefix):
```
/execute-tasks i=features/auth/tasks/todo/auth-task-01.md to=5 p=[auth]

/execute-tasks i=features/auth/tasks/todo/auth-task-01.md to=5 r=yes v=yes c=/path/to/repo p=auth:
```

Optional grill-me pre-stage (grilled notes replace the draft as input, and the
second pass needs fewer questions because grilling already resolved most themes):
```
/grill-me i=inbox/idea.md o=features/auth/grilled-notes.md

/draft-discussion i=features/auth/grilled-notes.md o=features/auth/discussion.md n=3-5
```

Test-first executor instead of `/task-execute`:
```
/tdd i=features/auth/tasks/todo/auth-task-01.md
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

/grill-me i=inbox/idea.md o=features/auth/grilled-notes.md c=/path/to/repo
```

## Install modes

**Personal** (`~/.claude/skills/`): skills available in all Claude Code sessions.

**Project** (`<project>/.claude/skills/`): skills available only within that project directory.

**Global rules** (`~/.claude/CLAUDE.md` + `~/.config/opencode/AGENTS.md`): the repo's `CLAUDE.md` copied as a managed block, via `install-rules.sh` / `install-rules.ps1`.

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

Skills must land in the home directory of the environment where Claude Code actually runs. Windows has two separate home directories, and mixing them is the usual failure:

| Environment | Home | Skills path |
|-------------|------|-------------|
| Windows (PowerShell / CMD) | `C:\Users\<you>` | `C:\Users\<you>\.claude\skills` |
| WSL | `/home/<you>` | `/home/<you>/.claude/skills` |

If you run Claude Code from PowerShell but install from WSL, the skills go to the WSL home and Claude Code never sees them.

**Recommended: PowerShell install**

Use the native PowerShell script. No bash, no WSL:

```powershell
powershell -ExecutionPolicy Bypass -File .\install-skills.ps1
```

Verify:

```powershell
dir $env:USERPROFILE\.claude\skills
```

**Alternative: Git Bash**

Git Bash ships with Git for Windows and its `$HOME` is `C:\Users\<you>`, so the bash script installs to the right place:

```bash
./install-skills.sh
```

**Alternative: WSL, installing into the Windows home**

If you only have the bash script and you are in WSL but run Claude Code on Windows, override `HOME` so the files land in the Windows profile:

```bash
HOME=/mnt/c/Users/<YourWindowsUser> ./install-skills.sh
```

Running `./install-skills.sh` plainly inside WSL is correct only when you also run Claude Code inside WSL.

**Project install**

`install-project.sh` has no PowerShell equivalent. Use Git Bash or WSL for it, or copy manually:

```powershell
$dest = "C:\path\to\project\.claude\skills"
New-Item -ItemType Directory -Force -Path $dest | Out-Null
Copy-Item -Path .\skills\* -Destination $dest -Recurse -Force
```

The skill files themselves (Markdown) are cross-platform and work on any OS.

## Workflow guide

### Full orchestration

`/orchestrate` runs the entire pipeline from idea to verified tasks. It:
1. Asks which executor (`task-execute` or `tdd`) and gathers inputs (draft or grilled notes)
2. Asks whether to enable task-review and task-verify (both optional, default: off)
3. Chains skills in sequence, passing outputs between them
4. Stops at the approval gate (`analysis-plan` review)
5. Executes tasks one by one with the chosen executor, optionally running `task-review` after each
6. Retries failed tasks via the file-driven loop: `task-execute` reads the persisted `failed_checks` and fixes only those, until the task reaches `Done` or `Blocked` (`Max attempts`)
7. Optionally runs `task-verify` after each task
8. Produces a final summary with all artifacts and their paths

Use `/orchestrate` when you want to run the full pipeline without manually invoking each skill. You still control the process at approval gates and can stop at any time.

### The pipeline

0. `/grill-me` (optional entry point) - Claude interrogates your idea with 8-15 grouped questions. Can explore the codebase to answer its own questions. Produces `grilled-notes.md` once all branches are resolved. Feed that file to `/draft-discussion` instead of a raw draft.
1. Write a rough idea in `inbox/` or `features/<name>/inbox/` (no structure required). Unscoped ideas go in `backlog/`.
2. `/draft-discussion` - Claude asks 8-12 clarifying questions, then writes `discussion.md`. The questions and your verbatim answers are saved alongside in `discussion-qa.md`, written after each round. Given grilled notes as input, it skips the themes already resolved and asks only the gaps (pass `n=3-5`).
3. `/discussion-analysis` - Claude reads discussion, separates facts from assumptions, writes `analysis.md`.
4. `/analysis-plan` - Claude sequences work, identifies dependencies, writes `plan.md`, then STOPS for your review and approval before `plan-tasks` runs.
5. `/plan-tasks` - Claude decomposes the approved plan into atomic tasks, writes one file per task into `tasks/todo/`. Tasks are vertical slices: no layer-only tasks, each one delivers observable user-visible value.
6. Executor, one per task, pick one:
   - `/task-execute` - Claude implements a single task, verifies its acceptance criteria, and moves the file from `tasks/todo/` to `tasks/done/`.
   - `/tdd` - Claude implements one task using red-green-refactor: state the interface, write one failing test, write minimum code, refactor, repeat. Moves the task to `tasks/done/` when all criteria are covered by passing tests.
7. `/task-review` (optional) - Claude reviews the code changes for quality, security, performance, spec compliance, and test quality. Produces a report with findings by severity. Read-only.
8. `/task-verify` (optional) - read-only re-check of a task's Given/When/Then against the repo. Useful to audit done work.
9. `/handoff` at session end to write a resumable session document.

Optionally seed `overview/principles.md` first with `/project-principles`. When present, `discussion-analysis`, `analysis-plan`, and `task-execute` read it as binding constraints.

### Implementation loop

Execution is a file-driven loop, not a one-shot. State lives on disk so it survives across sessions and tools:

- **Task state** - each task file carries `Status:` (`Draft | Approved | Revise | Done | Blocked`), `Attempts:`, and `Max attempts:`. The folder also signals state: `tasks/todo/` vs `tasks/done/`.
- **Feedback artifacts** - the executor (`task-execute` or `tdd`), `task-review`, and `task-verify` each write a report into `tasks/feedback/` per attempt (`<task-id>-attempt-NN.md`, `<task-id>-review-NN.md`, `<task-id>-verify-NN.md`). Highest `NN` is the latest. The reports carry YAML frontmatter with a `verdict` and a `failed_checks` list.
- **Targeted re-entry** - on a retry, `task-execute` reads the latest review/verify report and fixes only the `failed_checks`. Retries target named failures, they do not redo the whole task.
- **Loop exit** - the loop ends at `Status: Done` (all criteria pass) or `Status: Blocked` (`Attempts` reached `Max attempts`).

One pass through the loop:
```
Approved -> /task-execute or /tdd    -> Attempts++, writes attempt-NN report
         -> /task-review             -> writes review-NN (verdict + failed_checks)
   PASS  -> Status: Done, todo/ -> done/
   FAIL  -> Status: Revise
         -> executor again (reads review-NN, fixes failed_checks only)
         -> ... repeat until Done or Blocked
```

Because every signal (status, attempts, verdicts, failed checks) is a file, a fresh session, OpenCode, or `/orchestrate` can resume the loop by reading the folder. Nothing important lives only in chat. `/orchestrate` drives this loop automatically; you can also run each step by hand for full control.

### Unattended task ranges

`/execute-tasks` runs a contiguous range of task files end to end, with nobody watching. It orchestrates only: it writes no code and edits no task file, `task-execute` still does the implementation and still owns every status change.

```
/execute-tasks i=features/auth/tasks/todo/auth-task-01.md to=5 p=[auth]
```

What it adds on top of `task-execute`:

- **Range** - walks task numbers ascending, from the number parsed out of `i` through `to` inclusive. `to` is a task number, not a count. Missing numbers are skipped, and tasks already in `tasks/done/` are skipped, so re-invoking the same range after a halt resumes where it stopped.
- **Isolation** - every task, and every retry attempt, gets a fresh subagent. Task five is never executed inside the accumulated context of tasks one through four.
- **Commits** - each task that reaches `Status: Done` in `tasks/done/` gets exactly one local commit, its message taken from the task file's H1 with the bracketed task ID stripped. Never pushes, never branches, never opens a pull request.
- **Stopping conditions** - a blocked task, or one that exhausts `Max attempts`, halts the whole run at that task and leaves the working tree untouched so you can see what the failed attempt produced.

Preflight refuses the run if the range is inverted, the layout is wrong, git identity is unset, or the working tree is dirty. The clean-tree check matters because each task commit runs `git add -A`.

Arguments:

| Arg | Meaning |
|-----|---------|
| `i` | first task file of the range, in `tasks/todo/` |
| `to` | last task number of the range, inclusive |
| `r` | `r=yes` runs `task-review` after each task (default off) |
| `v` | `v=yes` runs `task-verify` after each task (default off) |
| `c` | codebase root, forwarded to `task-review` |
| `p` | commit prefix (optional) |

**The `p` commit prefix.** Without `p`, commit messages are the task title alone, and the commits of a feature are indistinguishable from anything else in the log. With `p`, the value is prepended verbatim plus a single space to every commit the run creates, so the whole feature can be spotted, filtered, or unwound as a unit:

```
/execute-tasks i=features/auth/tasks/todo/auth-task-01.md to=5 p=[auth]

[auth] Add token expiry check
[auth] Reject expired refresh tokens
[auth] Add logout endpoint
```

The prefix format is yours: the skill adds no brackets, colon, or separator of its own, so `p=[auth]`, `p=auth:`, and `p=feat(auth):` all work as typed. The prefix touches commit messages only, never the task files or the task IDs.

### Architecture review

`/improve-codebase-architecture` (no arguments) - runs in the current directory. Identifies shallow modules, scattered concepts, and tight coupling. Produces `architecture-report.md` with evidence-backed candidates and specific proposals. No code changes.

Stages before the executor produce no code: each writes a reviewable file, and `analysis-plan` requires your explicit approval before the plan is decomposed into tasks. The executor (`task-execute` or `tdd`) is the only stage that writes code, and only for one approved task at a time.

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
