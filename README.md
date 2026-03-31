# Milpi Bot

A Discord bot that uses Playwright to scrape library event data and notify users about D&D sessions.

---

## Prerequisites

* Python 3.10+
* Git
* A Discord Bot Token (from Developer Portal)

---

## Local Setup

### 1. Clone and Enter

```bash
git clone <your-repo-url>
cd Milpi
```

### 2. Environment Setup

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install discord.py playwright python-dotenv
playwright install chromium
```

### 3. Secrets

Create a `.env` file in the root:

```env
DISCORD_TOKEN=your_token_here
```

### 4. Run

```bash
python3 milpi.py
```

---

## Google Cloud Deployment (e2-micro)

### 1. System Prep

```bash
sudo apt update && sudo apt install -y python3-pip python3-venv git nodejs npm
sudo npm install pm2 -g
```

### 2. Swap File (Required for 1GB RAM)

```bash
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile swap swap defaults 0 0' | sudo tee -a /etc/fstab
```

### 3. Install Headless Dependencies

```bash
pip install discord.py playwright python-dotenv
playwright install chromium
sudo playwright install-deps
```

### 4. Persistence with PM2

```bash
pm2 start milpi.py --interpreter ./venv/bin/python3 --name "milpi-bot"
pm2 save
pm2 startup
```

---

## Files

* `milpi.py` — Discord client and command handling
* `scraper.py` — Playwright automation logic
* `extractor.py` — Cleaning and formatting raw data
* `.gitignore` — Prevents `venv/`, `.env`, and `__pycache__` from leaking

---

## Final Check

1. Save the file
2. Look at the "Changes" sidebar in VS Code
3. If it shows only a few files (and not 1600+), run:

```bash
git add .
git commit -m "Fixed README formatting"
git push origin main
```
