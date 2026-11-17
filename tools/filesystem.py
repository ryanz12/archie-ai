from pathlib import Path
from datetime import datetime
import shutil
import zipfile

def normalize_path(path: str) -> Path:
    new_path = Path(path).expanduser()

    if not new_path.is_absolute():
        new_path = Path.home() / path

    return new_path.resolve()


def list_files(directory: str) -> list[str]:
    """
    Given a relative directory, list the files in the folder
    """
    path = normalize_path(directory)

    if not path.is_dir():
        return []

    return sorted(file.name for file in path.iterdir())


def find_directory(target: str, directory: str = "~") -> list[str]:
    """
    Given a folder name, try to find the path in /home/user
    """
    new_dir = normalize_path(directory)
    return [str(path) for path in new_dir.rglob(target) if path.is_dir()]


def find_file(target: str, directory: str = "~") -> list[str]:
    """
    Given a file name, try to find the path of file in /home/user
    """
    new_dir = normalize_path(directory)
    return [str(path) for path in new_dir.rglob(target) if path.is_file()]


def get_file_info(file: str) -> dict:
    """
    Given a file directory, output the name, stem, etension, size, last modified,
    and last accessed of the file
    """
    path = normalize_path(file)

    if not path.is_file():
        return {"error": "File does not exist or is not accessible"}

    stats = path.stat()

    return {
        "name": path.name,
        "stem": path.stem,
        "extension": path.suffix,
        "size_bytes": stats.st_size,
        "last_modified": datetime.fromtimestamp(stats.st_mtime).isoformat(),
        "last_accessed": datetime.fromtimestamp(stats.st_atime).isoformat()
    }


def read_file(path: str) -> str:
    """
    Given a file path, read the file and output its content
    """
    new_path = normalize_path(path)

    try:
        return new_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as e:
        return f"Error: {e}"


def move_files(sources: list[str], destination: str) -> dict:
    destination_path = normalize_path(destination)

    if not destination_path.is_dir():
        return {
            "success": False,
            "error": "Destination directory does not exist."
        }

    moved = []
    failed = []

    for source in sources:
        source_path = normalize_path(source)

        try:
            if not source_path.exists():
                raise FileNotFoundError("Source does not exist")

            target_path = destination_path / source_path.name

            if target_path.exists():
                raise FileExistsError("A file with this name already exists")

            shutil.move(str(source_path), str(destination_path))
            moved.append(str(source_path))

        except (OSError, shutil.Error) as e:
            failed.append({
                "source": str(source_path),
                "error": str(e)
            })

    return {
        "success": len(failed) == 0,
        "moved": moved,
        "failed": failed
    }


def rename_file(path: str, name: str, overwrite: bool = False) -> dict:
    source = normalize_path(path)
    target = source.with_name(name)

    if not source.exists():
        return {
            "success": False,
            "error": "Source file does not exist."
        }

    if target.exists() and not overwrite:
        return {
            "success": False,
            "require_confirmation": True,
            "message": f"{target.name} already exists. Overwrite it?"
        }

    try:
        source.rename(target)

        return {
            "success": True,
            "old_path": str(source),
            "new_path": str(target),
            "overwrite": target.exists()
        }

    except OSError as e:
        return {
            "success": False,
            "error": str(e)
        }


def create_files(paths: list[str]) -> dict:
    """
    Create multiple empty files.
    Existing files are never overwritten.
    """
    created = []
    failed = []

    for file in paths:
        path = normalize_path(file)

        try:
            if path.exists():
                raise FileExistsError("A file or directory already exists at this path")

            if not path.parent.is_dir():
                raise FileNotFoundError("Parent directory does not exist")

            path.touch(exist_ok=False)
            created.append(str(path))

        except OSError as e:
            failed.append({
                "path": str(path),
                "error": str(e)
            })

    return {
        "success": len(failed) == 0,
        "created": created,
        "failed": failed
    }


def create_directory(path: str) -> dict:
    """
    Create a directory, including any missing parent directories.
    """
    new_path = normalize_path(path)

    try:
        new_path.mkdir(parents=True, exist_ok=True)

        return {
            "success": True,
            "path": str(new_path),
            "already_existed": False
        }

    except FileExistsError:
        return {
            "success": False,
            "error": "A file already exists at this path."
        }

    except OSError as e:
        return {
            "success": False,
            "error": str(e)
        }


def copy_file(source: str, destination: str) -> dict:
    """
    Copy a file into an existing destination directory.
    Refuses to overwrite existing files.
    """
    source_path = normalize_path(source)
    destination_path = normalize_path(destination)

    if not source_path.is_file():
        return {
            "success": False,
            "error": "Source file does not exist."
        }

    if not destination_path.is_dir():
        return {
            "success": False,
            "error": "Destination directory does not exist."
        }

    target_path = destination_path / source_path.name

    if target_path.exists():
        return {
            "success": False,
            "error": "A file with this name already exists at the destination."
        }

    try:
        shutil.copy2(source_path, target_path)

        return {
            "success": True,
            "source": str(source_path),
            "destination": str(target_path)
        }

    except (OSError, shutil.Error) as e:
        return {
            "success": False,
            "error": str(e)
        }


def delete_file(path: str) -> dict:
    """
    Delete a file. Does not delete directories.
    """
    file_path = normalize_path(path)

    if not file_path.exists() and not file_path.is_symlink():
        return {
            "success": False,
            "error": "File does not exist."
        }

    if file_path.is_dir() and not file_path.is_symlink():
        return {
            "success": False,
            "error": "The specified path is a directory. This tool only deletes files."
        }

    try:
        file_path.unlink()

        return {
            "success": True,
            "deleted": str(file_path)
        }

    except OSError as e:
        return {
            "success": False,
            "error": str(e)
        }


def write_file(path: str, content: str) -> dict:
    """
    Create a new text file and write content into it.
    Refuses to overwrite existing files.
    """
    file_path = normalize_path(path)

    if not file_path.parent.is_dir():
        return {
            "success": False,
            "error": "Parent directory does not exist."
        }

    try:
        # Exclusive creation prevents accidental overwrites.
        with file_path.open("x", encoding="utf-8") as file:
            file.write(content)

        return {
            "success": True,
            "path": str(file_path),
            "bytes_written": file_path.stat().st_size
        }

    except FileExistsError:
        return {
            "success": False,
            "error": "A file already exists at this path. No changes were made."
        }

    except OSError as e:
        return {
            "success": False,
            "error": str(e)
        }


def append_file(path: str, content: str) -> dict:
    """
    Append text to an existing file, or create it if it does not exist.
    """
    file_path = normalize_path(path)

    if not file_path.parent.is_dir():
        return {
            "success": False,
            "error": "Parent directory does not exist."
        }

    if file_path.exists() and not file_path.is_file():
        return {
            "success": False,
            "error": "The specified path is not a regular file."
        }

    try:
        with file_path.open("a", encoding="utf-8") as file:
            file.write(content)

        return {
            "success": True,
            "path": str(file_path),
            "bytes_appended": len(content.encode("utf-8"))
        }

    except OSError as e:
        return {
            "success": False,
            "error": str(e)
        }


def unzip_file(source: str, destination: str) -> dict:
    """
    Extract a ZIP archive into a destination directory.
    Refuses to overwrite existing files and prevents path traversal.
    """
    source_path = normalize_path(source)
    destination_path = normalize_path(destination)

    if not source_path.is_file():
        return {
            "success": False,
            "error": "ZIP archive does not exist."
        }

    if not zipfile.is_zipfile(source_path):
        return {
            "success": False,
            "error": "The specified file is not a valid ZIP archive."
        }

    try:
        destination_path.mkdir(parents=True, exist_ok=True)

        extracted = []

        with zipfile.ZipFile(source_path, "r") as archive:
            # Validate all entries before extracting anything.
            for member in archive.infolist():
                target = (destination_path / member.filename).resolve()

                if not target.is_relative_to(destination_path.resolve()):
                    return {
                        "success": False,
                        "error": "Archive contains an unsafe file path."
                    }

                if target.exists():
                    return {
                        "success": False,
                        "error": f"File already exists: {target}"
                    }

            for member in archive.infolist():
                target = (destination_path / member.filename).resolve()

                if member.is_dir():
                    target.mkdir(parents=True, exist_ok=True)
                    continue

                target.parent.mkdir(parents=True, exist_ok=True)

                with archive.open(member) as source_file:
                    with target.open("xb") as target_file:
                        shutil.copyfileobj(source_file, target_file)

                extracted.append(str(target))

        return {
            "success": True,
            "archive": str(source_path),
            "destination": str(destination_path),
            "extracted": extracted
        }

    except (OSError, zipfile.BadZipFile, RuntimeError, ValueError) as e:
        return {
            "success": False,
            "error": str(e)
        }
