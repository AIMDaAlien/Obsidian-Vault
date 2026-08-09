# 🐧 The Gentleman's Guide to Starting DevOps on Arch Linux

**Date:** January 02, 2026
**System:** Omarchy (Arch Linux)
**Goal:** Transition from GUI/Mouse to Terminal/Keyboard & Learn Docker Fundamentals.

---

## 🧭 Part 1: The Environment (Terminal & Navigation)

Before controlling servers, one must master their own vessel. We moved away from the mouse and established a keyboard-centric workflow.

### 1. The Core Navigation Commands
Think of the file system as an upside-down tree.
* `pwd` (**Print Working Directory**): "Where am I right now?"
* `ls -la` (**List All**): "Show me everything in this room, even hidden files."
* `cd` (**Change Directory**): "Take me to this folder."
    * `cd ..` = Go up one level.
    * `cd ~` = Go home.
* `mv [file] [destination]` (**Move**): Moves a file from A to B.

### 2. The Command Center: Zellij
We installed **Zellij**, a "Terminal Multiplexer."
* **Why?** It allows us to split one window into multiple panes (like a security guard's monitor wall).
* **Installation:** `sudo pacman -S zellij`
* **Key usage:**
    * `Alt + n`: New Pane.
    * `Alt + Arrow Keys`: Move between panes.

---

## 🐳 Part 2: The Engine (Docker Installation)

We installed the **Docker Engine**. On Arch, this is a two-step process: buying the car (install) and turning on the engine (daemon).

### 1. Installation & Startup
```bash
# 1. Install the software
sudo pacman -S docker

# 2. Start the background service (The Daemon)
sudo systemctl start docker

# 3. Ensure it starts automatically on reboot
sudo systemctl enable docker
```

### 2. The Permission Fix (Vital)
By default, Docker requires `root` (sudo). To run it as a regular user:
```bash
sudo usermod -aG docker $USER
# Note: Requires a logout/login or 'newgrp docker' to take effect.
```

### 3. Visual Management: Lazydocker
Because we are visual learners, we installed a Terminal User Interface (TUI).
* **Command:** `lazydocker`
* **Function:** A dashboard inside the terminal to view logs, stats, and manage containers without memorizing commands.

---

## 🏗️ Part 3: Building & Running Containers

We moved from running pre-made software to building our own.

### 1. The Concepts
* **Image:** The Blueprint (The recipe, read-only).
* **Container:** The House (The running instance built from the blueprint).
* **Dockerfile:** The written instructions to create the Image.

### 2. The Project Structure
We created a dedicated workspace (`~/my-website`) containing:
1.  `index.html` (The content).
2.  `Dockerfile` (The recipe).

**The Dockerfile Recipe:**
```dockerfile
# Step 1: Use Nginx (a web server) as the base
FROM nginx:alpine

# Step 2: Copy our HTML file into the server's folder
COPY index.html /usr/share/nginx/html/index.html
```

### 3. The "Manual" Build & Run
```bash
# Build the image and tag it (-t)
docker build -t my-custom-site .

# Run it in the background (-d) and map ports (-p)
docker run -d -p 8081:80 my-custom-site
```
* **Port Mapping (`8081:80`):** Maps port 8081 on your **Laptop** to port 80 inside the **Container**.

---

## 🎼 Part 4: Orchestration (Docker Compose)

Manual commands are fragile. We graduated to **Infrastructure as Code (IaC)** using `docker-compose.yml`. This allows us to run a multi-container stack (Web Server + Database) with one word.

### 1. The `docker-compose.yml` File
*Note: YAML is whitespace-sensitive. Indentation must be precise (2 spaces).*

```yaml
version: '3.8'

services:
  web:
    build: .             # Build from the Dockerfile here
    ports:
      - "8080:80"        # Map ports
    container_name: production-site
    restart: always      # Auto-heal if it crashes

  redis:                 # A second service (Database)
    image: redis:alpine
    container_name: my-redis
```

### 2. The Magic Commands
* **Start Everything:** `sudo docker-compose up -d`
    * (Add `--build` to force a rebuild if you changed files).
* **Stop Everything:** `sudo docker-compose down`
    * (Stops containers and removes networks).

---

## ⚠️ Troubleshooting Log (The "Gotchas")

We encountered and solved these common DevOps hurdles:

1.  **"Mapping values are not allowed in this context"**
    * **Cause:** Bad indentation in the YAML file.
    * **Fix:** Ensure proper 2-space indentation hierarchy.

2.  **"Failed to read Dockerfile: no such file or directory"**
    * **Cause:** Running the command from the wrong folder (e.g., Home instead of `~/my-website`).
    * **Fix:** Use `cd` to enter the directory where the files actually live.

3.  **"Failed to calculate checksum / COPY failed"**
    * **Cause:** The file being copied (`index.html`) didn't exist in the folder.
    * **Fix:** Created the file or moved it to the correct directory.

4.  **"Conflict / Name already in use"**
    * **Cause:** Trying to start a new container when an old one is still running with the same name.
    * **Fix:** Use `docker-compose down` to clean up before starting again.


Ended up leaving Omarchy for CachyOS for more personalization and have a better "opinionated" distro that isnt extremely steep in a way where Id have to already know keybinds to do certain things (which ofc I should get used to).