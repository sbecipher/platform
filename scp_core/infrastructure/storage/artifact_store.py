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
            
        return str(run_root.absolute())
        
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
