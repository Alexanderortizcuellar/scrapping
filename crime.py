import os
from datetime import datetime
from time import sleep

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

url = "https://www.policia.gov.co/grupo-informacion-criminalidad/estadistica-delictiva"


def download(p, year):
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(url)
    page.is_visible("#edit-field-delito-de-impacto-tid")
    page.select_option("select#edit-field-delito-de-impacto-tid",
                       label="- Cualquiera -")
    page.select_option("select#edit-field-ano-deltos-impacto-value",
                       label=year)
    page.locator("#edit-submit-delitos-de-impacto-view").click()
    page.is_visible("table")
    table = page.locator("table").inner_html()
    soup = BeautifulSoup(table, "html.parser")
    links = soup.find_all("a")
    info = {link.text: link["href"] for link in links}
    os.makedirs(str(year), exist_ok=True)
    for link in info:
        with page.expect_download() as d:
            page.locator(f"table >> a:has-text('{link}')").click()
            file = d.value
            name = file.suggested_filename
            no_year_name = name.split(".")
            filename = year + "/" + name if year in name else year + "/" + no_year_name[
                0] + "_{}".format(year) + "." + no_year_name[1]
            file.save_as(filename)
            print("downloaded" + "  " + filename)
    print(f"Succesfully downloaded {len(links)} files.")


years = list(range(2010, 2022))

with sync_playwright() as p:
    for year in years:
        download(p, str(year))
