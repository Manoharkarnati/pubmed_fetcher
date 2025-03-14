from pubmed_paper_fetcher.filter import is_non_academic

def test_is_non_academic():
    assert is_non_academic("Pfizer Inc.") == True
    assert is_non_academic("Harvard University") == False
