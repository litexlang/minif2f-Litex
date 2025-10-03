#!/usr/bin/env python3
"""
Script to add a 'lit_completed' column to minif2f.jsonl
This script checks if each problem has a corresponding .lit file in valid_litex_code directory
and adds a boolean field indicating completion status.
"""

import json
import os
import sys
from pathlib import Path

def get_existing_lit_files(valid_litex_code_dir):
    """Get list of existing .lit files (without extension)"""
    lit_files = set()
    if os.path.exists(valid_litex_code_dir):
        for file in os.listdir(valid_litex_code_dir):
            if file.endswith('.lit'):
                lit_files.add(file[:-4])  # Remove .lit extension
    return lit_files

def update_jsonl_with_lit_status(jsonl_file, valid_litex_code_dir, output_file=None):
    """
    Update JSONL file with lit_completed status
    
    Args:
        jsonl_file: Path to input JSONL file
        valid_litex_code_dir: Path to valid_litex_code directory
        output_file: Path to output file (if None, overwrites input file)
    """
    
    # Get existing .lit files
    existing_lit_files = get_existing_lit_files(valid_litex_code_dir)
    print(f"Found {len(existing_lit_files)} existing .lit files")
    
    # Read and process JSONL file
    updated_entries = []
    total_entries = 0
    completed_entries = 0
    
    with open(jsonl_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            if line.strip():
                try:
                    entry = json.loads(line.strip())
                    total_entries += 1
                    
                    # Check if this problem has a corresponding .lit file
                    problem_name = entry.get('name', '')
                    lit_completed = problem_name in existing_lit_files
                    
                    if lit_completed:
                        completed_entries += 1
                    
                    # Add the lit_completed field
                    entry['lit_completed'] = lit_completed
                    updated_entries.append(entry)
                    
                except json.JSONDecodeError as e:
                    print(f"Warning: Invalid JSON on line {line_num}: {e}")
                    continue
    
    # Write updated entries to output file
    output_path = output_file if output_file else jsonl_file
    with open(output_path, 'w', encoding='utf-8') as f:
        for entry in updated_entries:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    
    print(f"Updated {total_entries} entries")
    print(f"Completed: {completed_entries} ({completed_entries/total_entries*100:.1f}%)")
    print(f"Remaining: {total_entries - completed_entries}")
    print(f"Output written to: {output_path}")

def main():
    """Main function"""
    # Default paths
    current_dir = Path(__file__).parent
    jsonl_file = current_dir / "minif2f.jsonl"
    valid_litex_code_dir = current_dir / "valid_litex_code"
    
    # Check if files exist
    if not jsonl_file.exists():
        print(f"Error: {jsonl_file} not found!")
        sys.exit(1)
    
    if not valid_litex_code_dir.exists():
        print(f"Error: {valid_litex_code_dir} not found!")
        sys.exit(1)
    
    # Create backup
    backup_file = jsonl_file.with_suffix('.jsonl.backup')
    print(f"Creating backup: {backup_file}")
    import shutil
    shutil.copy2(jsonl_file, backup_file)
    
    # Update the file
    print("Updating JSONL file with lit_completed status...")
    update_jsonl_with_lit_status(jsonl_file, valid_litex_code_dir)
    
    print("\nDone! You can now manually edit the lit_completed field as needed.")
    print("To restore from backup: cp minif2f.jsonl.backup minif2f.jsonl")

if __name__ == "__main__":
    main()
