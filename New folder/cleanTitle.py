import re
import os

def clean_title(title):
    # 1. Define unwanted words/phrases (Case-Insensitive)
    unwanted_patterns = [
        r'vintage', r'the best', r'\[Available\]', r'Blanket Quilt -', r'Bella Canvas', r'Bella \+ Canvas', r'Bella\+Canvas',
        r'Valentine Blanket Quilt -', r'2D -', r'3D -', r'Fleece', 
        r'Oversized?', r'All-', r'Flag-', r'Doormat-', r'Cap-', 
        r'ZipAroundWallet-', r'BaseballJersey-', r'BaseballJacket-',
        r'pajama(Tshirt|Sweater|s)?(-)?', r'Comfort Colors', r'Bootleg', r'Comfort Colours',
        r'Hoodie Shirts -', r'Long Sleeve', r'Short Sleeve', r'washed(-)?', r'Preorder?'
        , r'Navy?'
    ]
    
    # Combine patterns into one regex
    pattern = re.compile('|'.join(unwanted_patterns), re.IGNORECASE)
    title = pattern.sub('', title)

    # 2. Remove HTML entities like &039 or &8217
    title = re.sub(r'&\s?\d+\s?', '', title)

    # 3. NEW: Specifically remove Chinese Characters
    # This covers the main block of CJK Unified Ideographs
    title = re.sub(r'[\u4e00-\u9fff]+', '', title)

    # 4. Remove ALL special characters
    # Note: This step already removes Chinese characters, 
    # but keeping it ensures only English alphanumeric text remains.
    title = re.sub(r'[^a-zA-Z0-9\s]', '', title)

    # 5. Final Cleanup: Fix double spaces and strip edges
    title = re.sub(r'\s+', ' ', title).strip()
    
    return title

# Example usage:
# old_name = "Vintage (Limited) Blanket Quilt - Awesome Title™ & 039"
# new_name = clean_title(old_name)

root_path = r'D:\signinify6\T-Shirt\1'

for folder_name in os.listdir(root_path):
    old_path = os.path.join(root_path, folder_name)
    
    if os.path.isdir(old_path):
        # 1. Clean the name using the function from before
        new_name_base = clean_title(folder_name)
        new_path = os.path.join(root_path, new_name_base)
        
        # 2. Check for existence and handle conflicts
        counter = 1
        final_name = new_name_base
        final_path = new_path
        
        # While a folder with this name already exists (and it's not the current one)
        while os.path.exists(final_path) and old_path.lower() != final_path.lower():
            final_name = f"{new_name_base}-{counter}"
            final_path = os.path.join(root_path, final_name)
            counter += 1

        # 3. Perform the rename
        try:
            if old_path != final_path:
                os.rename(old_path, final_path)
                print(f"Success: {folder_name} -> {final_name}")
        except OSError as e:
            print(f"Error renaming {folder_name}: {e}")