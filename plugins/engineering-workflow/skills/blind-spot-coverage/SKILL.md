---
name: blind-spot-coverage
description: Use this skill when deciding whether a behavior deserves a test, or when the user wants test coverage for blind spots in a specific method. A qualifying behavior gets one integration test for its longest happy path and smaller unit tests for durable edge cases and blind spots. Leave it untested when the behavior is not permanent, there is no invariant or contract to uphold, or the code is due for rearchitecture. Activate on "what should I test here?", on an explicit blind-spot request, and when `fix-loop` is about to add or keep a test. This is not line coverage. It locks durable invariants that are easy to miss.
---

# Blind Spot Coverage

Activate when the user wants to identify and cover blind spots in a specific method's test coverage, or when deciding whether a behavior deserves a test. The goal is to lock durable invariants the existing tests miss.

## What deserves a test

A test protects a durable invariant. Give a behavior a test only when that behavior is permanent and a contract or invariant must hold.

A behavior that qualifies gets:

- one integration test for the longest happy path;
- smaller unit tests for edge cases and blind spots of that same invariant.

Leave a behavior untested when any of these is true:

- the behavior is not permanent;
- there is no strong invariant or contract to uphold;
- the code is due for a rearchitecture. Replace it first with `expand-and-contract`. Test the durable invariants of the new structure after usages move.

A unit test that repeats the happy path already covered by the long integration test does not qualify. Add a test because an invariant is unlocked, not because a branch exists.

## Input

The user provides:
- **Target method** (required): The specific method/function to analyze (e.g., `UserService.validateEmail`, `parseConfig`)
- **Context** (optional): Any specific concerns or areas they want to focus on

Example: `/blind-spot-coverage UserService.validateEmail`

## Procedure

### 1. Locate the method

Find the method in the codebase. Read it thoroughly, including:
- The method signature and return type
- All parameters and their types
- The full implementation body
- Any helper methods it calls internally

### 2. Find existing tests

Locate all existing tests for this method. Look for:
- Test files with matching names (e.g., `UserService.test.ts`, `test_user_service.py`)
- Test cases that explicitly call this method
- Integration tests that exercise it indirectly

Read all existing test cases to understand what's already covered.

### 3. Analyze the method for blind spots

Apply **What deserves a test** first. If the method's behavior fails that section, say which condition failed and stop. Do not propose tests.

For a behavior that qualifies, search these categories for unlocked invariants:

**A. Input edge cases**
- Empty strings, null, undefined, zero, negative numbers
- Minimum and maximum valid values (boundary conditions)
- Values just outside valid ranges
- Special characters or unusual formats
- Extremely long inputs (performance/overflow concerns)

**B. State edge cases**
- Empty collections, initialized but unused state
- Concurrent access or race conditions (if applicable)
- State transitions that skip expected steps

**C. Error paths**
- Exceptions that could be thrown but aren't tested
- Error conditions that return special values (null, error objects)
- Network timeouts or external service failures (for I/O methods)
- Permission/authorization failures

**D. Logic branches**
- A branch that protects a durable invariant
- A `switch/case` path, including `default`, that protects a durable invariant
- A loop boundary (empty, single item, many items) that protects a durable invariant
- An early return that protects a durable invariant

**E. External dependencies**
- API calls that could fail
- Database queries that return no results
- File system operations (file not found, permission denied)
- Third-party library edge cases

**F. Time-sensitive operations**
- Operations that depend on current time/date
- Timeout conditions
- Retry logic

### 4. Cross-reference with existing tests

For each blind spot category, check if existing tests already cover it. Mark as:
- ❌ **Uncovered**: No test exists for this scenario
- ⚠️ **Partially covered**: Some but not all aspects tested
- ✅ **Covered**: Adequately tested

### 5. Prioritize blind spots

Drop any candidate that fails **What deserves a test**. Prioritize what remains by:

**High priority** (cover these first):
- Error paths that could cause crashes
- Input validation failures
- Security-sensitive operations
- Data corruption risks

**Medium priority**:
- Boundary conditions
- Edge cases in business logic
- External dependency failures

**Low priority**:
- Unusual but harmless inputs
- Performance edge cases (unless explicitly requested)
- Cosmetic issues

### 6. Generate test suggestions

For each high and medium priority uncovered blind spot, provide:

1. **The scenario** in plain English
2. **Why it matters** in one sentence
3. **Test code template** showing how to test it

Format:

```
## Blind Spots Found

### [MethodName]

#### ❌ [Scenario description]
> **Why:** [one-sentence rationale]

**Test:**
```[language]
[test code template]
```
```

Group similar scenarios together. Include the file path and line numbers for reference.

### 7. Deliver the analysis

Present findings in this order:
1. Brief summary of what the method does
2. Existing test coverage overview
3. Prioritized list of blind spots
4. Test code templates for each

End with a question: "Which of these would you like me to implement as actual tests?"

## Guidelines

- **Be pragmatic**: **What deserves a test** is the gate. A long list of theoretical edges is not a test list.
- **Respect existing style**: Match the test style, framework, and patterns already used in the codebase.
- **Stay focused**: Unit tests stay on this method's edges. The one happy-path integration test covers the longest path of the behavior, even when that path leaves the method.
- **No false positives**: Only report blind spots that actually exist. Verify the code path is real.
- **Language-aware**: Adapt to the language's testing conventions (Jest, pytest, RSpec, etc.)
