# Building a Beast: TrueNAS SAS Server for $270

*How I turned $50 of enterprise drives into a legitimate storage server*

## What We Built

**The Mission**: Take 10 crusty enterprise SAS drives and build a proper NAS that doesn't suck  
**The Budget**: ~$270 total (including the drives that started this whole thing)  
**The Result**: 5.46TB of bulletproof storage that works with literally every device in my house  
**Bonus Round**: Threw Immich on there and ditched Google Photos like a boss

---

## The Hardware Shopping List

### The Brains: i5-11400 System ($190)

Here's where I almost screwed up - initially looked at 6th-8th gen Intel to save money. **Big mistake.** Those old chips max out at DDR4-2400, which means if you've got DDR4-3600 RAM lying around (like I did), you're only using 67% of its capability. That's like buying a sports car and only using 3rd gear.

The 11th gen i5-11400 hits the sweet spot:
- Supports DDR4-3200 (89% utilization of DDR4-3600 - good enough)
- 6 cores, built-in graphics (no GPU needed)
- Runs cool, doesn't guzzle power
- Found a complete system for $190 (originally quoted $280-380, so that was a win)

**Lesson learned**: Match your CPU generation to your RAM speed or you're wasting money.

### The Storage Controller: LSI 9207-8i ($35)

This is the magic piece that lets your computer talk to enterprise SAS drives. Here's what matters:

**IT Mode is CRITICAL** - This means "Initiator Target" mode, basically the card acts as a dumb passthrough. You want this because:
- ZFS (TrueNAS's file system) does all the RAID magic
- RAID mode on the card would fight with ZFS = bad time
- Pre-flashed cards with P20 firmware are worth the extra $5

The card has 2 SFF-8087 ports, each handles 4 drives = 8 drives total.

### Cables That Don't Suck ($30)

**Get SFF-8087 to SATA cables with integrated SATA power.** Each cable:
- One SFF-8087 end plugs into HBA
- Four SATA data + power connectors on the other end
- Need 2 cables for 8 drives

Why integrated power? Because Molex adapters are from the stone age and will haunt your dreams.

### Everything Else

- **Boot Drive**: 128GB NVMe SSD ($15) - dedicated to TrueNAS, nothing else
- **PSU**: 500W minimum - 8 drives + system draws ~140W
- **Drives**: 10x 1.2TB SAS drives (1.09TB usable each) - $50 for the lot

**Total damage**: ~$270 for what would cost $800+ buying prebuilt.

---

## The Build Process (Or: How I Learned To Stop Worrying And Love ZFS)

### Step 1: Cable Management Reality Check

**What you're connecting**:
1. HBA card into PCIe slot
2. SAS cables: HBA → Drives (data)
3. Power: PSU → SAS cables → Drives (via integrated SATA power)

It's gonna look messy. Accept this now. We're going for functional, not Instagram-worthy.

### Step 2: Installing TrueNAS

**The Right Way**:
1. Boot from TrueNAS USB installer
2. Install to the entire 128GB NVMe (not a partition - the whole drive)
3. Remove USB, reboot from NVMe
4. Never dual-boot a NAS, it's asking for trouble

### Step 3: Network Setup (Console Edition)

First boot drops you into a console menu. You need to configure networking to access the web interface.

```
Pick Option 1: Configure Network Interfaces
Interface: eno1 (or whatever yours is called)
```

**Two paths here**:
- **DHCP**: Router assigns IP automatically (quick but IP might change)
- **Static IP**: Set it once, never worry about it again (recommended)

For static, you need:
- IP: Something like 192.168.0.120
- Netmask: Usually 255.255.255.0
- Gateway: Your router IP (probably 192.168.0.1 or 192.168.1.1)
- DNS: 8.8.8.8 works fine

**Pro tip**: If the console's static IP wizard acts weird (it does sometimes), just use DHCP now and set static IP later in the web GUI. Life's too short to fight with ncurses interfaces.

After saving, the console shows: `Web interface available at: http://192.168.0.XXX`

### Step 4: Web Interface First Login

Open browser, go to that IP.
- Username: `admin`
- Password: What you set during install, or try blank (then it forces you to set one)

Welcome to the good stuff. Everything from here is point-and-click.

### Step 5: Creating The Storage Pool (The Main Event)

Navigate to: **Storage → Create Pool**

**Settings**:
- Name: `Storage_Pool` (or whatever you want)
- Layout: **RAID-Z2** (this is important)

**What's RAID-Z2?** It's ZFS's version of RAID-6. Here's the math:
- 7 drives in my case (one was dead, we'll get to that)
- 5 drives for actual data
- 2 drives for parity (error correction)
- Can lose ANY 2 drives and not lose a single byte
- Usable space: ~5.46TB from 7.63TB raw

**In the wizard**:
- Width: 7 (how many drives in the group)
- Number of VDEVs: 1 (how many RAID groups)
- Click through the optional stuff (Log, Cache, Spare) - skip it all unless you know you need it

Hit Create, confirm you're okay with wiping the drives, wait 30 seconds. Done.

### Step 6: Sharing Is Caring (SMB Setup)

**Create a dataset** (think of it as a top-level folder):
```
Storage → Storage_Pool → Add Dataset
Name: Shared
Hit Save
```

**Enable SMB** (works on Windows, Mac, Linux, Android - everything):
```
Shares → Windows (SMB) Shares → Add
Path: /mnt/Storage_Pool/Shared
Name: Shared
Enable: Yes
```

**Connecting from your devices**:
- **Windows**: Open File Explorer → Type `\\192.168.0.120` in address bar
- **Mac**: Finder → Go → Connect to Server → `smb://192.168.0.120`
- **Linux**: File manager → Connect to Server → `smb://192.168.0.120`
- **Android**: Install Solid Explorer, FX File Explorer, or Material Files
  - Add network storage → SMB
  - Server: 192.168.0.120
  - Username: admin
  - Password: your TrueNAS password
  - Domain: Leave blank (or try "WORKGROUP" if it insists)

Log in with your `admin` account and password. You're in.

### Step 7: Immich (Self-Hosted Google Photos Killer)

This part's almost too easy.

```
Apps → Discover Apps → Search "Immich" → Install
```

That's it. TrueNAS handles the containers, database, everything. After install completes (5-10 min), access at `http://192.168.0.120:2283`

**Importing Google Photos**:
1. Request Google Takeout (photos only, zip format)
2. Download to computer (~15-20GB takes 30-60 min)
3. Copy to NAS via SMB
4. Immich web interface → Upload → drag and drop

Immich will churn for 1-2 hours generating thumbnails and doing facial recognition. When it's done, you've got your own private Google Photos that you actually control.

---

## Maintenance (The Boring But Important Stuff)

### Set It And Forget It Tasks

**Monthly Scrub** (checks data integrity):
```
Data Protection → Scrub Tasks → Add
Pool: Storage_Pool
Schedule: Monthly, 3AM on a weekend
```

This reads every block and verifies checksums. Catches bit rot before it becomes data loss.

**Weekly SMART Tests** (drive health monitoring):
```
Tasks → S.M.A.R.T. Tests → Add
Disks: All
Type: Short
Schedule: Weekly
```

Watches for dying drives so you can replace them before they take your data with them.

**Snapshots** (undo button for file deletion):
```
Data Protection → Periodic Snapshot Tasks → Add
Dataset: Storage_Pool/immich (or whatever needs protection)
Schedule: Hourly
Retention: Keep 7 days worth
```

Snapshots are NOT backups - they save disk state so you can roll back. If the whole NAS explodes, snapshots won't help you.

---

## When Things Go Sideways (Troubleshooting)

### No Display On Boot

**Symptoms**: Power on, fans spin, absolutely nothing on screen. No BIOS, no nothing.

**The usual suspects**:

1. **RAM not seated** (this was my problem)
   - Power off, unplug everything
   - Pull all RAM sticks out
   - Push them back in until you hear the click
   - Start with ONE stick in slot A2 (check motherboard manual)
   - If it boots, add the rest one at a time

2. **Loose HDMI/DisplayPort cable**
   - Yeah, I felt dumb about this one
   - Reseat both ends
   - Try a different cable
   - Try a different port on the motherboard

3. **Clear CMOS** (resets BIOS to defaults)
   - Remove the watch battery from motherboard for 30 seconds
   - Or use the CMOS jumper if your board has one
   - Put it back, try again

4. **HBA causing issues**
   - Pull the LSI card temporarily
   - Try booting without it
   - If it works, reseat the card

### Drive Shows 0 B Size

**What happened**: One of my 10 drives (sda) showed up in the list but reported 0 bytes capacity.

**What it means**: Drive's either failed, or cable connection is sketchy.

**How to fix**:
1. Match the serial number to the physical drive label
2. Power down, reseat that specific drive
3. Check the SAS cable connection at the HBA end
4. Still broken? Try the drive in a different position
5. If it still shows 0 B, the drive's probably toast

In my case, I just proceeded with 7 drives and kept the bad one as a parts donor. Still got 5.46TB usable.

### Network Configuration Acting Weird

**Console won't show static IP fields**: This is a known bug. Just use DHCP to get started, then set static IP in the web GUI under Network → Global Configuration.

**Can't access web interface**:
- Check the IP address shown on the console (it's right there on the main screen)
- Ping the IP from another computer to test connectivity
- Make sure your firewall isn't blocking it
- Try a different browser (sometimes helps, sometimes doesn't)

### Pool Creation Confusion

**"Why are only 7 drives showing in automated mode?"**

One drive probably has old partitions or data. Click "Manual Disk Selection" to see all drives and select them individually. TrueNAS will wipe them during pool creation.

**"Width and VDEVs sound made up"**
- Width = drives per RAID group (set this to however many drives you're using)
- VDEVs = number of RAID groups (usually 1 unless you're doing something fancy)

---

## Pro Tips & Things I Wish I'd Known

### Security Stuff

**Make your life harder for the bad guys**:
- Set a static IP outside your router's DHCP range
- Disable services you're not using (System → Services)
- Keep TrueNAS updated (it'll nag you, don't ignore it)
- Consider VLANs if you're paranoid (or just smart)

**Snapshots ≠ Backups**: Say it with me. Snapshots protect against "oops I deleted that", not "the house burned down". For real backup:
- 3 copies of data
- 2 different storage types
- 1 offsite copy

For 15-20GB of photos, Backblaze B2 costs about $1/month. Set it and forget it.

### Performance Tweaks

**If you go 10GbE later**: The 11th gen Intel system supports 10 gigabit ethernet via PCIe card. You'll need a compatible switch, but when you're moving TBs around, it's worth it.

**RAM is ZFS's best friend**: General rule is 1GB RAM per TB of storage. More RAM = better caching = faster everything. 8GB minimum, 16GB+ makes ZFS happy.

### Adding The 8th Drive Later

When you fix that dead drive (or just want more space):
```
Storage → Storage_Pool → Manage Devices → Extend
Select the new drive
Wait several hours for "resilvering" (ZFS rebuilding parity)
New usable capacity: 6.5TB
```

---

## The Command Line Stuff (For When You Want To Feel Like A Hacker)

Access via: System → Shell in web interface

**Find a drive by serial number**:
```bash
lsblk -o NAME,SERIAL,SIZE
```

**Check pool health**:
```bash
zpool status
```

**Watch a scrub in progress**:
```bash
zpool status -v
```

**Check drive temperatures**:
```bash
smartctl -A /dev/sda | grep Temperature
```

**Find where Immich is storing stuff**:
```bash
find /mnt -name "*immich*" -type d
```

---

## The Bill (What It Actually Cost)

| Component | Price | Notes |
|-----------|-------|-------|
| i5-11400 system | $190 | Found a deal, was quoted $280-380 |
| LSI 9207-8i HBA | $35 | Pre-flashed with IT mode firmware |
| 10x SAS drives | $50 | 1.2TB enterprise drives |
| 128GB NVMe boot | $15 | Dedicated to TrueNAS |
| SAS cables | $30 | With integrated SATA power |
| **TOTAL** | **$320** | Using 7 of 10 drives = ~$285 in practice |

Compare this to a Synology with similar specs: $800+. Yeah.

---

## Lessons From The Trenches

**Things that would've saved me time**:

1. **Check CPU RAM support first** - Don't waste premium DDR4-3600 on a CPU that maxes at DDR4-2400
2. **IT mode matters** - If your HBA is in RAID mode, ZFS will fight with it and you'll have a bad time
3. **Get the right cables** - SFF-8087 to SATA with integrated power. Don't cheap out with Molex adapters
4. **Expect DOA drives** - Enterprise pulls are cheap for a reason. One dead drive out of ten isn't bad luck, it's expected
5. **Dedicated NAS = happy NAS** - Don't dual-boot, don't share with gaming PC, just let it be a NAS
6. **Console is for network only** - Configure networking in the console, do everything else in the web GUI
7. **RAID-Z2 minimum** - Single parity (RAID-Z1) is playing with fire. Always go RAID-Z2

---

## Resources That Actually Helped

- TrueNAS Official Docs: https://docs.truenas.com
- Immich Documentation: https://immich.app/docs
- ServeTheHome Forums: Where enterprise gear nerds hang out
- r/TrueNAS: When you need 5 different opinions on the same problem

---

**Status**: Running solid, 5.46TB ready to go  
**Build Time**: ~4 hours including troubleshooting the RAM thing  
**Would I do it again?** Absolutely. Beats paying Google $10/month forever.