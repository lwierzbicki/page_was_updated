import requests
import hashlib
import json

# List of pages to check
def load_pages_to_check(file_path):
    try:
        with open(file_path, 'r') as file:
            pages = [line.strip() for line in file]
        return pages
    except FileNotFoundError:
        return []

# Usage
file_path = "pages_to_check.txt"  # Replace with the actual file path
pages_to_check = load_pages_to_check(file_path)

# Functions to operate on content_hashes file
content_hashes = "stored_data.json"

def load_stored_data(page_url, data_file=content_hashes):
    try:
        with open(data_file, 'r') as file:
            stored_data = json.load(file)
            return stored_data.get(page_url)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def update_stored_data(page_url, new_content, data_file=content_hashes):
    try:
        # Read existing data from the file
        with open(data_file, 'r') as file:
            stored_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        stored_data = {}

    # Calculate the hash of the new content
    new_hash = calculate_hash(new_content)

    # Update or add the data for the given page URL
    #stored_data[page_url] = {"hash": new_hash, "content": new_content}
    stored_data[page_url] = {"hash": new_hash}

    # Write the updated data back to the file
    with open(data_file, 'w') as file:
        json.dump(stored_data, file, indent=4)

def store_initial_data(page_url, initial_content, data_file=content_hashes):
    try:
        # Read existing data from the file
        with open(data_file, 'r') as file:
            stored_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        stored_data = {}

    # Calculate the hash of the initial content
    initial_hash = calculate_hash(initial_content)

    # Update or add the data for the given page URL
    #stored_data[page_url] = {"hash": initial_hash, "content": initial_content}
    stored_data[page_url] = {"hash": initial_hash}

    # Write the updated data back to the file
    with open(data_file, 'w') as file:
        json.dump(stored_data, file, indent=4)

def calculate_hash(content):
    return hashlib.sha256(content.encode()).hexdigest()

for page_url in pages_to_check:
    response = requests.get(page_url)
    if response.status_code == 200:
        current_content = response.text
        # Load stored data from the database or file
        stored_data = load_stored_data(page_url)
        if stored_data is not None:
            stored_hash = stored_data['hash']
            if calculate_hash(current_content) != stored_hash:
                # Page has been updated
                print(f"Page {page_url} has been updated.")
                # Update the stored data with new content and hash
                update_stored_data(page_url, current_content)
        else:
            # First time checking, store the initial data
            store_initial_data(page_url, current_content)

# Store and retrieve data functions will depend on your chosen storage method (database or file).
