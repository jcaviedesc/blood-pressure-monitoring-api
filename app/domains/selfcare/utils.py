from bs4 import BeautifulSoup

def get_title_from_html(text: str):
    soup = BeautifulSoup(text, "html.parser")
    title = soup.find("h1")
    return title.text.strip() if title is not None else ""
