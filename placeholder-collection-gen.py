"""
This script downloads a specified number of images and generates corresponding NFT metadata for each image.
Images are downloaded from a specified URL and saved to a folder.
Metadata is generated with random attributes and saved in the output folder as JSON files.
"""

import json
import os
import random
from io import BytesIO
from pathlib import Path
from time import sleep

import requests
from PIL import Image

from constants import MY_IPFS_FOLDER

NUM_FILES = 520  # Number of metadata JSON files to generate
NUM_ONE_OF_ONE = 10  # How many of them will be labeled as "One of one"
NUM_EDITION = 10  # How many of them will be labeled as "Edition"
OUTPUT_FOLDER = 'data/json-metadata'  # Folder to save metadata JSON files
SEPARATE_TOKEN_TYPES = True  # Whether to save metadata in separate folders for each token type
IPFS_FOLDER = MY_IPFS_FOLDER  # IPFS folder where you uploaded the images (with or without '/')
DOWNLOAD_DIR = 'data/downloaded-images'  # Folder to save downloaded images
IMAGE_BASE_URL = (
    'https://vole.wtf/this-mp-does-not-exist/mp/mp'  # Base URL from which to download images
)


def generate_attributes():
    """
    Generate a list of random attributes for an NFT.

    Returns:
        attributes (list): A list of dictionaries containing attribute name and value.
    """
    possible_attributes = [
        {"name": "Height", "value_range": (150, 210)},
        {"name": "Hair", "value_list": ["Black", "Brown", "Blonde", "Red", "Gray"]},
        {"name": "Age", "value_range": (18, 100)},
        {"name": "Eye Color", "value_list": ["Blue", "Green", "Brown", "Hazel", "Gray"]},
        {
            "name": "Nationality",
            "value_list": ["American", "British", "Canadian", "Australian", "French", "German"],
        },
        {
            "name": "Hobby",
            "value_list": ["Photography", "Painting", "Hiking", "Gaming", "Cooking", "Traveling"],
        },
    ]

    num_attributes = random.randint(0, 2)
    selected_attributes = random.sample(possible_attributes, num_attributes)
    attributes = []

    for attr in selected_attributes:
        attribute = {"name": attr["name"]}
        if "value_range" in attr:
            attribute["value"] = random.randint(attr["value_range"][0], attr["value_range"][1])
        elif "value_list" in attr:
            attribute["value"] = random.choice(attr["value_list"])
        attributes.append(attribute)

    return attributes


def generate_nft_metadata(index):
    """
    Generate NFT metadata for a given index.

    Args:
        index (int): The index of the NFT item.

    Returns:
        metadata (dict): A dictionary containing the NFT metadata.
    """
    token_type = "Folio"

    if index >= NUM_FILES - (NUM_ONE_OF_ONE + NUM_EDITION):
        if index < NUM_FILES - NUM_ONE_OF_ONE:
            token_type = "Edition"
        else:
            token_type = "One of one"

    metadata = {
        "name": f"Fake MP {index}",
        "description": f"This is the item with id {index} in the fake MP collection",
        "image": f"{IPFS_FOLDER.rstrip('/')}/{index}.jpg",
        "token_type": token_type,
        "attributes": generate_attributes(),
    }
    return metadata


def save_metadata_to_file(folder, index, metadata):
    """
    Save the NFT metadata to a JSON file in the specified folder.

    Args:
        folder (str): The folder path to save the metadata file.
        index (int): The index of the NFT item.
        metadata (dict): The NFT metadata dictionary.
    """
    if SEPARATE_TOKEN_TYPES:
        dir = os.path.join(folder, metadata["token_type"])
        Path(dir).mkdir(parents=True, exist_ok=True)
    else:
        dir = folder
    fname = os.path.join(dir, str(index)) # no json extension, to work as token URI
    with open(fname, 'w') as f: 
        json.dump(metadata, f, indent=2)


def download_random_images(ind_start, ind_end, base_url, download_dir):
    """
    Download a range of images from the specified base URL and save them to a folder.

    Args:
        ind_start (int): The starting index of the image range.
        ind_end (int): The ending index of the image range.
        base_url (str): The base URL from which to download images.
        download_dir (str): The folder path to save the downloaded images.
    """
    Path(download_dir).mkdir(parents=True, exist_ok=True)

    err_cnt = 0
    for i in range(ind_start, ind_end):
        try:
            file_name = os.path.join(download_dir, f'{i}.jpg')
            if Path(file_name).exists():
                print(f'File {file_name} exists, skipping.')
                continue
            url = f'{base_url}{str(i):{"0"}>{5}}.jpg'
            print(f'Downloading image {i} from {url}...')
            image_response = requests.get(url)
            image = Image.open(BytesIO(image_response.content))
            image.save(file_name)
            print(f'Successfully downloaded image {i}')
        except Exception as e:
            print(f'Error downloading image {i}: {e}')
            err_cnt += 1
        sleep(0.5)
    print(f'Finished with {err_cnt} errors. Can rerun to try to download missing files.')


def main():
    """
    Main function that coordinates downloading images, generating NFT metadata, and saving metadata to files.
    """
    while True:
        choice = input("Enter 1 to download images, 2 to generate metadata, or q to quit: ")

        if choice == "q":
            break
        if choice == "1":
            # Download images
            download_random_images(0, NUM_FILES, IMAGE_BASE_URL, DOWNLOAD_DIR)
            print(
                "Download complete. Please upload the images to IPFS and update the IPFS_FOLDER constant."
            )
        elif choice == "2":
            # Generate and save metadata
            if not os.path.exists(OUTPUT_FOLDER):
                os.makedirs(OUTPUT_FOLDER)

            for i in range(NUM_FILES):
                metadata = generate_nft_metadata(i)
                save_metadata_to_file(OUTPUT_FOLDER, i, metadata)
            
            print("Metadata generation complete. You can now upload the metadata to IPFS.")


if __name__ == "__main__":
    main()
