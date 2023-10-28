import requests
import json
import os
import re  # Importing re to clean the string of html tags
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Configuration
ANKI_CONNECT_URL = "http://localhost:8765"
ANKI_MEDIA_FOLDER = os.getenv("ANKI_MEDIA_FOLDER")  # Path to Anki media folder
DECK_NAME = os.getenv("DECK_NAME")  # Anki deck name
IMAGE_FIELD_NAME = os.getenv("IMAGE_FIELD_NAME")  # Name of the field to add the image to
SEARCH_INPUT_FIELD_NAME = os.getenv("SEARCH_INPUT_FIELD_NAME")  # Name of the field to search for the image

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")  # Google API Key
CX = os.getenv("CX")  # Custom Search Engine ID

def invoke(action, params):
    request = {
        "action": action,
        "params": params,
        "version": 6
    }
    response = requests.post(ANKI_CONNECT_URL, json=request)
    if response.status_code != 200:
        raise Exception(f"Received non-200 response from AnkiConnect: {response.status_code}")
    return response.json()

# cleans a string of html tags such as li, div, etc
def clean_string_of_html_tags(string):
    # remove all html tags
    no_opening = re.sub(r'<[^<]+?>', ';', string)
    clean = re.sub(r';+', ',', no_opening)

    # remove affix and suffix if = ","
    if clean[0] == ",":
        clean = clean[1:]
    if clean[-1] == ",":
        clean = clean[:-1]

    # take MAX first 3 words
    length = len(clean.split(","))
    if length > 2:
        clean = ','.join(clean.split(",")[:2])
    return clean


def fetch_image_url(query):
    print(f"Searching for image: {query}")
    params = {
        "q": query,
        "searchType": "image",
        "key": GOOGLE_API_KEY,
        "cx": CX,
        "num": 1,  # Number of images to return. Set to 1 to get the first image.
        "fileType": "jpg"
    }
    response = requests.get("https://www.googleapis.com/customsearch/v1", params=params)
    if response.status_code != 200:
        raise Exception(f"Received non-200 response from Google Custom Search API: {response.status_code}")
    data = response.json()
    if "items" not in data or not data["items"]:
        print(f"No images found for query: {query}")
        return None
    return data["items"][0]["link"]

def add_image_to_card(card_id, image_url):
    # Download the image
    image_data = requests.get(image_url).content
    image_filename = f"{card_id}.jpg"
    
    # Save the image to the Anki media folder
    filepath = os.path.join(ANKI_MEDIA_FOLDER, image_filename)
    print(f"Saving image to {filepath}")

    # override existing file:
    with open(filepath, 'wb') as f:
        f.write(image_data)


    # Update the Anki card to reference the image by its filename
    field_data = f'<img src="{image_filename}">'
    params = {
        "note": {
            "id": card_id,
            "fields": {IMAGE_FIELD_NAME: field_data}
        }
    }
    invoke("updateNoteFields", params)
    print(f"Added image to card {card_id}")

def main():
    query = f'deck:"{DECK_NAME}"'
    params = {"query": query}
    response = invoke("findNotes", params)
    card_ids = response.get("result")
    
    if card_ids is None:
        print(f"Error: Could not retrieve cards for query: {query}")
        return
    
    params = {"notes": card_ids}
    response = invoke("notesInfo", params)
    note_infos = response.get("result", [])
    
    for note_info in note_infos:
        card_id = note_info.get("noteId")

        fields = note_info.get("fields", {})
        search_input_content = fields.get(SEARCH_INPUT_FIELD_NAME, {}).get("value", "")
        image_field_content = fields.get(IMAGE_FIELD_NAME, {}).get("value", "")
        
        if not search_input_content:
            print(f"Card {card_id} skipped: search input field is empty")
            continue
        
        if image_field_content:
            print(f"Card {card_id} skipped: image field already populated")
            continue

        image_url = fetch_image_url(clean_string_of_html_tags(search_input_content))
        if image_url:
            add_image_to_card(card_id, image_url)

if __name__ == "__main__":
    main()
