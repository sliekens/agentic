# Decision Tables

## What it is

A decision table maps every meaningful combination of conditions (inputs, states, flags) to a specific outcome (action, result, behavior). Each column is one rule (scenario); each row is a condition or action.

Decision tables are the right tool when behavior is governed by **combinations of independent yes/no conditions** and you want to ensure every combination is specified — and none are missing or contradictory.

## When to use

- Authorization logic ("if role is admin AND resource is active AND user owns it...")
- Validation rules with multiple interacting constraints
- Business rules expressed as conditional chains
- Any place where you'd naturally write a truth table

## How to apply

### Step 1 — List all conditions

Identify every independent boolean condition that affects the outcome. Keep them binary (Y/N) where possible. If a condition has more than two values (e.g., role = admin/user/guest), either split it into two binary conditions or include all values as distinct columns.

Aim for 4–6 conditions. More than 6 creates 2^N explosion; consider whether some conditions are truly independent or whether the problem should be split.

### Step 2 — List all actions/outcomes

Identify every distinct thing the system does or returns for a given rule. There is usually one primary outcome plus secondary effects (error messages, audit logs, etc.).

### Step 3 — Generate all rules

For N binary conditions, there are 2^N possible combinations. Start by generating all of them. Use a systematic order (e.g., binary counting: YY, YN, NY, NN for 2 conditions).

### Step 4 — Fill in actions

For each rule (column), specify whether each action fires (✓ or ✗). If a rule's behavior is undefined by the spec, mark it as **GAP**.

### Step 5 — Simplify with don't-care conditions

If two adjacent rules have the same actions and differ only in one condition, that condition is irrelevant for this outcome. Merge those columns and mark the condition as `-` (don't-care). This reduces clutter.

### Step 6 — Check for gaps and contradictions

- **Gap**: A rule column where no action is specified — the system has undefined behavior
- **Contradiction**: Two identical condition columns with different actions — the spec is inconsistent
- **Dead rule**: A condition combination that is logically impossible — mark and remove

## Output format

Write the table in markdown with two sections: **Conditions** and **Actions**. One column per rule.

```markdown
## Decision Table: [Name]

| | Rule 1 | Rule 2 | Rule 3 | Rule 4 |
|---|---|---|---|---|
| **Conditions** | | | | |
| User is authenticated | Y | Y | N | N |
| User has permission | Y | N | - | - |
| **Actions** | | | | |
| Allow access | ✓ | ✗ | ✗ | ✗ |
| Redirect to login | ✗ | ✗ | ✓ | ✓ |
| Return 403 Forbidden | ✗ | ✓ | ✗ | ✗ |

**Gaps identified:**
- Rule 3 and Rule 4 produce the same action but the spec only documents Rule 3. Verify Rule 4 behavior.
```

After the table, list:
- **Gaps**: undefined or undocumented rules
- **Contradictions**: rules with conflicting outcomes
- **Impossible combinations**: condition sets that can never occur (note why)
