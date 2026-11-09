"""Check repository-relative links, binary assets and released workbook integrity."""
from pathlib import Path
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
import zipfile

ROOT=Path(__file__).resolve().parents[1]
NS={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
errors=[]
for p in ROOT.rglob('*.md'):
    for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
        if target.startswith(('http:','https:','#','mailto:')):continue
        path=target.split('#')[0]
        if path and not (p.parent/path).exists():errors.append(f'Broken link: {p.relative_to(ROOT)} -> {target}')
for p in (ROOT/'assets').glob('*.png'):
    if p.stat().st_size<32 or p.read_bytes()[:8]!=b'\x89PNG\r\n\x1a\n':errors.append(f'Invalid PNG: {p.name}')
for p in ROOT.rglob('*.pdf'):
    if not p.read_bytes().startswith(b'%PDF-'):errors.append(f'Invalid PDF: {p.name}')
checksums=json.loads((ROOT/'docs/workbook_checksums.json').read_text())
for p in (ROOT/'workbooks').glob('*.xlsx'):
    digest=hashlib.sha256(p.read_bytes()).hexdigest()
    if checksums.get(p.name)!=digest:errors.append(f'Checksum mismatch: {p.name}')
    try:
        with zipfile.ZipFile(p) as z:
            for name in z.namelist():
                if not name.endswith('.xml'):continue
                root=ET.fromstring(z.read(name))
                for cell in root.findall('.//s:c[@t="e"]',NS):
                    errors.append(f'Cached error: {p.name} {name} {cell.get("r")}')
                for t in root.itertext():
                    if 'IMPORTRANGE(' in t:errors.append(f'External import remains: {p.name}')
                    if re.search('[\u0400-\u04ff]',t):errors.append(f'Non-English legacy text: {p.name}')
    except zipfile.BadZipFile:errors.append(f'Invalid XLSX: {p.name}')
if errors:
    print('\n'.join(errors));sys.exit(1)
print('PASS: relative links, PNG/PDF signatures, workbook checksums, cached errors, import removal and legacy-language scan.')
