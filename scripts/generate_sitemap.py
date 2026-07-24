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
    
    # Note: We do not include SPA hash fragment URLs (#note=...) because search engines (like Google)
    # ignore fragment identifiers and treat them all as the base URL https://ayush-mgr.github.io/Node-Notes/.


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
