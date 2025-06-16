from duckduckgo_search import DDGS, exceptions
import requests
import time
import random
from serpapi import GoogleSearch
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("SERP_API_KEY")
# def fetch_and_save_first_image(query, save_path='downloaded_image.jpg', retries=5):
#     print("query" , query)
#     delay = 1

#     for attempt in range(retries):
#         try:
#             with DDGS() as ddgs:
#                 results = ddgs.images(query, max_results=1)

#                 if not results:
#                     print("No image results found.")
#                     return

#                 image_url = results[0]["image"]
#                 print("Image URL:", image_url)

#                 response = requests.get(image_url, stream=True, timeout=10)
#                 response.raise_for_status()

#                 with open(save_path, 'wb') as out_file:
#                     for chunk in response.iter_content(chunk_size=8192):
#                         out_file.write(chunk)

#                 print(f"Image saved as {save_path}")
#                 return  # Success, so exit the function

#         except exceptions.RatelimitException as e:
#             print(f"Rate limited on attempt {attempt + 1}. Retrying in {delay:.1f}s...")
#             time.sleep(delay + random.uniform(0.5, 1.5))
#             delay *= 2

#         except Exception as e:
#             print(f"Error during attempt {attempt + 1}: {e}")
#             time.sleep(delay + random.uniform(0.5, 1.5))
#             delay *= 2

#     print("Failed to fetch or save image after multiple attempts.")


async def fetch_and_save_first_image(query , save_path = "downloaded_image.jpg"):
    params = {
        "q" : query,
        "tbm" : "isch",
        "api_key" : api_key

    }

    search =  GoogleSearch(params)
    results = search.get_dict()
    images = results.get("images_results" , [])

    for img in images:
        image_url = img.get("original") 

        if image_url and ".jpg" in image_url.lower():
            try:
                response = requests.get(image_url, stream=True, timeout=10)
                response.raise_for_status()
                with open(save_path, 'wb') as f:
                    for chunk in response.iter_content(8192):
                        f.write(chunk)
                print(f"Image downloaded: {image_url}")
                return
            except Exception as e:
                print("Error Download image")
        print("No .jpg image found.")



#     print(images)

#     if images:
#         image_url = images[0]["original"]
#         img_data = requests.get(image_url).content
#         with open(save_path, "wb") as f:
#             f.write(img_data)
#             print("Image downloaded:", image_url)
#     else:
#         print("No image found.")



#  for img in images:
#         image_url = img.get("original")
#         if image_url and ".jpg" in image_url.lower():
#             try:
#                 response = requests.get(image_url, stream=True, timeout=10)
#                 response.raise_for_status()
#                 with open(save_path, 'wb') as f:
#                     for chunk in response.iter_content(8192):
#                         f.write(chunk)
#                 print(f"Image downloaded: {image_url}")
#                 return
#             except Exception as e:
#                 print(f"Error downloading image: {e}")
#                 continue

#     print("No .jpg image found.")