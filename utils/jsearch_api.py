import os 
import requests
from dotenv import load_dotenv

load_dotenv()

def find_jobs(query, location=None, page=1, num_jobs=10):
    """Find jobs based on a query, location, page number, and number of jobs."""
    try:
        url = "https://jsearch.p.rapidapi.com/search"

        print("RAPIDAPI_KEY:", os.getenv("RAPIDAPI_KEY"))

        headers = {
            "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
            "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
        }
        params = {
            "query": query,
            "page": page,
            "num_jobs": num_jobs
        }
        if location:
            params["location"] = location
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code != 200:
            raise Exception(f"Error fetching jobs: {response.status_code} - {response.text}")
        
        results = response.json().get("data", [])[:num_jobs]
        if not results:
            raise ValueError("No jobs found for the given query.")
        
        print (response.json())
        
        print(results)
        
        return results
    except Exception as e:
        print(f"An error occurred while finding jobs: {e}")
        return []