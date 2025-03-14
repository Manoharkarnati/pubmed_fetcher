import argparse
import pandas as pd
from pubmed_paper_fetcher.fetch import search_pubmed, fetch_paper_details
from pubmed_paper_fetcher.filter import filter_non_academic_authors

def main():
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed with company-affiliated authors.")
    parser.add_argument("query", type=str, help="PubMed search query")
    parser.add_argument("-f", "--file", type=str, help="CSV output filename")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()

    if args.debug:
        print("Searching PubMed for:", args.query)

    pubmed_ids = search_pubmed(args.query)
    if not pubmed_ids:
        print("No papers found.")
        return

    papers = fetch_paper_details(pubmed_ids)
    filtered_papers = filter_non_academic_authors(papers)

    if args.file:
        df = pd.DataFrame(filtered_papers)
        df.to_csv(args.file, index=False)
        print(f"Results saved to {args.file}")
    else:
        print(filtered_papers)

if __name__ == "__main__":
    main()
