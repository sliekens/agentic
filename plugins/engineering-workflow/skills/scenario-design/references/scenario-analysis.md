# Scenario Analysis / Scenario Planning

## What it is

Scenario analysis structures the problem space as a set of **named, narrative scenarios** — each one a coherent combination of conditions, context, and stakeholder intent. Unlike decision tables (which are exhaustive and combinatorial) or FMEA (which is risk-quantified), scenario analysis is about building a shared vocabulary of meaningful situations that stakeholders can reason about together.

Each scenario is a story: who is doing what, under what conditions, and what should happen. This makes scenario analysis especially useful for requirements work, user story analysis, and anywhere the "why" and "who" matter as much as the technical "what."

## When to use

- Requirements analysis: ensuring all stakeholder use cases are covered
- API design: documenting the meaningful ways a client can use an endpoint
- User story gap-finding: checking whether acceptance criteria cover all the relevant situations
- Regulatory or compliance contexts where scenarios must be documented and signed off
- Any domain where the vocabulary of scenarios is as important as their enumeration

Scenario analysis is not the right choice when you need exhaustive combinatorial coverage (use decision tables or orthogonal arrays) or quantified risk (use FMEA). It's the right choice when you need *meaningful* scenarios that humans can reason about and validate.

## How to apply

### Step 1 — Identify the subject and participants

What is the artifact being analyzed (feature, API, business process, policy)? Who are the relevant actors (user types, systems, external parties)?

### Step 2 — Identify the key variables

What dimensions create meaningfully different situations? These might be:
- Actor type (admin, regular user, unauthenticated visitor)
- System state (first-time setup, steady state, degraded mode)
- Data state (empty, populated, at capacity)
- External conditions (third-party service available/unavailable, time-of-day constraints)

Unlike decision tables, you don't enumerate all combinations — you select combinations that are *meaningful and distinct*.

### Step 3 — Draft scenarios

For each meaningful combination, write a scenario. Each scenario should have:
- **Name**: Short, memorable label
- **Preconditions**: What must be true before the scenario begins
- **Actor**: Who initiates the action
- **Action**: What they do
- **Expected outcome**: What should happen
- **Notes**: Any open questions, assumptions, or edge cases to verify

### Step 4 — Check for coverage

After drafting, review: Are there important actors not covered? Important system states not represented? Common failure modes not included? Add scenarios for any gaps.

### Step 5 — Flag gaps and open questions

Scenarios that expose undefined behavior, missing requirements, or assumptions that haven't been validated become action items.

## Output format

```markdown
## Scenario Analysis: [Feature/System Name]

### Scenario 1: Happy path — new user registration

| Field | Value |
|---|---|
| **Actor** | Unauthenticated visitor |
| **Preconditions** | Registration form displayed; email not already registered |
| **Action** | Submits form with valid name, email, and password |
| **Expected outcome** | Account created; confirmation email sent; user redirected to onboarding |
| **Notes** | — |

---

### Scenario 2: Duplicate email registration attempt

| Field | Value |
|---|---|
| **Actor** | Unauthenticated visitor |
| **Preconditions** | Email address already registered to an existing account |
| **Action** | Submits registration form with the same email |
| **Expected outcome** | Error: "An account with this email already exists." No account created. |
| **Notes** | Should the error hint that the user can log in instead? Not specified. |

---

### Scenario 3: Registration during email service outage

| Field | Value |
|---|---|
| **Actor** | Unauthenticated visitor |
| **Preconditions** | SMTP service unavailable |
| **Action** | Submits valid registration form |
| **Expected outcome** | Account created; user notified that confirmation email will be delayed |
| **Notes** | **GAP**: Current spec does not specify fallback behavior when email cannot be sent. |

---

## Coverage summary

| Actor | Happy path | Duplicate data | Service outage | Admin intervention |
|---|---|---|---|---|
| Unauthenticated visitor | ✓ Sc.1 | ✓ Sc.2 | ✓ Sc.3 | — |
| Existing user | — | — | — | — |
| Admin | — | — | — | ❌ not covered |

**Gaps:**
- No scenarios covering admin-initiated registration (e.g., bulk import)
- No scenarios for registration via social auth (OAuth)
- Behavior during service outage not specified — requires product decision
```
