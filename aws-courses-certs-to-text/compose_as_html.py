import os
import shutil
from datetime import datetime

# Settings
OUTPUT_DIR = 'output'
TARGET_IMG_DIR = 'to-certs-html'
HTML_OUTPUT_FILE = 'certs.html'
CERT_PROVIDER = 'aws'
used_date_ids = {}
html_blocks = []  # Store (date_obj, html_block)

os.makedirs(TARGET_IMG_DIR, exist_ok=True)

def sanitize_filename(text):
    return ''.join(c if c.isalnum() or c in ('-', '_') else '_' for c in text)

def read_txt_and_extract_data(folder_path):
    txt_file_path = os.path.join(folder_path, 'page_1.txt')
    png_file_path = None

    # Find first .png file in the folder
    for fname in os.listdir(folder_path):
        if fname.lower().endswith('.png'):
            png_file_path = os.path.join(folder_path, fname)
            break

    if not os.path.exists(txt_file_path) or not png_file_path:
        print(f"❌ Missing text or png file in: {folder_path}")
        return

    with open(txt_file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    text_blocks = [block.replace('\n', ' ').strip() for block in text.split('\n\n') if block.strip()]

    # Extract course name
    if len(text_blocks) >= 5:
        course_name = text_blocks[4]
    elif len(text_blocks) >= 3:
        fallback_block = text_blocks[2]
        keyword = "successfully completed "
        if keyword in fallback_block:
            course_name = fallback_block.split(keyword, 1)[-1].strip()
        else:
            course_name = "[Unable to extract course name]"
    else:
        course_name = "[Not enough text blocks]"

    # Extract and convert date
    raw_date = text_blocks[-1] if text_blocks else "[No content]"

    try:
        date_obj = datetime.strptime(raw_date, "%m/%d/%Y")
        date_yyyymmdd = date_obj.strftime("%Y%m%d")
        date_yyyy_mm_dd = date_obj.strftime("%Y-%m-%d")

        # Handle duplication
        if date_yyyymmdd not in used_date_ids:
            used_date_ids[date_yyyymmdd] = 0
            date_id = date_yyyymmdd
        else:
            used_date_ids[date_yyyymmdd] += 1
            suffix = used_date_ids[date_yyyymmdd]
            date_id = f"{date_yyyymmdd}-{suffix}"

    except ValueError:
        print(f"⚠️ Invalid date in {folder_path}")
        return

    # Final file name and copy PNG
    final_png_name = f"{date_id}-{CERT_PROVIDER}.png"
    target_path = os.path.join(TARGET_IMG_DIR, final_png_name)
    shutil.copy(png_file_path, target_path)

    # HTML block
    block = f"""
    <div class="cert-item">
        <label class="tag {CERT_PROVIDER}">{CERT_PROVIDER.upper()}</label>
        <label class="title">{course_name}</label>
        <label class="date">{date_yyyy_mm_dd}</label>
        &emsp;
        <a class="image" href="javascript:void(0)"
           onclick="showImage('./assets/certs/{CERT_PROVIDER}/{final_png_name}');">
            <img src="./assets/icon/image.svg" width="70%"/>
        </a>
    </div>
    """
    html_blocks.append((date_obj, block.strip()))
    print(f"✅ Processed: {course_name} [{date_id}]")


def main():
    for folder_name in os.listdir(OUTPUT_DIR):
        folder_path = os.path.join(OUTPUT_DIR, folder_name)
        if os.path.isdir(folder_path):
            read_txt_and_extract_data(folder_path)

    # Sort by date descending (最新的在上面)
    html_blocks.sort(key=lambda x: x[0], reverse=True)

    # Write to HTML
    with open(HTML_OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("\n\n".join(block for _, block in html_blocks))

    print(f"\n✅ HTML generated: {HTML_OUTPUT_FILE}")
    print(f"✅ PNG files copied to: {TARGET_IMG_DIR}")


if __name__ == '__main__':
    main()
