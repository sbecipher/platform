import os
import shutil
import zipfile
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class ArtifactStore:
    def __init__(self, base_path: str = "output/runs"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def store_run_archive(self, run_id: str, zip_file_path: str) -> str:
        """
        Unzips a diligence run archive into the local artifact store.
        Returns the absolute path to the run root directory.
        """
        run_root = self.base_path / run_id
        run_root.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Unzipping artifact archive for run {run_id} to {run_root}")
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(run_root)
            
        artifacts = []
        for root, _, files in os.walk(run_root):
            for file in files:
                if file.endswith(('.csv', '.json', '.png')):
                    full_path = Path(root) / file
                    rel_path = full_path.relative_to(run_root)
                    source_key = file.split('.')[0]
                    file_type = file.split('.')[-1].upper()
                    artifacts.append({
                        "source_key": source_key,
                        "file_path": str(rel_path).replace('\\', '/'),
                        "file_type": file_type
                    })
                    
        return str(run_root.absolute()), artifacts
        
    def store_file(self, run_id: str, file_name: str, file_bytes: bytes) -> str:
        """
        Stores a single raw file into the run root directory.
        """
        run_root = self.base_path / run_id
        run_root.mkdir(parents=True, exist_ok=True)
        
        file_path = run_root / file_name
        with open(file_path, 'wb') as f:
            f.write(file_bytes)
            
        return str(file_path.absolute())
