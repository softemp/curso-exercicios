import os
import re
from pathlib import Path

def get_all_md_files(root_dir):
    md_files = {}
    for path in Path(root_dir).rglob('*.md'):
        if '.git' in path.parts or '.obsidian' in path.parts:
            continue
        rel_path = path.relative_to(root_dir)
        name = path.stem
        md_files[name] = str(rel_path.with_suffix(''))
        md_files[str(rel_path.with_suffix(''))] = str(rel_path.with_suffix(''))
    return md_files

def find_links_in_file(file_path):
    links = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            matches = re.findall(r'\[\[(.*?)\]\]', content)
            for match in matches:
                link = match.split('|')[0]
                links.append(link)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return links

def main():
    root = os.getcwd()
    md_files = get_all_md_files(root)
    
    # 1. Broken Links
    broken_links = []
    orphans = set(md_files.values())
    
    # Exclude non-orphans by default
    if '30_Atlas/Index' in orphans: orphans.remove('30_Atlas/Index')
    if 'README' in orphans: orphans.remove('README')
    if '50_System/WIKI_SCHEMA' in orphans: orphans.remove('50_System/WIKI_SCHEMA')

    for path in Path(root).rglob('*.md'):
        if '.git' in path.parts or '.obsidian' in path.parts:
            continue
        
        file_links = find_links_in_file(path)
        for link in file_links:
            if link not in md_files:
                broken_links.append((str(path.relative_to(root)), link))
            else:
                target = md_files[link]
                if target in orphans:
                    orphans.remove(target)

    # 2. Coverage Check (Index.md or any MOC_*.md)
    mocs = [p for p in md_files.values() if p.startswith('30_Atlas/MOC_') or p == '30_Atlas/Index']
    covered_links = set()
    for moc_path_str in mocs:
        full_moc_path = Path(root) / (moc_path_str + '.md')
        links = find_links_in_file(full_moc_path)
        for l in links:
            if l in md_files:
                covered_links.add(md_files[l])
    
    missing_from_atlas = []
    for name, path_str in md_files.items():
        if path_str.startswith('10_Neurons/') and path_str not in covered_links:
            if path_str not in missing_from_atlas:
                missing_from_atlas.append(path_str)

    print("--- BROKEN LINKS ---")
    if not broken_links: print("None")
    for file, link in broken_links:
        print(f"{file} -> [[{link}]]")
    
    print("\n--- MISSING FROM ATLAS (Index or MOCs) ---")
    if not missing_from_atlas: print("None")
    for missing in sorted(missing_from_atlas):
        print(missing)

    print("\n--- ORPHAN PAGES (Not linked by any other page) ---")
    filtered_orphans = [o for o in orphans if o.startswith('10_Neurons/') or o.startswith('20_Projects/')]
    if not filtered_orphans: print("None")
    for orphan in sorted(filtered_orphans):
        print(orphan)

if __name__ == "__main__":
    main()
