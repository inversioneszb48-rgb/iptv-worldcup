import requests
from pathlib import Path

sources = [
    'https://iptv-org.github.io/iptv/categories/sports.m3u',
    'https://iptv-org.github.io/iptv/countries/pe.m3u',
    'https://iptv-org.github.io/iptv/languages/spa.m3u'
]

custom_file = 'custom_channels.m3u'

Path('output').mkdir(exist_ok=True)

entries = []
seen = set()

for url in sources:
    try:
        data = requests.get(url, timeout=15).text.splitlines()
        print(f'OK: {url}')

        for i, line in enumerate(data):
            if line.startswith('http'):
                stream = line.strip()
                info = data[i - 1] if i > 0 else ''

                if stream not in seen:
                    seen.add(stream)
                    entries.append((info, stream))

    except Exception as e:
        print(f'ERROR: {url} -> {e}')

if Path(custom_file).exists():
    custom_data = Path(custom_file).read_text(encoding='utf-8').splitlines()

    for i, line in enumerate(custom_data):
        if line.startswith('http'):
            stream = line.strip()
            info = custom_data[i - 1] if i > 0 else ''

            if stream not in seen:
                seen.add(stream)
                entries.append((info, stream))

output = ['#EXTM3U']

priority = ['Sports', 'Deportes', 'Peru', 'Perú', 'LATAM']

entries.sort(key=lambda x: any(p.lower() in x[0].lower() for p in priority), reverse=True)

for info, stream in entries:
    output.append(info)
    output.append(stream)

with open('output/merged.m3u', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))

print('Merged playlist created successfully.')
