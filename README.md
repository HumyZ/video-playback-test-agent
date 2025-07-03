
# 🎥 AI-Powered Web Video Playback Test Agent

This project is a fully automated, AI-powered video testing agent that validates whether a web-based video player is functioning correctly. It uses **Selenium** to open a video in a browser, captures screenshots at intervals, applies **perceptual hashing** to detect frame freezes, and generates an HTML report. Optionally, it can email the report to an address.

---

## 🚀 Features

- 🔍 Detects video frame freezing using perceptual hashing (pHash)
- 🖼 Captures browser screenshots with Selenium and Headless Chrome
- 📊 Generates a visual HTML report of frame similarity
- 📧 Emails the report using secure SMTP
- ⚙️ Can be automated via `cron` or GitHub Actions

---

## 🛠️ Requirements

Install dependencies:
```bash
pip install selenium pillow imagehash
```

You also need:
- [ChromeDriver](https://sites.google.com/chromium.org/driver/) installed and available in your system PATH
- A working SMTP email account (Gmail app password)

---

## 🧪 Usage

Edit `agent_config.py` to set:
- VIDEO_PAGE_URL
- Screenshot times (in seconds)
- Email credentials and recipient

Then run:
```bash
python web_video_test_agent.py
```

---

## 🔁 Automate It

### With `cron`
```bash
0 8 * * * /usr/bin/python3 /path/to/web_video_test_agent.py
```

### With GitHub Actions
See `.github/workflows/daily-test.yml` for an example GitHub Actions workflow.

---

## 📬 Email Report

The agent sends an HTML-formatted playback report showing frame differences and freeze detection status.

---

## 📁 Project Structure

```
.
├── agent_config.py
├── web_video_test_agent.py
├── report.html
├── README.md
└── .github
    └── workflows
        └── daily-test.yml
```

---

## 📜 License

MIT License. Feel free to modify and extend.
