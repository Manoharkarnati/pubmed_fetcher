import requests
import xml.etree.ElementTree as ET
from typing import List, Dict, Optional

PUBMED_SEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

def search_pubmed(query: str, max_results: int = 10) -> List[str]:
    """Searches PubMed for papers matching the query and returns PubMed IDs."""
    params = {"db": "pubmed", "term": query, "retmax": max_results, "retmode": "json"}
    response = requests.get(PUBMED_SEARCH_URL, params=params)
    response.raise_for_status()
    data = response.json()
    return data.get("esearchresult", {}).get("idlist", [])

def fetch_paper_details(pubmed_ids: List[str]) -> List[Dict[str, Optional[str]]]:
    """Fetches details of papers using PubMed IDs."""
    params = {"db": "pubmed", "id": ",".join(pubmed_ids), "retmode": "xml"}
    response = requests.get(PUBMED_FETCH_URL, params=params)
    response.raise_for_status()
    root = ET.fromstring(response.text)

    papers = []
    for article in root.findall(".//PubmedArticle"):
        paper_data = {
            "PubmedID": article.find(".//PMID").text,
            "Title": article.find(".//ArticleTitle").text,
            "Publication Date": article.find(".//PubDate/Year").text if article.find(".//PubDate/Year") else "Unknown",
            "Authors": []
        }

        for author in article.findall(".//Author"):
            last_name = author.find(".//LastName")
            affiliation = author.find(".//Affiliation")
            if last_name is not None and affiliation is not None:
                paper_data["Authors"].append({"name": last_name.text, "affiliation": affiliation.text})

        papers.append(paper_data)
    return papers
