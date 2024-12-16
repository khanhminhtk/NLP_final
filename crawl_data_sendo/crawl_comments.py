import os
import re
import requests
import pandas as pd


def read_products_id(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        products_list = f.read().split("\n")
    products_id = [
        re.search(r'-(\d+)\.html', product).group(1)
        for product in products_list
    ]
    return products_id

def crawl_comments(products_id, avg_cmt_prod=10):
    comments = {
        "comments": [],
        "status": []
    }
    for product_id in products_id:
        url = f"https://ratingapi.sendo.vn/product/{product_id}/rating?page=1&limit={avg_cmt_prod}&sort=review_score&v=2&star=all"
        response = requests.get(url)
        json_data = response.json()
        reviews = json_data.get('data', [])
        for review in reviews:
            if review.get("comment") == "":
                continue
            comments["comments"].append(review.get("comment"))
            comments["status"].append(review.get("status"))
    return comments

if __name__ == "__main__":
    products_list = list(set(read_products_id("./data/products_id.txt")))
    comments = crawl_comments(products_list, 20)
    df = pd.DataFrame(comments)
    df.to_csv("./data/comments.csv", index=False)
    