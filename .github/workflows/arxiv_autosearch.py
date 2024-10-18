import arxiv
import pandas as pd
from datetime import date

def search_arxiv(keywords_list):
    results = []
    for keywords in keywords_list:
        query = f'"{keywords}"'
        search = arxiv.Search(
            query=query,
            max_results=10,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )
        print(f"Searching for '{keywords}' in titles...")
        try:
            for result in arxiv.Client().results(search):
                results.append({
                    'title': result.title,
                    'authors': ", ".join([author.name for author in result.authors]),
                    'published': result.published.date(),
                    'summary': result.summary,
                    'keywords': keywords
                })
        except Exception as e:
            print(f"Error searching for '{keywords}': {e}")
    return results

def save_to_github(results):
    today = date.today().strftime("%Y-%m-%d")
    df = pd.DataFrame(results)
    if df.empty:
        print("No results to save. CSV file will be empty.")
    else:
        df.to_csv(f'arxiv_results_{today}.csv', index=False)

if __name__ == '__main__':
    keywords_list = ["deep learning", "machine learning", 
                     "neural quantum states", "all you need"]
    results = search_arxiv(keywords_list)
    save_to_github(results)