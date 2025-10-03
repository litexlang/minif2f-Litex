#!/usr/bin/env python3
"""
Quick script to update lit_completed status in minif2f.jsonl
Usage: python3 quick_update.py
"""

import json
import os
from pathlib import Path

def quick_update():
    """Quickly update the JSONL file with current .lit file status"""
    
    # Paths
    jsonl_file = Path("minif2f.jsonl")
    valid_litex_code_dir = Path("valid_litex_code")
    
    if not jsonl_file.exists():
        print("Error: minif2f.jsonl not found!")
        return
    
    if not valid_litex_code_dir.exists():
        print("Error: valid_litex_code directory not found!")
        return
    
    # Get existing .lit files
    existing_lit_files = set()
    for file in valid_litex_code_dir.iterdir():
        if file.suffix == '.lit':
            existing_lit_files.add(file.stem)
    
    print(f"Found {len(existing_lit_files)} .lit files")
    
    # Read and update JSONL
    entries = []
    updated_count = 0
    completed_count = 0
    
    with open(jsonl_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                entry = json.loads(line.strip())
                name = entry.get('name', '')
                old_status = entry.get('lit_completed', False)
                new_status = name in existing_lit_files
                
                if old_status != new_status:
                    entry['lit_completed'] = new_status
                    updated_count += 1
                
                if new_status:
                    completed_count += 1
                
                entries.append(entry)
    
    # Write back to file
    with open(jsonl_file, 'w', encoding='utf-8') as f:
        for entry in entries:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    
    print(f"Updated {updated_count} entries")
    print(f"Total completed: {completed_count}/{len(entries)} ({completed_count/len(entries)*100:.1f}%)")
    print("Done!")

if __name__ == "__main__":
    quick_update()
