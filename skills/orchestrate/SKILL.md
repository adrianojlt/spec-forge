---
name: orchestrate
description: "Run the full SDD pipeline end-to-end. Semi-autonomous orchestrator that chains skills, handles approval gates, and retries on review failures."
argument-hint: "[i=<input-file>] [o=<output-dir>] [p=<prefix>]"
disable-model-invocation: true
---

# orchestrate

## Purpose
Run the complete Spec-Driven Development pipeline from idea to verified tasks. Semi-autonomous: runs skills in sequence, stops at human approval gates, retries failed tasks via the file-driven loop until each reaches `Done` or `Blocked` (the task file's `Max attempts`).

This skill does not produce code itself. It instructs you to read and follow other skills' SKILL.md files in the correct order, passing outputs between them, and managing the flow.

## Inputs
- `$i` - input file (optional; if not provided, ask the user)
- `$o` - output directory for feature artifacts (optional; if not provided, ask the user)
- `$p` - prefix for all generated artifact filenames (optional; if not provided, ask the user)

## Hard rules
- Do not skip the approval gate at `analysis-plan` (Classic pipeline). This is the only mandatory human stop.
- Do not auto-advance past a task that reached `Status: Blocked` (`Max attempts` exhausted). Stop and report.
- Do not run tasks in parallel. Execute them sequentially in dependency order.
- Do not modify task files directly. Let `task-execute` and `tdd` handle that.
- Do not invent requirements or make design decisions. Defer to the user at gates.
- If any skill fails or errors, stop and report. Do not attempt to recover silently.

## Procedure

### Step 1 - Gather context
Ask the user:
1. **Which pipeline?** Classic (draft -> discussion -> analysis -> plan -> tasks) or Agile (idea -> grill -> PRD -> issues)?
2. **Input file?** If `$i` is provided, use it. Otherwise ask for the path to the draft or idea file.
3. **Output directory?** If `$o` is provided, use it. Otherwise ask where to write artifacts (e.g. `features/auth/`).
4. **Prefix?** If `$p` is provided, use it. Otherwise ask for a short prefix used for all generated filenames and task IDs (e.g. `auth` produces `auth-discussion.md`, `auth-analysis.md`, `auth-task-01`, etc.).
5. **Run code-review after each task?** (yes/no, default: no)
6. **Run task-verify after each task?** (yes/no, default: no)

If the user has already provided these via arguments or context, skip the questions.

### Step 2 - Run entry skill
**Classic pipeline:**
Read and follow `draft-discussion/SKILL.md` with args: `i=<input> o=<output>/<p>-discussion.md`

Wait for the user to answer all clarification rounds. The skill will produce `<p>-discussion.md` and `<p>-discussion-qa.md`.

**Agile pipeline:**
Read and follow `grill-me/SKILL.md` with args: `i=<input> o=<output>/<p>-grilled-notes.md`

Wait for the user to answer all question rounds. The skill will produce `<p>-grilled-notes.md`.

### Step 3 - Run analysis/requirements skill
**Classic pipeline:**
Read and follow `discussion-analysis/SKILL.md` with args: `i=<output>/<p>-discussion.md o=<output>/<p>-analysis.md`

If the user provided a codebase root (`$c`), pass it through.

**Agile pipeline:**
Read and follow `to-prd/SKILL.md` with args: `i=<output>/<p>-grilled-notes.md o=<output>/<p>-prd.md`

If the user provided a codebase root (`$c`), pass it through.

### Step 4 - Run planning skill (Classic only)
**Classic pipeline:**
Read and follow `analysis-plan/SKILL.md` with args: `i=<output>/<p>-analysis.md o=<output>/<p>-plan.md`

**STOP HERE. This is the approval gate.**

Present the plan summary to the user (slice sequence, tradeoffs, risks, open questions). Ask:
1. Approve the plan as-is
2. Request edits (apply them, then re-present)
3. Edit the plan themselves and tell you when done

Do not proceed until the user explicitly approves.

**Agile pipeline:**
Skip this step. The PRD is the planning artifact.

### Step 5 - Run decomposition skill
**Classic pipeline:**
Read and follow `plan-tasks/SKILL.md` with args: `i=<output>/<p>-plan.md o=<output>/tasks/todo/ p=<p>`

The skill produces one task file per task in `tasks/todo/`.

**Agile pipeline:**
Read and follow `to-issues/SKILL.md` with args: `i=<output>/<p>-prd.md o=<output>/tasks/todo/ p=<p>`

The skill produces one task file per vertical slice in `tasks/todo/`.

After decomposition, report the task count and list task IDs. Ask the user to confirm before proceeding to execution.

### Step 6 - Execute tasks (loop)
For each task file in `tasks/todo/` (in dependency order):

**6a - Execute (loop on the task's own self-check)**
**Classic pipeline:**
Read and follow `task-execute/SKILL.md` with args: `i=<task-file>`

**Agile pipeline:**
Read and follow `tdd/SKILL.md` with args: `i=<task-file>`

Wait for the skill to complete. If it stops due to unmet dependencies, report and ask the user how to proceed.

After it completes, read the task file's `Status:`. The executor self-checks its own acceptance criteria, so this loop runs even when code-review and task-verify are both disabled:
- **`Done`**: proceed to 6b.
- **`Revise`** (self-check failed, `Attempts` still `< Max attempts`): re-read and follow `task-execute/SKILL.md` (or `tdd/SKILL.md`) again. Its Step 1 reads the latest `tasks/feedback/<task-id>-attempt-<NN>.md` and fixes only the `failed_checks`. Repeat until `Done` or `Blocked`.
- **`Blocked`** (`Attempts` reached `Max attempts`): stop on this task and report. Do not auto-advance. Ask the user how to proceed.

Only proceed to 6b once the task is `Done`. Code-review and task-verify are *additional* gates layered on top of this loop, not the thing that triggers it.

**6b - Review (if enabled)**
If the user chose to run code-review:
  Read and follow `code-review/SKILL.md` with args: `i=<task-file>`

  Check the verdict:
  - **PASS** or **PASS WITH WARNINGS**: proceed to 6c
  - **FAIL**: proceed to 6b-retry

  **6b-retry - Retry on failure (state-driven)**
  Retries are driven by the task file's `Attempts` / `Max attempts` and the persisted feedback files, not by a counter held in chat. If the review verdict is FAIL:
  1. Report the blocker findings to the user.
  2. Re-read and follow `task-execute/SKILL.md` (or `tdd/SKILL.md`). It reads the latest `tasks/feedback/<task-id>-review-<NN>.md` in its Step 1 and fixes only the `failed_checks` (targeted re-entry, not a blind redo).
  3. Re-read and follow `code-review/SKILL.md` with args: `i=<task-file>`.
  4. The loop ends when the task reaches `Status: Done` (pass) or `Status: Blocked` (`Attempts` reached `Max attempts`). On `Blocked`, stop and report. Do not auto-advance. Because state lives in the task file and `tasks/feedback/`, the loop resumes correctly even in a fresh session.

If code-review is disabled, skip directly to 6c.

**6c - Verify (if enabled)**
If the user chose to run task-verify:
  Read and follow `task-verify/SKILL.md` with args: `i=<task-file>`

  Check the verdict:
  - **All pass**: task is done, proceed to next task
  - **Failures**: report to the user. Ask whether to re-execute or skip.

If task-verify is disabled, the task is considered done after execution (and review if enabled). Proceed to next task.

After each task completes (or is skipped), report progress: "Task X of Y complete. Next: <task-id>."

### Step 7 - Handoff (optional)
After all tasks are processed, ask the user:
- "All tasks complete. Would you like to generate a handoff document for the next session?"

If yes:
Read and follow `handoff/SKILL.md` with args: `o=<output>/sessions/<date>-<p>.md n="<next-session-purpose>"`

Ask the user for the next session purpose if not obvious.

### Step 8 - Final report
Present a summary:
- Pipeline used
- Artifacts produced (with paths)
- Tasks completed / failed / skipped
- Code review verdicts (if enabled; otherwise note "code-review was disabled")
- Task verification results (if enabled; otherwise note "task-verify was disabled")
- Any unresolved issues or deferred work

### Step 9 - Graduate (optional, default no)
After the final report, offer to graduate the feature, but **default to no**. A feature is rarely shippable the instant the build loop ends (it still needs merge / release / stabilization), and graduating archives the plan and task files. Ask:
- "The build loop is done. Graduate this feature now? This distills a durable `<p>-decision.md`, keeps your original draft, and archives the process artifacts. Most users do this later, once the feature is merged and stable - run `/graduate o=<output> p=<p>` whenever you stop touching it. Graduate now? (default: no)"

Only if the user explicitly says yes:
Read and follow `graduate/SKILL.md` with args: `o=<output> p=<p>`

Do not graduate as part of the normal pipeline flow. It is a separate, user-triggered lifecycle step.

## State tracking
Source of truth for task state is on disk, not chat: each task file's `Status:` / `Attempts:` and the reports in `tasks/feedback/`. Throughout the orchestration, track:
- Current pipeline stage (entry, analysis, planning, decomposition, execution, handoff)
- Task progress, read from each task's `Status:` (Approved, Revise, Done, Blocked)
- Retry state, read from each task's `Attempts:` vs `Max attempts:`
- User decisions at gates (approved plan, skipped tasks, etc.)

Report state transitions clearly: "Moving from planning to decomposition..." or "Task 3 of 5: auth-task-03..."

## Failure modes
- **Skill errors**: If following a skill's procedure produces an error or fails, stop and report the error. Do not attempt to continue.
- **User cancels**: If the user says "stop" or "cancel", stop immediately. Report what was completed and what remains.
- **Dependency unmet**: If a task's dependencies are not in `tasks/done/`, skip it and report. Ask the user whether to continue with remaining tasks.
- **Max retries exceeded**: After 2 failed review retries, stop on that task. Report the blockers. Ask the user whether to skip or fix manually.

## Output contract
No direct output files. The orchestrator produces:
- All artifacts from the chained skills (discussion.md, analysis.md, plan.md, task files, etc.)
- A final summary report (in chat)
- Optional handoff document

## Validation
Before reporting completion, verify:
- All task files are either in `tasks/done/` or explicitly marked as skipped/failed
- If code-review was enabled: no task has an unresolved FAIL verdict
- The approval gate was respected (Classic pipeline only)
- The final summary includes all artifacts and their paths
