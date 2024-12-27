import json
import os
from pathlib import Path

def _validate_path(base_dir, filename):
    try:
        # Convert to absolute path and resolve any symlinks
        base_path = Path(base_dir).resolve()
        full_path = (base_path / filename).resolve()
        
        # Verify the path is within the base directory
        if not str(full_path).startswith(str(base_path)):
            raise ValueError("Invalid path: Attempted directory traversal")
        
        # Verify the file has .json extension
        if not full_path.suffix.lower() == '.json':
            raise ValueError("Invalid file: Must have .json extension")
            
        return full_path
        
    except Exception as e:
        raise ValueError(f"Invalid path: {str(e)}")

def create_json_if_not_exists(base_dir, filename):
    path = _validate_path(base_dir, filename)
    os.makedirs(path.parent, exist_ok=True)
    
    if not path.exists():
        with open(path, 'w') as f:
            json.dump({}, f)

def load_json(base_dir, filename):

    path = _validate_path(base_dir, filename)
    
    if not path.exists():
        raise FileNotFoundError(f"File not found: {filename}")
        
    with open(path, 'r') as f:
        return json.load(f)

def save_json(data, base_dir, filename):
    path = _validate_path(base_dir, filename)
    os.makedirs(path.parent, exist_ok=True)
    
    with open(path, 'w') as f:
        json.dump(data, f)
