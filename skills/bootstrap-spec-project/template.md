# Project Structure Template

Standard ai-specs layout created by bootstrap-spec-project.

```
~/ai-specs/<project_name>/
  README.md                       <- project purpose and folder guide
  features/
    <feature_name>/
      inbox/                      <- rough drafts (input to /draft-discussion)
        .gitkeep
      tasks/
        todo/                     <- tasks from BACKLOG ready to start
          .gitkeep
        done/                     <- completed tasks
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
| `features/<name>/inbox/` | Raw drafts and ideas. Input to `/draft-discussion`. |
| `features/<name>/tasks/todo/` | Tasks from BACKLOG that are ready to work. |
| `features/<name>/tasks/done/` | Completed and merged tasks. |
| `features/<name>/sessions/` | Feature-level session handoff documents. |
| `prompts/` | Reusable prompt snippets for this project. |
| `sessions/` | Project-level session handoff documents. |

## Workflow entry point

1. Write idea in `features/<name>/inbox/idea.md`
2. `/draft-discussion source_file=features/<name>/inbox/idea.md target_file=features/<name>/discussion.md`
3. `/discussion-analysis source_file=features/<name>/discussion.md target_file=features/<name>/analysis.md`
4. `/analysis-plan source_file=features/<name>/analysis.md target_file=features/<name>/plan.md`
5. `/plan-tasks source_file=features/<name>/plan.md target_file=features/<name>/BACKLOG.md`
6. Work tasks. Move files from `tasks/todo/` to `tasks/done/` when complete.
7. `/handoff target_file=sessions/<date>-<topic>.md next_purpose="..."`
