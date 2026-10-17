---
tags: [meta, privacy]
created: 2026-10-16
publish: true
---

# Redaction Conventions

This vault is public. To keep my home network and the people I work with private, identifying details are replaced in place with the placeholders below, so the notes still read naturally and the technical ideas stay intact.

| Placeholder | What it stands for |
|---|---|
| `<lan-ip-N>` | A private address on my home network, where N numbers each distinct machine. |
| `<wan-ip>` | The public internet address of my home connection. |
| `<mac>` | A network hardware (MAC) address. |
| `<ddns-host>` | A dynamic DNS hostname that points at my home connection. |
| `<tailnet-host>` | A machine name on my private Tailscale network. |
| `<phone>` | A telephone number. |
| `<customer-A>` | A client or customer, kept anonymous. |
| `<customer-B>` | A second, different client or customer. |
| `~` | My home directory, standing in for the full path on my computer. |
| `<user>@<host>` | A login name and machine name, as used in SSH commands. |
| `<env-path>` | A file path that points to a private environment or secrets file. |
| `<admin-user>` | An administrator account name. |
| `<private-deployment>` | The name or address of a deployment that is not public. |

The `<lan-ip-N>` numbering is stable across the vault, so `<lan-ip-1>` always means the same machine in every note.

Some lines, such as device-enrollment URLs and commands that carry credentials, were removed outright rather than replaced, because a placeholder would not make them safe to share.

An HTML comment of the form `<!-- embed removed: name (file not in vault) -->` marks where a note embedded an image or file that was never part of the vault, so the original reference is kept for context but nothing renders. A line reading *screenshot removed: showed workstation identifiers* marks a screenshot that was deleted because it showed details of my computer, such as a user folder path.
