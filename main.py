from PIL import Image
import imagehash
import os

def calculate_hash(image_path):
    try:
        img = Image.open(image_path)
        hash = imagehash.dhash(img)
        return hash
    except (OSError, FileNotFoundError):
        print(f"Error: Could not open or process image at {image_path}")
        return None

def find_duplicate_images(directory):
    hashes = {}
    duplicates = {}

    for filename in os.listdir(directory):
        if not filename.lower().endswith(('.png', '.jpg', 'jpeg', 'gif', '.bmp')):
            continue

        image_path = os.path.join(directory, filename)
        hash_value = calculate_hash(image_path)

        if hash_value is not None:
            pass
            if hash_value in hashes:
                if hashes[hash_value] in duplicates:
                    original_image = hashes[hash_value]
                    duplicates[original_image].append(image_path)
                else:
                    duplicates[hashes[hash_value]] = list((hashes[hash_value],image_path))
            else:
                hashes[hash_value] = image_path

    return duplicates

if __name__ == "__main__":
    
    directory_to_scan = "./test_directory"
    duplicates = find_duplicate_images(directory_to_scan)

    if duplicates:
        for value_list in duplicates.values():
            print(value_list)

    else:
        print("No duplicate images found.")