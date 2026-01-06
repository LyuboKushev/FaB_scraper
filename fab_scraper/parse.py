import re
from urllib.parse import urljoin

BASE_URL = "https://fabtcg.com"

def extract_headers(table):
    return [th.get_text(strip=True) for th in table.find_all("th")]

def extract_rows(soup, headers):
    table = soup.find("table")
    rows = table.find_all("tr")[1:]

    results = []
    for row in rows:
        cells = row.find_all("td")
        if not cells:
            continue

        entry = {
            headers[i]: cells[i].get_text(strip=True)
            for i in range(len(cells))
        }

        link = cells[2].find("a")
        entry["deck_url"] = urljoin(BASE_URL, link["href"]) if link else None
        results.append(entry)

    return results

def get_max_page(soup):
    pages = set()
    for a in soup.find_all("a", href=True):
        m = re.search(r"/decklists/page/(\d+)/", a["href"])
        if m:
            pages.add(int(m.group(1)))
    return max(pages)
