import json
import urllib.request
import urllib.parse
import xml.sax.saxutils as saxutils
from pathlib import Path

# Fetch from the live Node-Notes site instead of a local path!
NODE_NOTES_URL = "https://ayush-mgr.github.io/Node-Notes/graph-data.json"
OUTPUT_SITEMAP = Path("sitemap.xml")

def main():
    urls = []
    
    # 1. Add home page
    urls.append({
        "loc": "https://ayush-mgr.github.io/",
        "priority": "1.0",
        "changefreq": "daily"
    })
    
    # 2. Add Node-Notes index
    urls.append({
        "loc": "https://ayush-mgr.github.io/Node-Notes/",
        "priority": "0.9",
        "changefreq": "daily"
    })
    
    # 3. Fetch graph-data.json from the live site
    print(f"Fetching from {NODE_NOTES_URL}...")
    try:
        req = urllib.request.Request(NODE_NOTES_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            
        nodes = data.get("nodes", [])
        note_count = 0
        for node in nodes:
            # Filter out ghost nodes and assets
            if node.get("ghost") or node.get("id", "").startswith("Assets"):
                continue
            
            note_id = node.get("id")
            if not note_id:
                continue
                
            encoded_id = urllib.parse.quote(note_id, safe='')
            note_url = f"https://ayush-mgr.github.io/Node-Notes/#note={encoded_id}"
            
            urls.append({
                "loc": note_url,
                "priority": "0.7",
                "changefreq": "weekly"
            })
            note_count += 1
            
        print(f"Processed {note_count} individual notes.")
    except Exception as e:
        print(f"Failed to fetch or parse graph-data.json: {e}")
        return

    # Generate XML
    xml_content = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml_content.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    
    for url in urls:
        escaped_loc = saxutils.escape(url["loc"])
        xml_content.append('  <url>')
        xml_content.append(f'    <loc>{escaped_loc}</loc>')
        xml_content.append(f'    <changefreq>{url["changefreq"]}</changefreq>')
        xml_content.append(f'    <priority>{url["priority"]}</priority>')
        xml_content.append('  </url>')
        
    xml_content.append('</urlset>')
    
    # Write to sitemap.xml
    OUTPUT_SITEMAP.write_text("\n".join(xml_content), encoding="utf-8")
    print(f"Successfully generated {OUTPUT_SITEMAP} with {len(urls)} URLs.")

if __name__ == "__main__":
    main()
