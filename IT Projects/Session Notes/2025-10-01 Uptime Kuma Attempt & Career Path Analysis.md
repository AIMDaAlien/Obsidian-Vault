# Session: Uptime Kuma Attempt & Career Path Analysis
**Date:** October 1, 2025  
**Duration:** ~45 minutes  
**Status:** ⚠️ Blocked - Hardware Limitation Discovered  
**Key Learning:** ARMv6 Pi incompatible with modern Docker

---

## What We Tried to Accomplish

**Primary Goal:** Install Uptime Kuma monitoring dashboard to test if NOC/Operations work appeals to me.

**Why This Project:**
- Tests whether I actually *like* monitoring work (core NOC skill)
- Low commitment (2-3 hours estimated)
- Builds on existing Pi-hole/WireGuard setup
- Visual learning style match
- Gateway to understanding if Operations roles fit my personality

**The Test:** If I find myself checking dashboards regularly and tweaking alerts, Operations might be my path. If I'm bored after setup, big red flag for NOC work.

---

## Career Path Analysis Completed

Before diving into the project, ran comprehensive analysis of three career paths:

### Path 1: IT Operations / NOC Analyst
**Match: 85%** (highest alignment)

**Pros:**
- Matches hardware troubleshooting background
- Minimal customer interaction (internal teams)
- 85% remote availability
- Management experience is differentiator
- Clear career ladder

**Cons:**
- Reactive firefighting mode
- Shift work (24/7 operations)
- Repetitive alert triage
- Salary ceiling ~$110k without management move

**Salary:** $55k-$75k entry → $85k-$110k mid-level

---

### Path 2: Systems Administrator / DevOps
**Match: 70%**

**Pros:**
- Higher salary ceiling ($95k-$140k mid-level)
- Build systems, not just fix them
- Process optimization skills multiply value
- Hot job market (Docker/Kubernetes)
- Pi-hole/WireGuard work directly relevant

**Cons:**
- Steeper learning curve (scripting/automation required)
- More collaborative (not ideal for introverts)
- On-call rotations common
- Requires Linux CLI comfort (my weak point currently)

**Critical insight:** This is where my process optimization mindset will really pay off, but entry barrier is higher.

---

### Path 3: IT Infrastructure Analyst / PM
**Match: 55%** (lowest)

**Pros:**
- Management experience shines
- Less technical grind, more strategy
- No on-call/shift work

**Cons:**
- **HIGH customer/stakeholder interaction** (dealbreaker for me)
- Less hands-on technical work
- Meeting-heavy culture
- My introversion works against me

**Verdict:** Not my natural fit given interaction requirements.

---

## Technical Execution: What Went Wrong

### Initial Setup Attempt

**Command used:**
```bash
docker run -d --restart=always -p 3001:3001 -v uptime-kuma:/app/data --name uptime-kuma louislam/uptime-kuma:1
```

**Error encountered:**
```
Unable to find image 'louislam/uptime-kuma:1' locally
docker: Error response from daemon: error creating temporary lease: Unavailable: connection error: desc = "transport: Error while dialing: dial unix:///run/containerd/containerd.sock: timeout"
```

### Troubleshooting Steps

**Step 1: Check Docker daemon**
```bash
sudo systemctl start docker
sudo systemctl status docker
```
Result: Docker was running (active/running), but containerd crashed

**Step 2: Containerd inspection**
```bash
sudo systemctl status containerd
```
Result: `code=dumped, signal=ILL` (illegal instruction - critical failure)

**Step 3: Nuclear option - Full Docker reinstall**
```bash
sudo apt-get remove docker docker-engine docker.io containerd runc
sudo rm -rf /var/lib/docker
sudo rm -rf /var/lib/containerd
curl -sSL https://get.docker.com | sh
sudo usermod -aG docker pi
sudo reboot
```
Result: Same error persisted

**Step 4: Hardware check**
```bash
uname -m
```
**Result: `armv6l`** ← Root cause discovered

---

## Root Cause: Hardware Blocker

**Current Pi:** ARMv6 architecture (Raspberry Pi Zero or Pi 1)

**Problem:** Modern Docker images don't support ARMv6. Containerd crashes with illegal instruction errors because it's trying to run code the CPU can't execute.

**Impact:** This blocks not just Uptime Kuma, but *every project* on my roadmap:
- Docker home cluster ❌
- Prometheus/Grafana ❌
- Nginx Proxy Manager ❌
- Vaultwarden ❌
- Any modern containerized app ❌

---

## Solutions & Budget Planning

### Option 1: Manual Install (Stopgap)
```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs git
git clone https://github.com/louislam/uptime-kuma.git
cd uptime-kuma
npm run setup
node server/server.js
```

**Downsides:**
- Manual updates (no `docker pull`)
- No process isolation
- Dependency conflicts with future projects
- Lower resume value ("manually installed" vs "deployed with Docker")
- Doesn't solve the larger problem

**Verdict:** Not worth it - kicks the can down the road

---

### Option 2: Hardware Upgrade (Recommended)

**Pi 3B+ (eBay used):** $25-35
- ARMv7/ARMv8 architecture
- Docker fully supported
- Good enough for all home lab projects

**Pi 4 (2GB, new):** $45
- Ideal sweet spot for price/performance
- Handles multiple containers smoothly
- Future-proof for next 2-3 years

**Pi 5:** $80+ (overkill)
- Not necessary for monitoring/VPN/home lab work
- Extra performance unused in these scenarios

**Decision:** Save for Pi 4 (2GB) - $45 investment unlocks entire project roadmap

---

## Key Insights from This Session

### Career Direction
**Current assessment:** Natural fit for IT Operations (85% match), but should push toward SysAdmin/DevOps territory for higher salary ceiling and better use of process optimization skills.

**Strategy:** Use Operations as entry point, skill up toward automation/infrastructure work over 2-3 years to avoid "reactive firefighting" trap.

### Technical Learning
**Critical realization:** Modern IT infrastructure is containerized. Docker isn't optional - it's foundational. My current Pi blocks all career-relevant projects.

**Resume impact:** "Deployed monitoring stack with Docker" >> "Manually installed Node.js apps"

### Budget Reality Check
**Needed investment:** $45 for Pi 4 (2GB)  
**Payoff:** Unlocks 5+ resume-worthy projects  
**ROI:** First IT job pays $55k+ entry level - this $45 investment is negligible

### Personality Testing
**The meta-lesson:** Attempting Uptime Kuma was supposed to test if I like monitoring work. Instead, hit hardware blocker that taught different lesson: need proper tools to evaluate career paths effectively.

**Still need to answer:** Do I actually *enjoy* watching dashboards and responding to alerts? Question postponed until hardware upgrade.

---

## Lessons Learned (日本語: 教訓 - kyōkun - lessons)

### Technical
1. **Check hardware compatibility first** - ARMv6 vs ARMv7/8 matters for Docker
2. **Containerd crashes = likely architecture mismatch** - not always fixable with reinstall
3. **Home lab requires minimum viable hardware** - can't build IT portfolio on 10-year-old Pi

### Career Planning
4. **Hands-on testing reveals gaps** - thought I was ready for Uptime Kuma, discovered infrastructure blocker instead
5. **Small investments enable big returns** - $45 Pi unlocks thousands in salary potential
6. **Process optimization mindset = DevOps fit** - but need to bridge Linux CLI skills gap first

### Workflow
7. **Document failures, not just successes** - this session is valuable *because* it didn't work
8. **Troubleshooting follows a pattern** - daemon check → service status → hardware verification
9. **Know when to pivot** - manual install "solves" immediate problem but creates future debt

---

## Next Steps

### Immediate (Before Next Project)
- [ ] Budget $45 for Raspberry Pi 4 (2GB model)
- [ ] Research where to buy (Amazon, Adafruit, local microcenter)
- [ ] Verify I can repurpose existing Pi-hole/WireGuard setup to new Pi
- [ ] Plan migration strategy for existing services

### After Hardware Upgrade
- [ ] Reinstall Pi-hole on new Pi 4
- [ ] Reinstall WireGuard VPN
- [ ] Attempt Uptime Kuma installation (Docker version)
- [ ] Add monitors for Pi-hole, WireGuard, router, external sites
- [ ] **Actually test if I like monitoring work** (original goal)

### Career Development (Ongoing)
- [ ] Continue George Mason IT studies
- [ ] Start GitHub documentation for completed projects (Pi-hole, WireGuard)
- [ ] Research NOC analyst job descriptions to validate skill requirements
- [ ] Consider AWS Cloud Practitioner cert (still evaluating ROI)

---

## Why This Session Matters

**Many people would view this as a "failed" session.** Wrong perspective.

**What was actually accomplished:**
1. ✅ Identified critical hardware blocker affecting *all* future projects
2. ✅ Comprehensive career path analysis (Operations vs SysAdmin vs Infrastructure)
3. ✅ Learned Docker troubleshooting process
4. ✅ Established minimum hardware requirements for home lab
5. ✅ Created budget plan ($45 investment = career enabler)
6. ✅ Documented real troubleshooting workflow (resume-worthy)

**Real-world parallel:** In actual IT jobs, you'll hit blockers constantly. Knowing when to troubleshoot vs when to upgrade infrastructure is a critical skill. This session demonstrated that judgment.

---

## Documentation Value

**For future interviews when asked "Tell me about a time you encountered a technical problem":**

*"I was building a home monitoring lab to learn NOC operations skills. Attempted to deploy Uptime Kuma via Docker but hit containerd crashes. Systematically troubleshot - checked daemon status, reinstalled Docker, verified service health. Eventually traced root cause to ARMv6 architecture incompatibility. Rather than implementing a hacky manual workaround, I made the business decision to upgrade infrastructure since it blocked multiple future projects. This taught me to evaluate technical debt vs investment tradeoffs - sometimes the 'quick fix' creates more problems long-term."*

**That answer demonstrates:**
- Systematic troubleshooting
- Root cause analysis
- Business thinking (tech debt awareness)
- Long-term planning
- Honest failure assessment

---

## Session Metadata

**Tools used:**
- SSH into Raspberry Pi
- Docker installation attempts
- systemctl service management
- uname hardware verification

**Time spent troubleshooting:** ~30 minutes

**Realization moment:** When `uname -m` showed `armv6l` - instant clarity on why nothing worked

**Emotional journey:** Excitement → frustration → confusion → clarity → planning

**Alfred's assessment:** "Master Aim, this is 石橋を叩いて渡る (*ishibashi wo tataite wataru* - tap the stone bridge before crossing) in action. You tested before committing to a path, discovered a foundational issue, and adjusted course rationally. That's precisely the mindset that succeeds in IT operations."

---

## Related Notes
- [[Pi-hole Setup]] - Current working project on same Pi
- [[WireGuard VPN Configuration]] - Recently completed, also on ARMv6 Pi
- [[IT Project Roadmap]] - Full list of planned projects (all blocked by hardware)
- [[Career Path Analysis]] - Detailed breakdown of Operations vs SysAdmin paths
- [[Budget Tracking]] - Need to add $45 Pi 4 purchase

**Status:** 🔴 Blocked - awaiting hardware upgrade  
**Priority:** High (blocks entire project roadmap)  
**Estimated resume date:** When Pi 4 acquired

---

*Note: This "failed" setup is one of the most valuable sessions documented. Real learning comes from hitting walls and understanding why, not just from things working on the first try.*