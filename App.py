import requests
from bs4 import BeautifulSoup
import time
import csv
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

url = "https://www.amazon.com/dp/B09G3HRMVB"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def check_price():
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    title = soup.find(id="productTitle").get_text(strip=True)
    try:
        price = soup.find("span", {"class": "a-offscreen"}).get_text(strip=True)
    except AttributeError:
        price = "Fiyat Bulunamadı"
    print(f"Ürün Adı: {title}\nFiyat: {price}")
    save_to_csv(title, price)
    return title, price

def save_to_csv(title, price):
    with open("fiyatlar.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now(), title, price])

def send_email(subject, message):
    sender = "your_email@gmail.com"
    password = "your_password"
    receiver = "target_email@gmail.com"

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "plain"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, receiver, msg.as_string())
    print("E-posta gönderildi.")

while True:
    title, price = check_price()
    send_email("Ürün Fiyat Güncellemesi", f"{title} fiyatı: {price}")
    time.sleep(3600)
