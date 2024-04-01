from pathlib import Path
import sys
from urllib.request import urlretrieve
from urllib.parse import urljoin
import csv
import httpx
from selectolax.parser import HTMLParser


def parse_data():
    urls = []
    if len(sys.argv) == 1:
        print("Not url provided")
        return None
    url = sys.argv[1]
    response = httpx.get(url)
    if response.status_code != 200:
        print("status code: ", response.status_code)
        return None
    parser = HTMLParser(response.content)
    images = parser.css("img")
    for img in images:
        # image src
        img_src = img.attributes["src"]
        img_url = urljoin(url, img_src)
        urls.append(img_url)
    return urls


def download_images(urls, folder: str):
    Path(folder).mkdir(exist_ok=True)
    with open(f"{folder}/urls.csv", "w") as file:
        writer = csv.writer(file)
        for url in urls:
            # extract name from url
            name = url.split("/")[-1]
            filename = Path(folder).joinpath(name)
            urlretrieve(url, filename)
            writer.writerow(url)
            print(f"saving file as {filename}")


def main():
    if len(sys.argv) < 3:
        print("Not destination folder provided")
        exit()
    parser = parse_data()
    if parser is not None:
        urls = parse_data()
        download_images(urls, sys.argv[2])


if __name__ == "__main__":
    main()
