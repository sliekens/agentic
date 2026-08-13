# ugacltool

UGREEN utility for editing FACLs.

## Skills

- **ugacltool**: UGREEN NAS ACL utility. Use when editing UGOS ACLs, converting a path back to Linux mode, or choosing between chmod and del_all.

## Change Log

### v1.0.1

- Document that `del_all` leaves mode 000 and can zero inherited children; use `chmod` to return a path to Linux mode

### v1.0.0

- Add the ugacltool skill for reading and editing UGOS ACLs on UGREEN NAS
- Document command quick reference, ACL entry format (allow/deny and special types), and inconsistent exit codes
