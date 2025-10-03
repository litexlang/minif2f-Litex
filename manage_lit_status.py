#!/usr/bin/env python3
"""
Advanced script to manage lit_completed status in minif2f.jsonl
This script provides various utilities for tracking and updating completion status.
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Set

class LitStatusManager:
    def __init__(self, jsonl_file: str, valid_litex_code_dir: str):
        self.jsonl_file = Path(jsonl_file)
        self.valid_litex_code_dir = Path(valid_litex_code_dir)
        self.entries = []
        self.load_entries()
    
    def load_entries(self):
        """Load all entries from JSONL file"""
        self.entries = []
        with open(self.jsonl_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    self.entries.append(json.loads(line.strip()))
    
    def get_existing_lit_files(self) -> Set[str]:
        """Get set of existing .lit files (without extension)"""
        lit_files = set()
        if self.valid_litex_code_dir.exists():
            for file in self.valid_litex_code_dir.iterdir():
                if file.suffix == '.lit':
                    lit_files.add(file.stem)  # filename without extension
        return lit_files
    
    def update_status_from_files(self):
        """Update lit_completed status based on existing .lit files"""
        existing_files = self.get_existing_lit_files()
        updated_count = 0
        
        for entry in self.entries:
            name = entry.get('name', '')
            old_status = entry.get('lit_completed', False)
            new_status = name in existing_files
            
            if old_status != new_status:
                entry['lit_completed'] = new_status
                updated_count += 1
        
        return updated_count
    
    def save_entries(self):
        """Save all entries back to JSONL file"""
        with open(self.jsonl_file, 'w', encoding='utf-8') as f:
            for entry in self.entries:
                f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    
    def get_stats(self) -> Dict:
        """Get completion statistics"""
        total = len(self.entries)
        completed = sum(1 for entry in self.entries if entry.get('lit_completed', False))
        remaining = total - completed
        
        return {
            'total': total,
            'completed': completed,
            'remaining': remaining,
            'completion_rate': completed / total * 100 if total > 0 else 0
        }
    
    def list_completed(self) -> List[str]:
        """Get list of completed problem names"""
        return [entry['name'] for entry in self.entries if entry.get('lit_completed', False)]
    
    def list_remaining(self) -> List[str]:
        """Get list of remaining problem names"""
        return [entry['name'] for entry in self.entries if not entry.get('lit_completed', False)]
    
    def mark_completed(self, problem_names: List[str]):
        """Mark specific problems as completed"""
        updated_count = 0
        for entry in self.entries:
            if entry['name'] in problem_names:
                if not entry.get('lit_completed', False):
                    entry['lit_completed'] = True
                    updated_count += 1
        return updated_count
    
    def mark_incomplete(self, problem_names: List[str]):
        """Mark specific problems as incomplete"""
        updated_count = 0
        for entry in self.entries:
            if entry['name'] in problem_names:
                if entry.get('lit_completed', False):
                    entry['lit_completed'] = False
                    updated_count += 1
        return updated_count
    
    def search_problems(self, query: str) -> List[Dict]:
        """Search for problems by name or informal statement"""
        query_lower = query.lower()
        results = []
        
        for entry in self.entries:
            name = entry.get('name', '').lower()
            informal = entry.get('informal_prefix', '').lower()
            
            if query_lower in name or query_lower in informal:
                results.append(entry)
        
        return results
    
    def export_completion_report(self, output_file: str):
        """Export a detailed completion report"""
        stats = self.get_stats()
        completed = self.list_completed()
        remaining = self.list_remaining()
        
        report = {
            'summary': stats,
            'completed_problems': completed,
            'remaining_problems': remaining,
            'completion_rate_by_category': self._get_completion_by_category()
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return report
    
    def _get_completion_by_category(self) -> Dict:
        """Get completion rate by problem category"""
        categories = {}
        
        for entry in self.entries:
            name = entry.get('name', '')
            completed = entry.get('lit_completed', False)
            
            # Extract category from name (e.g., 'mathd_algebra' from 'mathd_algebra_182')
            if '_' in name:
                category = '_'.join(name.split('_')[:-1])
            else:
                category = 'other'
            
            if category not in categories:
                categories[category] = {'total': 0, 'completed': 0}
            
            categories[category]['total'] += 1
            if completed:
                categories[category]['completed'] += 1
        
        # Calculate completion rates
        for category in categories:
            total = categories[category]['total']
            completed = categories[category]['completed']
            categories[category]['completion_rate'] = completed / total * 100 if total > 0 else 0
        
        return categories

def main():
    """Main function with interactive menu"""
    manager = LitStatusManager("minif2f.jsonl", "valid_litex_code")
    
    while True:
        print("\n" + "="*50)
        print("Minif2f Litex Status Manager")
        print("="*50)
        
        stats = manager.get_stats()
        print(f"Total problems: {stats['total']}")
        print(f"Completed: {stats['completed']} ({stats['completion_rate']:.1f}%)")
        print(f"Remaining: {stats['remaining']}")
        
        print("\nOptions:")
        print("1. Update status from existing .lit files")
        print("2. Mark specific problems as completed")
        print("3. Mark specific problems as incomplete")
        print("4. Search problems")
        print("5. Show completed problems")
        print("6. Show remaining problems")
        print("7. Export completion report")
        print("8. Save and exit")
        print("9. Exit without saving")
        
        choice = input("\nEnter your choice (1-9): ").strip()
        
        if choice == '1':
            updated = manager.update_status_from_files()
            print(f"Updated {updated} entries based on existing .lit files")
        
        elif choice == '2':
            names = input("Enter problem names (comma-separated): ").strip().split(',')
            names = [name.strip() for name in names if name.strip()]
            updated = manager.mark_completed(names)
            print(f"Marked {updated} problems as completed")
        
        elif choice == '3':
            names = input("Enter problem names (comma-separated): ").strip().split(',')
            names = [name.strip() for name in names if name.strip()]
            updated = manager.mark_incomplete(names)
            print(f"Marked {updated} problems as incomplete")
        
        elif choice == '4':
            query = input("Enter search query: ").strip()
            results = manager.search_problems(query)
            print(f"Found {len(results)} matching problems:")
            for entry in results[:10]:  # Show first 10
                status = "✓" if entry.get('lit_completed', False) else "✗"
                print(f"  {status} {entry['name']}")
            if len(results) > 10:
                print(f"  ... and {len(results) - 10} more")
        
        elif choice == '5':
            completed = manager.list_completed()
            print(f"Completed problems ({len(completed)}):")
            for name in completed[:20]:  # Show first 20
                print(f"  ✓ {name}")
            if len(completed) > 20:
                print(f"  ... and {len(completed) - 20} more")
        
        elif choice == '6':
            remaining = manager.list_remaining()
            print(f"Remaining problems ({len(remaining)}):")
            for name in remaining[:20]:  # Show first 20
                print(f"  ✗ {name}")
            if len(remaining) > 20:
                print(f"  ... and {len(remaining) - 20} more")
        
        elif choice == '7':
            output_file = input("Enter output filename (default: completion_report.json): ").strip()
            if not output_file:
                output_file = "completion_report.json"
            report = manager.export_completion_report(output_file)
            print(f"Report exported to {output_file}")
            print(f"Completion by category:")
            for category, data in report['completion_rate_by_category'].items():
                print(f"  {category}: {data['completed']}/{data['total']} ({data['completion_rate']:.1f}%)")
        
        elif choice == '8':
            manager.save_entries()
            print("Changes saved!")
            break
        
        elif choice == '9':
            print("Exiting without saving...")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
