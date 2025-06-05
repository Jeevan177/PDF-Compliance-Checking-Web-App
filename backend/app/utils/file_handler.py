import tempfile
import os
from fastapi import UploadFile
import aiofiles

class FileHandler:
    @staticmethod
    async def save_upload_file(upload_file: UploadFile, destination: str) -> str:
        """Save uploaded file to destination"""
        async with aiofiles.open(destination, 'wb') as f:
            content = await upload_file.read()
            await f.write(content)
        return destination
    
    @staticmethod
    def create_temp_file(suffix: str = "") -> str:
        """Create temporary file and return path"""
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
        temp_file.close()
        return temp_file.name
    
    @staticmethod
    def cleanup_file(file_path: str):
        """Remove file if it exists"""
        if os.path.exists(file_path):
            os.unlink(file_path)