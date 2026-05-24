# Example: Project Tree After bootstrap-spec-project

Command run:
```
/bootstrap-spec-project project_name=my-app feature_name=user-auth
```

Result:
```
~/ai-specs/my-app/
  README.md
  overview/
    .gitkeep
  backlog/
    .gitkeep
  tasks/
    todo/
      .gitkeep
    done/
      .gitkeep
  features/
    user-auth/
      inbox/
        .gitkeep
      tasks/
        todo/
          .gitkeep
        done/
          .gitkeep
      sessions/
        .gitkeep
  prompts/
    .gitkeep
  sessions/
    .gitkeep
```

## Script output

```
Bootstrapping: /Users/adriano/ai-specs/my-app

  [ok] /Users/adriano/ai-specs/my-app/features/user-auth/inbox
  [ok] /Users/adriano/ai-specs/my-app/features/user-auth/tasks/todo
  [ok] /Users/adriano/ai-specs/my-app/features/user-auth/tasks/done
  [ok] /Users/adriano/ai-specs/my-app/features/user-auth/sessions
  [ok] /Users/adriano/ai-specs/my-app/overview
  [ok] /Users/adriano/ai-specs/my-app/backlog
  [ok] /Users/adriano/ai-specs/my-app/tasks/todo
  [ok] /Users/adriano/ai-specs/my-app/tasks/done
  [ok] /Users/adriano/ai-specs/my-app/prompts
  [ok] /Users/adriano/ai-specs/my-app/sessions
  [ok] /Users/adriano/ai-specs/my-app/README.md

Done.
  Project: /Users/adriano/ai-specs/my-app
  Feature: /Users/adriano/ai-specs/my-app/features/user-auth

Start with:
  Write idea to: /Users/adriano/ai-specs/my-app/features/user-auth/inbox/idea.md
  Then run: /draft-discussion source_file=/Users/adriano/ai-specs/my-app/features/user-auth/inbox/idea.md target_file=/Users/adriano/ai-specs/my-app/features/user-auth/discussion.md
```

## Folder guide

| Path | Use for |
|------|---------|
| `overview/` | Architecture docs, decision records, project context |
| `backlog/` | Unscoped ideas not yet ready for planning |
| `tasks/todo/` | Simple tasks - no feature pipeline needed |
| `tasks/done/` | Completed simple tasks |
| `features/<name>/inbox/` | Draft ideas entering the planning pipeline |
| `features/<name>/tasks/todo/` | Task files from `/plan-tasks` |
| `features/<name>/tasks/done/` | Completed feature tasks |

## After plan-tasks runs

```
~/ai-specs/my-app/features/user-auth/tasks/todo/
  user-auth-task-01.md
  user-auth-task-02.md
  user-auth-task-03.md
  ...
```

Move to done when complete:
```bash
mv features/user-auth/tasks/todo/user-auth-task-01.md features/user-auth/tasks/done/
```
