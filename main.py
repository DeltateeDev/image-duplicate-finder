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

def find_duplicate_images(directory, threshold = 5):
    hashes = {}
    duplicates = []

    for filename in os.listdir(directory):
        if not filename.lower().endswith(('.png', '.jpg', 'jpeg', 'gif', '.bmp')):
            continue

        image_path = os.path.join(directory, filename)
        hash_value = calculate_hash(image_path)
        duplicate_found = False #a flag for not overwriting the existing file paths in hashes dictionary

        if hash_value is not None:
            if not hashes:
                hashes[hash_value] = image_path
                continue
            for existing_hash, existing_image_path in list(hashes.items()):

                if (existing_hash - hash_value) < threshold:
                    duplicate_found = True
                    duplicates.append({'Duplicate File': image_path, 'Original File': existing_image_path, 'Difference Score': (existing_hash - hash_value)})

            if not duplicate_found:
                hashes[hash_value] = image_path

    return duplicates

if __name__ == "__main__":
    
    directory_to_scan = "./test_directory"
    duplicates = find_duplicate_images(directory_to_scan)

    if duplicates:
        # for value_list in duplicates.values():
        #     print(value_list)
        for i in duplicates:
            print(i)

    else:
        print("No duplicate images found.")