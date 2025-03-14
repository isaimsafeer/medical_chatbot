import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)  
logger = logging.getLogger(__name__)

list_of_files = [
    "src/__init__.py",
    "src/helper.py",
    "src/prompt.py",
    ".env",
    "setup.py",
    "app.py",
    "research/trials.ipynb"
]

def create_directory_structure(file_list):
    """
    Creates directory structure and files from a list of file paths
    """
    # Get the current working directory
    base_path = Path.cwd()
    
    for file_path in file_list:
        # Convert string path to Path object
        full_path = base_path / file_path
        
        try:
            # Create parent directories if they don't exist
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Create the file if it doesn't exist
            if not full_path.exists():
                full_path.touch()
                logger.info(f"Created file: {file_path}")
            else:
                logger.info(f"File already exists: {file_path}")
                
        except Exception as e:
            logger.error(f"Error creating {file_path}: {str(e)}")

def main():
    logger.info("Starting directory structure creation...")
    create_directory_structure(list_of_files)
    logger.info("Directory structure creation completed!")

if __name__ == "__main__":
    main()