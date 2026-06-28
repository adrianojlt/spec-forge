# Project Structure Template

Standard ai-specs layout created by bootstrap-spec-project.

```
~/ai-specs/<project_name>/
  README.md                       <- project purpose and folder guide
  overview/                       <- project documentation (architecture, decisions, context)
    .gitkeep
  backlog/                        <- loose ideas not yet in planning pipeline
    .gitkeep
  tasks/
    todo/                         <- simple tasks not tied to any feature
      .gitkeep
    done/                         <- completed simple tasks
      .gitkeep
    feedback/                     <- loop reports (attempt/review/verify) per task
      .gitkeep
  features/
    <feature_name>/
      inbox/                      <- rough drafts (input to /draft-discussion)
        .gitkeep
      tasks/
        todo/                     <- individual task files ready to work
          .gitkeep
        done/                     <- completed task files
          .gitkeep
        feedback/                 <- loop reports (attempt/review/verify) per task
          .gitkeep
      sessions/                   <- feature-level session handoffs
        .gitkeep
  prompts/                        <- reusable prompt snippets for this project
    .gitkeep
  sessions/                       <- project-level session handoffs
    .gitkeep
```

## Folder purposes

| Path | Purpose |
|------|---------|
| `overview/` | Project documentation: architecture, decisions, context, ADRs. |
| `backlog/` | Loose ideas and potential features not yet in the planning pipeline. |
| `tasks/todo/` | Simple tasks not tied to a feature - no full pipeline needed. |
| `tasks/done/` | Completed simple tasks. |
| `tasks/feedback/` | Per-attempt loop reports (execute/review/verify) with verdicts and failed checks. |
| `features/<name>/inbox/` | Raw drafts and ideas. Input to `/draft-discussion`. |
| `features/<name>/tasks/todo/` | Individual task files from `/plan-tasks`, ready to work. |
| `features/<name>/tasks/done/` | Completed task files (moved from todo when done). |
| `features/<name>/tasks/feedback/` | Per-attempt loop reports driving targeted retries. |
| `features/<name>/sessions/` | Feature-level session handoff documents. |
| `prompts/` | Reusable prompt snippets for this project. |
| `sessions/` | Project-level session handoff documents. |

## Workflow entry point

1. Write idea in `features/<name>/inbox/idea.md`
2. `/draft-discussion i=features/<name>/inbox/idea.md o=features/<name>/discussion.md`
3. `/discussion-analysis i=features/<name>/discussion.md o=features/<name>/analysis.md`
4. `/analysis-plan i=features/<name>/analysis.md o=features/<name>/plan.md`
5. `/plan-tasks i=features/<name>/plan.md o=features/<name>/tasks/todo/ p=<name>`
6. Work tasks. Move individual files from `tasks/todo/` to `tasks/done/` when complete.
7. `/handoff o=sessions/<date>-<topic>.md n="..."`
