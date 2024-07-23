from bs4 import BeautifulSoup
import requests
import smtplib
import os
from dotenv import load_dotenv
load_dotenv()

EMAIL = os.environ["MY_EMAIL"]
PASSWORD = os.environ["MY_PASSWORD"]
EMAIL_PROVIDER_SMTP_ADDRESS = os.environ["MY_EMAIL_PROVIDER_SMTP_ADDRESS"]

URL = "https://www.amazon.com/dp/B075CYMYK6?psc=1&ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6"
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.7",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/126.0.0.0 Safari/537.36",
}
response = requests.get(url=URL, headers=headers)

soup = BeautifulSoup(response.text, "html.parser")
price = soup.find(name="span", class_="aok-offscreen").getText().strip()
price_without_currency = price.split("$")[1]

price_as_float = float(price_without_currency)
print(price_as_float)

title = soup.find(id="productTitle").getText().strip()
BUY_PRICE = 100

if price_as_float < BUY_PRICE:
    message = f"{title} is on sale for {price}!"

    connection = smtplib.SMTP(EMAIL_PROVIDER_SMTP_ADDRESS, port=587)
    connection.starttls()
    connection.login(EMAIL, PASSWORD)
    connection.sendmail(
        from_addr=EMAIL,
        to_addrs=EMAIL,
        msg=f"Subject:Amazon Price Alert\n\n{message}\n{URL}".encode("utf-8")
    )

    print("Email sent!")
    print(message)