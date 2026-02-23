---
name: synouser
description: Synology utilities for managing local users and groups
---

# synouser & synogroup — Synology User & Group Management

`synouser` and `synogroup` manage local, domain, and LDAP users and groups on Synology DSM. Use them instead of standard Linux `useradd`/`groupadd` commands, which bypass the Synology user database.

## Quick Reference

### List all local users

```bash
synouser --enum local
```

### Get details for a user

```bash
synouser --get USERNAME
```

### Get user by UID

```bash
synouser --getuid UID
```

### Add a new local user

```bash
synouser --add USERNAME PASSWORD "Full Name" EXPIRED MAIL PRIVILEGE
```

- `EXPIRED`: `0` = active, `1` = expired/disabled
- `MAIL`: email address or empty string `""`
- `PRIVILEGE`: privilege level (typically `0`)

**Example:**

```bash
synouser --add myuser 'P@ssw0rd' "My User" 0 "" 0
```

### Modify a user

```bash
synouser --modify USERNAME "Full Name" EXPIRED MAIL
```

### Change a user's password

```bash
synouser --setpw USERNAME NEWPASSWORD
```

### Rename a user

```bash
synouser --rename OLD_USERNAME NEW_USERNAME
```

### Delete one or more users

```bash
synouser --del USERNAME1 USERNAME2 ...
```

### Rebuild the user database

```bash
synouser --rebuild all
```

> Use `--rebuild` after making changes outside of DSM, or to sync domain/LDAP users.

## Commands

| Command | Description |
|---|---|
| `--enum {local\|domain\|ldap\|all\|domain_used}` | List users by source |
| `--enumpre {local\|domain\|all\|domain_used} PREFIX CASELESS` | List users with a name prefix |
| `--enumsub {local\|domain\|all\|domain_used} SUBSTR CASELESS` | List users with a name substring |
| `--enum_admin {local\|domain\|ldap\|all}` | List admin users |
| `--get USERNAME` | Show details for a user |
| `--getuid UID` | Look up user by UID |
| `--add USERNAME PWD "FULL NAME" EXPIRED MAIL PRIVILEGE` | Create a new local user |
| `--modify USERNAME "FULL NAME" EXPIRED MAIL` | Update user details |
| `--rename OLD NEW` | Rename a user |
| `--setpw USERNAME NEWPASSWD` | Set a user's password |
| `--del USERNAME...` | Delete one or more users |
| `--login USERNAME PWD` | Test credentials |
| `--rebuild {all\|(domain FORCE)\|(ldap FORCE)}` | Rebuild the user database |
| `--create_homes {domain\|ldap}` | Create home directories for domain/LDAP users |
| `--revoke_password_pending USERNAME` | Clear a pending password-change requirement |
| `--filesetpw` | Apply password changes from a file |

## `--get` Output Fields

```
User Name   : [username]
User Type   : [AUTH_LOCAL]
User uid    : [1024]
Primary gid : [100]
Fullname    : [Display Name]
User Dir    : [/var/services/homes/username]
User Shell  : [/bin/sh]
Expired     : [false]
User Mail   : [user@example.com]
Alloc Size  : [0]
Member Of   : [N]
(gid) groupname
...
```

## Notes

- `synouser` only manages **user accounts**. Use `synogroup` (below) to manage group membership.
- Changes take effect immediately in DSM without a restart.
- DSM home directories are located under `/var/services/homes/`.
- The `--login` command can be used to validate credentials without actually logging in.

---

# synogroup — Synology Group Management Utility

`synogroup` manages local, domain, and LDAP groups on Synology DSM. Use it alongside `synouser` when assigning users to groups.

## Quick Reference

### List all local groups

```bash
synogroup --enum local
```

### Get details for a group

```bash
synogroup --get GROUPNAME
```

### Get group by GID

```bash
synogroup --getgid GID
```

### Create a group (with optional initial members)

```bash
synogroup --add GROUPNAME USERNAME1 USERNAME2 ...
```

### Add a single user to a group

```bash
synogroup --memberadd GROUPNAME USERNAME
```

### Set the full member list for a group (replaces existing members)

```bash
synogroup --member GROUPNAME USERNAME1 USERNAME2 ...
```

> This **replaces** the entire member list. To add without removing others, use `--memberadd`.

### Rename a group

```bash
synogroup --rename OLD_GROUPNAME NEW_GROUPNAME
```

### Delete one or more groups

```bash
synogroup --del GROUPNAME1 GROUPNAME2 ...
```

### Get/set a group description

```bash
synogroup --descget GROUPNAME
synogroup --descset GROUPNAME "Description text"
```

## Commands

| Command | Description |
|---|---|
| `--enum [{local\|domain\|ldap\|all}]` | List groups by source |
| `--enumpre {local\|domain\|all} PREFIX CASELESS` | List groups with a name prefix |
| `--enumsub {local\|domain\|all} SUBSTR CASELESS` | List groups with a name substring |
| `--get GROUPNAME` | Show details for a group |
| `--getgid GID` | Look up group by GID |
| `--descget GROUPNAME` | Get group description |
| `--descset GROUPNAME "DESC"` | Set group description |
| `--add GROUPNAME USERNAME...` | Create a group with initial members |
| `--rename OLD NEW` | Rename a group |
| `--member GROUPNAME USERNAME...` | Replace the full member list |
| `--memberadd GROUPNAME USERNAME` | Add a single user to a group |
| `--del GROUPNAME...` | Delete one or more groups |
| `--rebuild {all\|(domain FORCE)\|(ldap FORCE)}` | Rebuild the group database |

## Common Workflow: Service Account Setup

When adding a service account (e.g., for a Docker container) and granting it group access:

```bash
# 1. Create the user (expired=1 disables interactive login)
sudo synouser --add myservice "" "My Service" 1 "" 0

# 2. Create a group for it (or skip if adding to an existing group)
sudo synogroup --add myservice_group myservice

# 3. Add the user to an existing shared group
sudo synogroup --memberadd media myservice

# 4. Verify
synogroup --get media
```
