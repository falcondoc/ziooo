import json
import os
import requests

# 1. Define your channels list
CHANNELS = [
    {
        "name": "DD National",
        "id": "dd_national",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/8/81/Doordarshan_logo.svg",
        "group": "National",
        "url": "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8",
        "user_agent": "Mozilla/5.0"
    },
    {
        "name": "Live News Feed",
        "id": "live_news",
        "logo": "https://placehold.co/200x200/png?text=News",
        "group": "News",
        "url": "https://devstreaming-cdn.apple.com/videos/streaming/examples/bipbop_4x3/bipbop_4x3_variant.m3u8",
        "user_agent": "Mozilla/5.0"
    },
    {
        "name": "ClearKey DRM Stream Example",
        "id": "sports_hd",
        "logo": "https://placehold.co/200x200/png?text=Sports",
        "group": "Sports",
        "url": "https://dash.akamaized.net/dash264/TestCases/1c/qualcomm/1/MultiRate.mpd",
        "user_agent": "Mozilla/5.0",
        "key_id": "10000000100010001000100000000001",
        "key": "000102030405060708090a0b0c0d0e0f"
    }
]

def generate_playlist():
    playlist_content = '#EXTM3U x-tvg-url="https://raw.githubusercontent.com/username/epg/main/epg.xml.gz"\n\n'

    for ch in CHANNELS:
        # Build the standard #EXTINF metadata tag
        playlist_content += f'#EXTINF:-1 tvg-id="{ch["id"]}" tvg-name="{ch["name"]}" tvg-logo="{ch["logo"]}" group-title="{ch["group"]}",{ch["name"]}\n'
        
        # Add User-Agent headers if required
        if ch.get("user_agent"):
            playlist_content += f'#EXTVLCOPT:http-user-agent={ch["user_agent"]}\n'
            playlist_content += f'#EXTHTTP:{{"User-Agent":"{ch["user_agent"]}"}}\n'
        
        # Add ClearKey / Kodi DRM parameters if DRM keys exist
        if ch.get("key_id") and ch.get("key"):
            playlist_content += '#KODIPROP:inputstream.adaptive.manifest_type=mpd\n'
            playlist_content += '#KODIPROP:inputstream.adaptive.license_type=clearkey\n'
            playlist_content += f'#KODIPROP:inputstream.adaptive.license_key={ch["key_id"]}:{ch["key"]}\n'
            
        # Add the media stream link
        playlist_content += f'{ch["url"]}\n\n'

    # Save to playlist.m3u
    with open("playlist.m3u", "w", encoding="utf-8") as file:
        file.write(playlist_content)

    print("SUCCESS: playlist.m3u generated successfully!")

if __name__ == "__main__":
    generate_playlist()
