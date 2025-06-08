import os 
import requests
import streamlit as st
from dotenv import load_dotenv

def find_jobs(query, location=None):
    """Find jobs based on query and location."""
    url = "https://jsearch.p.rapidapi.com/search"
    
    # Create a focused query - don't send more than 5-6 words
    query_words = query.split()
    focused_query = " ".join(query_words[:6])
    
    params = {"query": focused_query, "page": "1", "num_pages": "1"}
    
    if location and location.strip():
        params["location"] = location.strip()
    
    headers = {
        "X-RapidAPI-Key": st.secrets["RAPIDAPI_KEY"],
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        data = response.json()
        
        # Properly extract jobs from the response
        if data.get("status") == "OK" and "data" in data:
            return data["data"]  # Return just the jobs array
        else:
            print(f"API error: {data}")
            return []
            
    except Exception as e:
        print(f"Error searching for jobs: {e}")
        return []