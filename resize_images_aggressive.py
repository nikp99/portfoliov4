from PIL import Image
import os

def resize_image(filepath, max_width=1080):
    try:
        img = Image.open(filepath)
        original_size = os.path.getsize(filepath)
        
        # Calculate new dimensions
        if img.width > max_width:
            ratio = max_width / img.width
            new_height = int(img.height * ratio)
            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
        
        # Convert RGBA to RGB for JPEGs (if PNG has transparency, keep as PNG)
        if filepath.lower().endswith(('.jpg', '.jpeg')) and img.mode == 'RGBA':
            img = img.convert('RGB')
        
        # Aggressive compression
        if filepath.lower().endswith('.png'):
            # Convert large PNGs to JPEG if no transparency
            if img.mode != 'RGBA' and original_size > 500000:  # 500KB
                new_filepath = filepath.rsplit('.', 1)[0] + '.jpg'
                img.convert('RGB').save(new_filepath, 'JPEG', quality=80, optimize=True)
                os.remove(filepath)
                print(f'Converted {filepath} to JPEG: {original_size/1024:.1f}KB -> {os.path.getsize(new_filepath)/1024:.1f}KB')
            else:
                img.save(filepath, 'PNG', optimize=True, compress_level=9)
                new_size = os.path.getsize(filepath)
                print(f'Optimized {filepath}: {original_size/1024:.1f}KB -> {new_size/1024:.1f}KB')
        else:
            # JPEG with quality 75 (was 85)
            img.save(filepath, 'JPEG', quality=75, optimize=True)
            new_size = os.path.getsize(filepath)
            print(f'Compressed {filepath}: {original_size/1024:.1f}KB -> {new_size/1024:.1f}KB')
        
    except Exception as e:
        print(f'Error processing {filepath}: {e}')

# Process all images
for root, dirs, files in os.walk('.'):
    if '.git' in root:
        continue
    
    for file in files:
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            filepath = os.path.join(root, file)
            resize_image(filepath)
