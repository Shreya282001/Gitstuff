from dotenv import load_dotenv
import pandas as pd
from tqdm import tqdm
import multiprocessing
import os
import requests

def env_load():
    load_dotenv()
    return os.environ['ACCESS_TOKEN']


from multiprocessing import Pool
from tqdm import tqdm
import pandas as pd
import requests
import os
from dotenv import load_dotenv

load_dotenv()

search_terms = ['The Beatles', 'Missy Elliot', 'Andy Shauf', 'Slowdive', 'Men I Trust']
n = 10
dfs = []

def genius(search_term, per_page=15):
    '''
    Collect data from the Genius API by searching for `search_term`.
    
    **Assumes ACCESS_TOKEN is loaded in the environment.**
    '''
    genius_search_url = f"http://api.genius.com/search?q={search_term}&" + \
                        f"access_token={os.getenv('ACCESS_TOKEN')}&per_page={per_page}"
    
    try:
        response = requests.get(genius_search_url)
        response.raise_for_status()
        json_data = response.json()
        return json_data['response']['hits']
    except requests.exceptions.RequestException as e:
        print(f"Error for search term '{search_term}': {e}")
        return []

def genius_to_df(search_term, n_results_per_term=10):
    json_data = genius(search_term, per_page=n_results_per_term)
    
    if not json_data:
        return pd.DataFrame()  
    
    hits = [hit['result'] for hit in json_data]
    df = pd.DataFrame(hits)

    # expand dictionary elements
    df_stats = df['stats'].apply(pd.Series)
    df_stats.rename(columns={c:'stat_' + c for c in df_stats.columns},
                    inplace=True)
    
    df_primary = df['primary_artist'].apply(pd.Series)
    df_primary.rename(columns={c:'primary_artist_' + c for c in df_primary.columns},
                      inplace=True)
    
    df = pd.concat((df, df_stats, df_primary), axis=1)
    
    return df

def process_search_term(search_term):
    df = genius_to_df(search_term, n_results_per_term=n)
    return df

if __name__ == '__main__':
    with Pool() as pool:
        dfs = list(tqdm(pool.imap(process_search_term, search_terms), total=len(search_terms)))

    df_genius = pd.concat(dfs)
    df_genius.to_csv("C:\\Users\\SHREYA\\OneDrive\\Documents\\Gitstuff\\Lab 5\\genius_data.csv", index=False)

