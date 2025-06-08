import os 
import requests

def find_jobs(query, location=None, page=1, num_jobs=10):
    """Find jobs based on a query, location, page number, and number of jobs."""
    try:
        url = "https://jsearch.p.rapidapi.com/search"

        headers = {
            "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
            "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
        }
        params = {
            "query": query,
            "location": location,
            "page": page,
            "num_jobs": num_jobs
        }
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code != 200:
            raise Exception(f"Error fetching jobs: {response.status_code} - {response.text}")
        
        results = response.json().get("data", [])[:num_jobs]
        if not results:
            raise ValueError("No jobs found for the given query.")
        
        return results
    except Exception as e:
        print(f"An error occurred while finding jobs: {e}")
        return []