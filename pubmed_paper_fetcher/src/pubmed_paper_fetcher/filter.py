import re
from typing import List, Dict

def is_non_academic(affiliation: str) -> bool:
    """Checks if an affiliation belongs to a non-academic company."""
    academic_keywords = ["university", "institute", "school", "college", "lab", "hospital"]
    return not any(re.search(rf"\b{word}\b", affiliation, re.IGNORECASE) for word in academic_keywords)

def filter_non_academic_authors(papers: List[Dict]) -> List[Dict]:
    """Filters authors affiliated with non-academic companies."""
    filtered_papers = []
    for paper in papers:
        non_academic_authors = [author["name"] for author in paper["Authors"] if is_non_academic(author["affiliation"])]
        company_affiliations = [author["affiliation"] for author in paper["Authors"] if is_non_academic(author["affiliation"])]

        if non_academic_authors:
            paper["Non-academic Authors"] = non_academic_authors
            paper["Company Affiliations"] = company_affiliations
            filtered_papers.append(paper)
    return filtered_papers
