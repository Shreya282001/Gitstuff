from dotenv import load_dotenv
import pandas as pd
from tqdm import tqdm
import multiprocessing
import os
import requests

def env_load():
    load_dotenv()
    return os.environ['ACCESS_TOKEN']

print(env_load())