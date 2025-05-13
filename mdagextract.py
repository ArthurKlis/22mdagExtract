#2025-05-11/13 Kliś + coPilot AI by Microsoft

import requests
from bs4 import BeautifulSoup
import time
import os
import re

BASE_URL = "https://mdag.pl"

def extract_movie_details(url):
    """Extract detailed information about a movie."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    movie_data = {
        "title": soup.find("h1", class_="entry-title").text.strip() if soup.find("h1", class_="entry-title") else "N/A",
        "description": soup.find("div", class_="entry-single-content").text.strip() if soup.find("div", class_="entry-single-content") else "N/A",
        "english_title": soup.select_one("#single-movie-title .box-org span").text.strip() if soup.select_one("#single-movie-title .box-org span") else "N/A"
    }

    return movie_data

# Extract category URLs ONCE
with open("22mdag.html", "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "html.parser")

category_links = [BASE_URL + a["href"] for a in soup.find_all("a", href=True) if "/movies/" in a["href"]]

# Extract movie URLs ONCE
movie_links = []
for category_url in category_links:
    response = requests.get(category_url)
    category_soup = BeautifulSoup(response.text, "html.parser")
    movie_links.extend([BASE_URL + a["href"] for a in category_soup.find_all("a", href=True) if "/movie/" in a["href"]])

print(f"Total movies found: {len(movie_links)}")

# Process each movie and remove from the list
while movie_links:
    movie_url = movie_links.pop(0)  # Removes the first movie URL from the list

    movie_info = extract_movie_details(movie_url)

    title_safe = re.sub(r'[\/:*?"<>|]', '_', movie_info['title'])
    filename = f"{title_safe}.txt"

    # Skip if file already exists
    if os.path.exists(filename):
        print(f"Skipping {filename}, file already exists.")
        continue

    with open(filename, "w", encoding="utf-8") as file:
        for key, value in movie_info.items():
            file.write(f"{key}: {value}\n")

    print(f"Saved: {filename}")
    time.sleep(60)  # Prevent overload

print("Movie data extraction completed!")
