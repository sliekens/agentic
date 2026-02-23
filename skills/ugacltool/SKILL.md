---
name: ugacltool
description: UGREEN utility for editing FACLs
---

# ugacltool — UGREEN NAS ACL Utility

`ugacltool` manages Access Control Lists (ACLs) on UGREEN NASync devices. Standard Linux `chown`/`chmod` commands don't work correctly on these devices due to their custom ACL system — use `ugacltool` instead.

## Quick Reference

### Grant read-only access (by name)

```bash
ugacltool add PATH group:NAME:allow:r-x---a-R-c--:-fd-
```

### Grant read-only access (by GID)

```bash
ugacltool addace PATH group:GID:allow:r-x---a-R-c--:-fd-
```

### Grant read+write access (by name)

```bash
ugacltool add PATH group:NAME:allow:rwxpdDaARWc--:-fd-
```

### Grant read+write access (by GID)

```bash
ugacltool addace PATH group:GID:allow:rwxpdDaARWc--:-fd-
```

### View current ACLs

```bash
ugacltool get PATH
```

### Remove a single ACL entry by index

```bash
ugacltool del_one PATH INDEX
```

> `del_one` only works with level 0 ACLs. Use `ugacltool get PATH` to find the index.

### Remove all ACLs

```bash
ugacltool del_all PATH
```

## Commands

| Command | Description |
|---|---|
| `add PATH [ACL Entry]` | Add a UG ACE to a file/directory |
| `addace PATH [ACL Entry]` | Add UG ACEs with uid/gid |
| `replace PATH [Index] [ACL Entry]` | Replace an ACE by index number |
| `get PATH` | Get UG ACL of a file/directory |
| `getace PATH` | Get UG ACEs with uid/gid |
| `get_perm PATH USERNAME` | Extract Windows permission from ACL or Linux permission |
| `get_perms USERNAME PATHS` | Extract Windows permissions for multiple paths |
| `del_one PATH [Index]` | Delete one UG ACL entry by index |
| `del_all PATH` | Delete all UG ACLs from a file/directory |
| `copy PATH_SRC PATH_DST` | Copy ACL from source to destination (ACL must exist) |
| `check PATH [ACL Perm]` | Check ACL permission of a file/directory |
| `set_eadir_acl PATH` | Set ACL for EA directory |
| `set_archive PATH [Option]` | Set ACL archive bit |
| `get_archive PATH` | Get ACL archive bit |
| `del_archive PATH [Option]` | Delete ACL archive bit |
| `stat PATH` | Get stat/archive bit |
| `lstat PATH` | Get stat/archive bit (no symlink follow) |
| `fstat PATH` | Get stat/archive bit |
| `utime PATH` | Set current time on a file |
| `enforce_inherit PATH` | Enforce ACL inheritance |

## `add` vs `addace`

- **`add`** / **`get`** — use user/group **names** (e.g., `group:docker:allow:...`)
- **`addace`** / **`getace`** — use numeric **uid/gid** (e.g., `group:121:allow:...`)

Use `addace` when the user/group only exists inside a container or when you only have numeric IDs (e.g., from a `.env` file).

## ACL Entry Format

```
[type]:name_or_id:[allow|deny]:permissions:inherit_mode
```

### Type

`user`, `group`, `owner`, `everyone`, `authenticated_user`, or `system`

### Permissions (`rwxpdDaARWcCo`)

| Flag | Meaning |
|---|---|
| `r` | **r**ead data |
| `w` | **w**rite data (create file) |
| `x` | e**x**ecute |
| `p` | a**p**pend data (create directory) |
| `d` | **d**elete |
| `D` | **D**elete child (directories only) |
| `a` | read **a**ttribute (SMB read-only/hidden/archive/system) |
| `A` | write **A**ttribute |
| `R` | **R**ead extended attribute |
| `W` | **W**rite extended attribute |
| `c` | read a**c**l |
| `C` | write a**C**l |
| `o` | get **o**wnership |

### Inherit Mode (`fdin`)

| Flag | Meaning |
|---|---|
| `f` | **f**ile inherited |
| `d` | **d**irectory inherited |
| `i` | **i**nherit only |
| `n` | **n**o propagate |

### Examples

```
user:root:allow:rwx-d---RWc--:fd--
owner:*:allow:rwx-d---RWc--:fd--
group:nginx:allow:r-x---a-R-c--:-fd-
```

## Common Workflow: Docker Container Permissions

When running Docker containers as unprivileged users on UGREEN NAS:

```bash
# 1. Create a dedicated system user
sudo useradd --system --user-group --shell /usr/sbin/nologin myapp

# 2. Find the UID/GID
id myapp

# 3. Grant the group read-only access to mounted volumes
ugacltool add /path/to/volume group:myapp:allow:r-x---a-R-c--:-fd-

# 4. Or grant read+write access if the app needs to write
ugacltool add /path/to/volume group:myapp:allow:rwxpdDaARWc--:-fd-

# 5. Run the container with the matching UID:GID
docker run -d --user UID:GID --name myapp_container myapp_image
```

## Archive Options

Used with `set_archive`, `get_archive`, and `del_archive`:

`is_inherit`, `is_read_only`, `is_owner_group`, `has_ACL`, `is_support_ACL`

---

*Source: [UGREEN Community Guide](https://guide.ugreen.community/ugos/docker/container-users.html)*
