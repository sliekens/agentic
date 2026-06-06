# Equivalence Partitioning & Boundary Value Analysis

## What it is

**Equivalence partitioning (EP)** divides the input space into classes where every value in a class is expected to behave the same way. Once you've identified the classes, you need only one representative value per class — the assumption being that if one value in the class passes (or fails), they all will.

**Boundary value analysis (BVA)** zooms in on the edges between equivalence classes, because bugs disproportionately cluster at boundaries. For every boundary between a valid and invalid class, you test: the value just inside, the boundary value itself, and the value just outside.

EP and BVA almost always apply together. EP gives you the structure; BVA tells you which values within that structure to actually test.

## When to use

- Any method that accepts numeric ranges (age, quantity, price, score)
- String length constraints (min/max characters)
- Date/time ranges (booking windows, expiry periods)
- Enumerated sets (status codes, role types, currency codes)
- Any parameter with documented valid/invalid ranges

## How to apply

### Step 1 — Identify all input parameters

List every parameter the method or component accepts. For each one, note its type and any documented constraints.

### Step 2 — Define equivalence classes for each parameter

For each parameter, define:
- **Valid classes**: Inputs that the system should accept and process normally
- **Invalid classes**: Inputs that the system should reject (with an appropriate error)

For numeric ranges, the typical partition for a range [min, max] is:
- Invalid low: values below min
- Valid: values between min and max (inclusive)
- Invalid high: values above max

For strings:
- Too short (below minimum length)
- Valid length
- Too long (above maximum length)
- Special cases: empty string, null/undefined, non-ASCII characters

For enumerations:
- Each valid value is its own class (or group related values if behavior is identical)
- Invalid/unrecognized values form one class

### Step 3 — Apply BVA to numeric and length boundaries

For each boundary between a valid and invalid class, identify three test values:
- **Just below the boundary** (e.g., min - 1)
- **At the boundary** (e.g., min)
- **Just above the boundary** (e.g., min + 1)

Do the same for the upper boundary (max - 1, max, max + 1).

For non-numeric boundaries (e.g., string patterns, date formats), identify the analogous "just inside" and "just outside" values.

### Step 4 — Combine across parameters

If the method has multiple parameters, note which combinations are worth testing together. You don't need every combination (that's combinatorial testing), but interactions between boundary cases are worth flagging.

## Output format

Produce one table per parameter, followed by a combined test case list.

```markdown
## Equivalence Partitions: [Method/Component Name]

### Parameter: age (integer, valid range: 0–150)

| Class | Range / Values | Type | Representative value | BVA values |
|---|---|---|---|---|
| Below minimum | < 0 | Invalid | -1 | -1, 0 (boundary) |
| Valid range | 0–150 | Valid | 75 | 0, 1, 149, 150 |
| Above maximum | > 150 | Invalid | 200 | 150 (boundary), 151 |
| Null/missing | null, undefined | Invalid | null | — |

### Parameter: name (string, 1–100 characters)

| Class | Range / Values | Type | Representative value | BVA values |
|---|---|---|---|---|
| Empty | length = 0 | Invalid | "" | — |
| Valid | length 1–100 | Valid | "Alice" | 1-char, 100-char |
| Too long | length > 100 | Invalid | 101-char string | 100-char, 101-char |
| Null/missing | null | Invalid | null | — |

## Test cases derived

| # | age | name | Expected outcome |
|---|---|---|---|
| 1 | -1 | "Alice" | Reject: age below minimum |
| 2 | 0 | "Alice" | Accept (lower boundary) |
| 3 | 75 | "Alice" | Accept (representative valid) |
| 4 | 150 | "Alice" | Accept (upper boundary) |
| 5 | 151 | "Alice" | Reject: age above maximum |
| 6 | 75 | "" | Reject: name empty |
| 7 | 75 | [100-char string] | Accept (name upper boundary) |
| 8 | 75 | [101-char string] | Reject: name too long |
| 9 | null | "Alice" | Reject: age missing |

**Gaps identified:**
- Behavior for negative zero (-0) not specified
- No documentation on behavior when both age and name are invalid simultaneously
```
