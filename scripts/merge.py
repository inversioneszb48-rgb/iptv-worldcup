import requests
from pathlib import Path

urls = [
    'https://iptv-org.github.io/iptv/categories/sports.m3u',
    'https://iptv-org.github.io/iptv/countries/pe.m3u',
    'https://iptv-org.github.io/iptv/languages/spa.m3u'
]

output = '#EXTM3U\n'

for url in urls:
    try:
        data = requests.get(url, timeout=15).text
        output += data + '\n'
        print(f'OK: {url}')
    except Exception as e:
        print(f'ERROR: {url} -> {e}')

Path('output').mkdir(exist_ok=True)

with open('output/merged.m3u', 'w', encoding='utf-8') as f:
    f.write(output)

print('Merged playlist created.')
