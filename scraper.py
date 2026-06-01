import requests
from bs4 import BeautifulSoup
import pandas as pd

books = []

base_url = "https://books.toscrape.com/catalogue/page-{}.html"

for page in range(1, 51):

    print(f"Scraping Page {page}...")

    url = base_url.format(page)

    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to access page {page}")
        continue

    soup = BeautifulSoup(response.text, "html.parser")

    for book in soup.find_all("article", class_="product_pod"):

        title = book.h3.a["title"]

        price = book.find("p", class_="price_color").text

        rating = book.find("p", class_="star-rating")["class"][1]

        availability = "In Stock"

        books.append({
            "Title": title,
            "Price": price,
            "Rating": rating,
            "Availability": availability,
            "Page": page
        })

# Create DataFrame
df = pd.DataFrame(books)

# Clean Data
rating_map = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

df["Price"] = (
    df["Price"]
    .astype(str)
    .str.extract(r'(\d+\.\d+)')[0]
    .astype(float)
)


df["Rating"] = df["Rating"].map(rating_map)

# Save Clean Data
df.to_csv("products.csv", index=False)

# Analytics
print("\n===================================")
print("BOOK STORE ANALYTICS")
print("===================================")

print(f"Total Books Scraped : {len(df)}")
print(f"Average Price       : £{df['Price'].mean():.2f}")
print(f"Highest Price       : £{df['Price'].max():.2f}")
print(f"Lowest Price        : £{df['Price'].min():.2f}")

print("\nTop 5 Highest Rated Books")
print("-----------------------------------")

top_books = df.sort_values(
    by=["Rating", "Price"],
    ascending=False
)[["Title", "Rating", "Price"]].head(5)

print(top_books)

print("\n===================================")
print("Data saved to products.csv")
print("===================================")