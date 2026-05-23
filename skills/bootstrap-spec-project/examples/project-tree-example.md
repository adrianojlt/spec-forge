# Example: Project Tree After bootstrap-spec-project

Command run:
```
/bootstrap-spec-project project_name=my-app feature_name=user-auth
```

Result:
```
~/ai-specs/my-app/
  README.md
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

## Next steps after bootstrap

1. Write a rough idea in `~/ai-specs/my-app/features/user-auth/inbox/idea.md`
2. Run `/draft-discussion` (paths shown in script output above)
3. Review `discussion.md` before proceeding to analysis
4. Follow the pipeline: discussion -> analysis -> plan -> BACKLOG
