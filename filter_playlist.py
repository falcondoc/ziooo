import json
import os
import re

WATERMARKS = ["𝗟ɪᴛᴛʟᴇ 𝗖ᴏᴅʀ", "ZioSt", "Fu£ked"]

def load_blocked_channels():
    if os.path.exists("blocked.json"):
        try:
            with open("blocked.json", "r", encoding="utf-8") as f:
                return [ch.strip().lower() for ch in json.load(f)]
        except Exception as e:
            print(f"[-] Error reading blocked.json: {e}")
    return []

def clean_and_filter():
    input_file = "temp_raw.m3u"
    output_file = "Zio.m3u"
    blocked_channels = load_blocked_channels()

    print(f"[+] Loaded {len(blocked_channels)} blocked channels from blocked.json")

    if not os.path.exists(input_file):
        print(f"[-] File {input_file} not found!")
        return

    with open(input_file, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # Scrub watermark lines
    for wm in WATERMARKS:
        content = re.sub(rf".*{re.escape(wm)}.*?\n", "", content)

    lines = content.splitlines()
    header_lines = []
    channels = []
    current_block = []

    for line in lines:
        if line.startswith("#EXTM3U"):
            header_lines.append(line)
        elif line.startswith("#EXTINF"):
            if current_block:
                channels.append(current_block)
            current_block = [line]
        elif current_block:
            current_block.append(line)
        elif line.strip() and not line.startswith("#EXTINF"):
            header_lines.append(line)

    if current_block:
        channels.append(current_block)

    filtered_channels = []
    for block in channels:
        extinf = block[0]
        ch_name = extinf.split(",")[-1].strip() if "," in extinf else ""

        # Check against blocked list (case-insensitive)
        if any(b in ch_name.lower() for b in blocked_channels):
            print(f"[-] Dropped channel: {ch_name}")
            continue

        filtered_channels.append(block)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(header_lines) + "\n\n")
        for block in filtered_channels:
            f.write("\n".join(block) + "\n\n")

    print(f"[✓] Successfully generated {output_file} with {len(filtered_channels)} channels.")

if __name__ == "__main__":
    clean_and_filter()
