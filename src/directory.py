from pathlib import Path

def get_dirs_valid_htmls(path: Path) -> list[Path]:
    if not path.is_dir(): raise NotADirectoryError(f"{path} is not a directory")
    valid_files: list[Path] = [file for file in path.glob("*.html") if file.stat().st_size > 0]
    if not valid_files or not any(path.iterdir()): 
        raise Exception(f"{path} is empty")
    return valid_files

        

    