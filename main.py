from PIL import Image
import imagehash
import os
import concurrent.futures

def calculate_hash(image_path):
    try:
        img = Image.open(image_path)
        hash = imagehash.dhash(img)
        img.close()
        return hash
    except (OSError, FileNotFoundError) as e:
        print(f"Error: Could not open or process image at {image_path}: {e}")
        return None

def find_duplicate_images(directory, threshold = 5):
    image_paths = []
    hashes = {}
    duplicates = []

    for filename in os.listdir(directory):
        if filename.lower().endswith(('.png', '.jpg', 'jpeg', 'gif', '.bmp')):
            image_paths.append(os.path.join(directory, filename))
    
    usable_cpu = max(1, os.cpu_count() - 2)

    with concurrent.futures.ProcessPoolExecutor(max_workers=usable_cpu) as executor:
        hash_results = list(executor.map(calculate_hash, image_paths))

    for i, image_path in enumerate(image_paths):
        hash_value = hash_results[i]
        print(i)

        if hash_value is None:
                continue
        
        for existing_hash, existing_image_path in list(hashes.items()):
            if (existing_hash - hash_value) < threshold:
                duplicates.append({
                    'Duplicate File': image_path, 
                    'Original File': existing_image_path, 
                    'Difference Score': (existing_hash - hash_value)
                })
                break

        hashes[hash_value] = image_path

    return duplicates

if __name__ == "__main__":
    
    directory_to_scan = "./test_directory"
    duplicates = find_duplicate_images(directory_to_scan)

    if duplicates:
        for i in duplicates:
            print(i)

    else:
        print("No duplicate images found.")