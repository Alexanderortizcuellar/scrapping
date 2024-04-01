import sys
import csv
import os
import httpx
from selectolax.parser import HTMLParser, Node

URL = sys.argv[1]


def main():
    data = get_data()
    name = 0
    for table_data in data.css("table"):
        table = parse_table(table_data)
        export(table, str(name))
        name += 1


def get_data() -> Node:
    response = httpx.get(URL)
    parser = HTMLParser(response.content)
    data = parser.css_first("html")
    return data  # pyright:ignore


def parse_table(table: Node):
    parsed_data = []
    trs = table.css("tr")
    for tr in trs:
        row = []
        tds = tr.css("td,th")
        for td in tds:
            row.append(td.text(strip=True))
        parsed_data.append(row)
    return parsed_data


def export(table: list[list[str]], name: str):
    os.makedirs("tables-data", exist_ok=True)
    filename = f"tables-data/{name}.csv"
    with open(filename, "w") as file:
        writer = csv.writer(file)
        writer.writerows(table)
    print(f"exporting table {name} as {filename}")


if __name__ == "__main__":
    main()
