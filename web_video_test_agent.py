from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import imagehash
from PIL import Image
import time
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import agent_config as config

def setup_browser():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=1280,720")
    options.add_argument("--disable-gpu")
    options.add_argument("--autoplay-policy=no-user-gesture-required")
    return webdriver.Chrome(options=options)

def take_screenshot(driver, filename):
    driver.save_screenshot(filename)

def hash_image(path):
    img = Image.open(path)
    return imagehash.phash(img)

def run_video_test():
    driver = setup_browser()
    driver.get(config.VIDEO_PAGE_URL)
    time.sleep(5)

    hashes = []
    for i, t in enumerate(config.SCREENSHOT_INTERVALS):
        time.sleep(t)
        filename = f"screen_{i}.png"
        take_screenshot(driver, filename)
        h = hash_image(filename)
        hashes.append((t, h))

    driver.quit()
    return hashes

def generate_html_report(hashes, report_path="report.html"):
    results = []
    for i in range(1, len(hashes)):
        t1, h1 = hashes[i-1]
        t2, h2 = hashes[i]
        diff = h1 - h2
        status = "OK" if diff >= 3 else "Freeze Detected"
        results.append((t1, t2, diff, status))

    with open(report_path, "w") as f:
        f.write("<html><body><h2>Web Video Playback Test Report</h2><table border='1'>")
        f.write("<tr><th>Frame A</th><th>Frame B</th><th>Diff</th><th>Status</th></tr>")
        for row in results:
            color = "#d4edda" if row[3] == "OK" else "#f8d7da"
            f.write(f"<tr style='background:{color};'><td>{row[0]}s</td><td>{row[1]}s</td><td>{row[2]}</td><td>{row[3]}</td></tr>")
        f.write("</table></body></html>")
    return results

def send_email_report(html_file):
    with open(html_file, 'r') as f:
        html_content = f.read()

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Web Video Test Report"
    msg["From"] = config.EMAIL_FROM
    msg["To"] = config.EMAIL_TO
    msg.attach(MIMEText(html_content, "html"))

    with smtplib.SMTP_SSL(config.SMTP_SERVER, config.SMTP_PORT) as server:
        server.login(config.EMAIL_FROM, config.EMAIL_PASSWORD)
        server.sendmail(config.EMAIL_FROM, config.EMAIL_TO, msg.as_string())

def cleanup():
    for file in os.listdir():
        if file.startswith("screen_") and file.endswith(".png"):
            os.remove(file)

def main():
    print("Starting test...")
    hashes = run_video_test()
    generate_html_report(hashes)
    send_email_report("report.html")
    cleanup()
    print("Test complete. Report emailed.")

if __name__ == "__main__":
    main()
