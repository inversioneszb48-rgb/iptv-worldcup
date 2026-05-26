import requests
from pathlib import Path

input_file = 'output/merged.m3u'
output_file = 'output/working.m3u'

with open(input_file, encoding='utf-8') as f:
    lines = f.read().splitlines()

working = ['#EXTM3U']

for i, line in enumerate(lines):
    if line.startswith('http'):
        try:
            response = requests.get(line, timeout=8, stream=True)
            if response.status_code == 200:
                if i > 0:
                    working.append(lines[i-1])
                working.append(line)
                print(f'LIVE: {line}')
        except:
            print(f'DEAD: {line}')

Path('output').mkdir(exist_ok=True)

with open(output_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(working))

print('Working playlist generated.')
