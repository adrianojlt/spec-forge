#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
    echo "Error: two arguments required"
    echo "Usage: $0 <project_name> <feature_name>"
    exit 1
fi

PROJECT_NAME="$1"
FEATURE_NAME="$2"

if [[ -z "$PROJECT_NAME" || -z "$FEATURE_NAME" ]]; then
    echo "Error: project_name and feature_name must be non-empty"
    exit 1
fi

BASE_DIR="$HOME/ai-specs"
PROJECT_DIR="$BASE_DIR/$PROJECT_NAME"
FEATURE_DIR="$PROJECT_DIR/features/$FEATURE_NAME"

echo "Bootstrapping: $PROJECT_DIR"
echo ""

dirs=(
    "$FEATURE_DIR/inbox"
    "$FEATURE_DIR/tasks/todo"
    "$FEATURE_DIR/tasks/done"
    "$FEATURE_DIR/sessions"
    "$PROJECT_DIR/overview"
    "$PROJECT_DIR/backlog"
    "$PROJECT_DIR/tasks/todo"
    "$PROJECT_DIR/tasks/done"
    "$PROJECT_DIR/prompts"
    "$PROJECT_DIR/sessions"
)

for dir in "${dirs[@]}"; do
    mkdir -p "$dir"
    if [[ ! -f "$dir/.gitkeep" ]]; then
        touch "$dir/.gitkeep"
    fi
    echo "  [ok] $dir"
done

PRINCIPLES="$PROJECT_DIR/overview/principles.md"
if [[ ! -f "$PRINCIPLES" ]]; then
    cat > "$PRINCIPLES" <<EOF
# Principles: $PROJECT_NAME

Status: Draft

---

> Binding, project-wide rules. Read by discussion-analysis, analysis-plan, and
> task-execute. Keep short. One line per rule. Run /project-principles to fill in.

## Principles

-

## Constraints

-

## Conventions

-

## Decision Defaults

-

## Non-Negotiables

-
EOF
    echo "  [ok] $PRINCIPLES"
fi

README="$PROJECT_DIR/README.md"
if [[ ! -f "$README" ]]; then
    cat > "$README" <<EOF
# $PROJECT_NAME

AI-specs project managed with Claude Code skills.

## Structure

\`\`\`
$PROJECT_NAME/
  overview/         <- project documentation (architecture, decisions, context)
  backlog/          <- loose ideas not yet in the planning pipeline
  tasks/
    todo/           <- simple tasks not tied to a feature
    done/           <- completed simple tasks
  features/
    <feature>/
      inbox/        <- rough drafts (input to /draft-discussion)
      tasks/
        todo/       <- task files ready to work
        done/       <- completed task files
      sessions/     <- feature-level handoffs
  prompts/          <- reusable prompt snippets
  sessions/         <- project-level handoffs
\`\`\`

## Workflow

1. Write idea in \`features/<name>/inbox/idea.md\`
2. \`/draft-discussion i=features/<name>/inbox/idea.md o=features/<name>/discussion.md\`  (also writes discussion-qa.md)
3. \`/discussion-analysis i=features/<name>/discussion.md o=features/<name>/analysis.md\`
4. \`/analysis-plan i=features/<name>/analysis.md o=features/<name>/plan.md\`  (review + approve before step 5)
5. \`/plan-tasks i=features/<name>/plan.md o=features/<name>/tasks/todo/ p=<name>\`
6. \`/task-execute i=features/<name>/tasks/todo/<name>-task-01.md\`  (implements, verifies, moves todo->done)
7. \`/task-verify i=features/<name>/tasks/done/<name>-task-01.md\`  (optional read-only re-check)
8. \`/handoff o=sessions/<date>.md n="..."\`

Optional: \`/project-principles o=overview/principles.md\` to set project-wide rules the pipeline reads.
EOF
    echo "  [ok] $README"
fi

echo ""
echo "Done."
echo "  Project: $PROJECT_DIR"
echo "  Feature: $FEATURE_DIR"
echo ""
echo "Start with:"
echo "  Write idea to: $FEATURE_DIR/inbox/idea.md"
echo "  Then run: /draft-discussion i=$FEATURE_DIR/inbox/idea.md o=$FEATURE_DIR/discussion.md"
