import requests as rq
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
from os import path

BASE_URL = "https://www.rfc-editor.org/"
RFC_INDEX = urljoin(BASE_URL + "/", "rfc-index.html")
RFC_BASE = BASE_URL + "rfc/"


def rfc_url(n):
    """
    The url for where RFC n is hosted
    """
    return RFC_BASE + f"rfc{n}.txt"


def get_available_rfcs():
    """
    Get the numbers of the currently available RFCs
    """
    content = rq.get(RFC_INDEX).content
    soup = BeautifulSoup(content, "html.parser")
    return (int(num) for num in map(lambda x: str(x.string), soup.find_all("noscript")) if re.match(r"^\d{1,4}$", num))


def update_index(index_file, rfcs):
    """
    Write the available RFCs to the index file
    """
    with open(index_file, "w") as f:
        f.writelines((str(rfc) + "\n" for rfc in rfcs))


def index_contains(index_file, rfc):
    """
    See if the index contains a specified RFC
    """
    if path.isfile(index_file):
        with open(index_file) as f:
            return str(rfc) + "\n" in f.readlines()
    return False
