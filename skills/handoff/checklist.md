# handoff validation checklist

Run before writing output. Fail any item = revise.

## Content checks

- [ ] No secrets, tokens, passwords, or credentials appear in output
- [ ] No large block of content copied verbatim from an existing artifact
- [ ] All referenced files are listed with their actual paths
- [ ] Paths are correct (not invented or approximate)
- [ ] Next recommended action is a single concrete step, not a list

## Scope checks

- [ ] Handoff is tailored to $next_purpose (not generic)
- [ ] Open questions are relevant to the next session (not all historical questions)
- [ ] Decisions listed are decisions (not observations or descriptions)

## Length check

- [ ] Total document is under 500 words
- [ ] No section contains prose longer than 5 sentences

## Hard stops

- Output blocked if: secrets or credentials are present
- Output blocked if: next session focus is vague ("continue work")
- Output blocked if: file paths are approximate ("somewhere in features/")
