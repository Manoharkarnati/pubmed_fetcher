from pubmed_paper_fetcher.fetch import search_pubmed

def test_search_pubmed():
    results = search_pubmed("cancer")
    assert isinstance(results, list)
    assert len(results) > 0
