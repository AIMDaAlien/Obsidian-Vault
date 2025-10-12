# Git Troubleshooting - Non-Fast-Forward & Push Conflicts

> **Tags**: #git #troubleshooting #version-control #github #deployment
> **Related**: [[Github Pages Setup]] | [[Privacy Filter - Matrix Decode]] | [[Development Tools]]
> **Status**: 📚 Reference Guide

## Common Issue: Non-Fast-Forward Error

### The Problem

```bash
aim@MacBook-Air First-Portfolio-Iteration % git push origin
To https://github.com/AIMDaAlien/First-Portfolio-Iteration.git
 ! [rejected]        main -> main (non-fast-forward)
error: failed to push some refs to 'https://github.com/AIMDaAlien/First-Portfolio-Iteration.git'
hint: Updates were rejected because the tip of your current branch is behind
hint: its remote counterpart. Integrate the remote changes (e.g.
hint: 'git pull ...') before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.
```

### What This Means

Your local repository is **behind** the remote (GitHub) repository. Git refuses to overwrite the newer commits on GitHub with your older local commits.

### Solution Approaches

#### **Option 1: Pull First (Recommended)**
Merge remote changes into your local branch:

```bash
git pull origin main
```

This preserves all commit history. You may need to resolve conflicts if changes overlap.

#### **Option 2: Force Push (Destructive)**
**⚠️ WARNING**: This will overwrite remote history and delete any commits that exist on GitHub but not locally.

```bash
# Create backup first
git branch backup-before-force

# Force push
git push origin main --force
```

#### **Option 3: Rebase (Clean History)**
Reapply your local commits on top of remote changes:

```bash
git pull --rebase origin main
git push origin main
```

## Best Practices

### Before Pushing
1. **Always check status first**:
   ```bash
   git status
   git log --oneline -5
   ```

2. **Fetch remote changes**:
   ```bash
   git fetch origin
   git log HEAD..origin/main --oneline  # See what's different
   ```

3. **Pull before push**:
   ```bash
   git pull origin main
   ```

### Commit Message Tips

From [[Development Tools#Git Best Practices]]:

✅ **Good Commit Messages**:
```bash
git commit -m "feat: Add matrix-decode privacy filter for contact section"
git commit -m "fix: Resolve CSS animation timing in Safari"
git commit -m "docs: Update deployment checklist"
```

❌ **Poor Commit Messages**:
```bash
git commit -m "Fixed stuff"
git commit -m "Changes"
git commit -m "asdf"
```

## Platform-Specific Notes

### macOS
- Git comes pre-installed (via Xcode Command Line Tools)
- Use native Terminal or iTerm2
- SSH keys stored in `~/.ssh/`

### Credential Issues
If you see authentication errors:

```bash
# Check current remote URL
git remote -v

# Switch to SSH (recommended)
git remote set-url origin git@github.com:username/repo.git

# Or use personal access token for HTTPS
# Settings → Developer settings → Personal access tokens
```

## Recovery Scenarios

### Lost Commits After Manual Upload
If you manually uploaded files to GitHub and "lost" local commits:

1. **Check reflog** (Git's safety net):
   ```bash
   git reflog
   # Find the commit before the problem
   git reset --hard HEAD@{n}
   ```

2. **Create new branch from old commit**:
   ```bash
   git branch recovery-branch <commit-hash>
   git checkout recovery-branch
   ```

3. **Cherry-pick specific commits**:
   ```bash
   git cherry-pick <commit-hash>
   ```

## Deployment Verification

After resolving conflicts and pushing:

1. **Verify push succeeded**:
   ```bash
   git log origin/main --oneline -5
   ```

2. **Check GitHub Actions** (if enabled):
   - Go to repo → Actions tab
   - Look for green checkmarks

3. **Test deployed site**:
   - Clear browser cache: `Cmd+Shift+R` (Mac) or `Ctrl+Shift+R`
   - Check for your changes

## Related Resources

- [[Github Pages Setup]] - Deployment configuration
- [[Development Tools]] - Complete Git command reference
- [Git Documentation](https://git-scm.com/doc) - Official docs

---

*Created: October 2025*
*Based on real troubleshooting experience*