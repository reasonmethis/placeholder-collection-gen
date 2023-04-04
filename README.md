# Placeholder NFT Collection Generator

This Python script downloads a specified number of images and generates corresponding NFT metadata for each image. Images are downloaded from a specified URL and saved to a folder. Metadata is generated with random attributes and saved in the output folder as JSON files.

## Features

- Downloads images from a URL and saves them to a folder
- Generates NFT metadata with random attributes
- Saves metadata as JSON files in the specified output folder

## Requirements

- Python 3.6 or higher
- `requests` library
- `PIL` (Python Imaging Library)

## Installation

1. Clone the repository:

```
git clone https://github.com/yourusername/nft-metadata-generator.git
cd nft-metadata-generator
```

2. Install the required libraries:

```
pip install -r requirements.txt
```

## Usage

1. Update the constants at the beginning of the `nft_metadata_generator.py` script as needed:

```
NUM_FILES = 10
NUM_ONE_OF_ONE = 2
NUM_EDITION = 3
OUTPUT_FOLDER = "output"
IPFS_FOLDER = "some_constant"
IMAGE_BASE_URL = `https://vole.wtf/this-mp-does-not-exist/mp/mp`
DOWNLOAD_DIR = `data/downloaded_images`
```

2. Run the script:

```
python nft_metadata_generator.py
```

The script will download the images and generate NFT metadata with random attributes. Metadata JSON files will be saved in the specified output folder.


