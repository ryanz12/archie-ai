from tools.system import get_current_time
from tools.filesystem import *

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": (
                "Get the computer's current local time. Use this when the user "
                "asks what time it is or needs the current time."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": (
                "List the names of the immediate contents of a directory. "
                "Accepts an absolute path or a path relative to the user's "
                "home directory. Returns an empty list if the directory "
                "does not exist or is inaccessible."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": (
                            "Directory path to list. For example, "
                            "'Downloads' or 'Documents/UofT'."
                        ),
                    }
                },
                "required": ["directory"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "find_directory",
            "description": (
                "Recursively search inside a specified directory for folders "
                "matching a name or glob pattern. Returns matching absolute "
                "paths. The search directory defaults to the user's home "
                "directory. Use the directory argument to narrow the search. "
                "If multiple matches are returned, inspect them or ask the "
                "user which one they mean. Do not guess paths."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "target": {
                        "type": "string",
                        "description": (
                            "Folder name or glob pattern to search for, "
                            "such as 'MAT148H'."
                        ),
                    },
                    "directory": {
                        "type": "string",
                        "description": (
                            "Directory to search inside. Accepts an absolute "
                            "path or a path relative to the user's home "
                            "directory. Defaults to '~' if omitted. Use this "
                            "to restrict the search, such as 'Downloads'."
                        ),
                    },
                },
                "required": ["target"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "find_file",
            "description": (
                "Recursively search inside a specified directory for files "
                "matching a filename or glob pattern. Returns matching "
                "absolute paths. The search directory defaults to the user's "
                "home directory. Use the directory argument to narrow the "
                "search. If multiple matches are returned, inspect them or "
                "ask the user which one they mean. Do not guess paths."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "target": {
                        "type": "string",
                        "description": (
                            "Filename or glob pattern to search for, "
                            "such as '*.pdf' or 'lecture25_print.pdf'."
                        ),
                    },
                    "directory": {
                        "type": "string",
                        "description": (
                            "Directory to search inside. Accepts an absolute "
                            "path or a path relative to the user's home "
                            "directory. Defaults to '~' if omitted. Use this "
                            "to restrict the search, such as 'Downloads'."
                        ),
                    },
                },
                "required": ["target"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_file_info",
            "description": (
                "Get metadata for an existing file, including its name, "
                "stem, extension, size in bytes, last-modified time, and "
                "last-accessed time."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "file": {
                        "type": "string",
                        "description": (
                            "Path to the file. Accepts an absolute path or "
                            "a path relative to the user's home directory."
                        ),
                    }
                },
                "required": ["file"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": (
                "Read and return the UTF-8 text contents of a file. "
                "Accepts an absolute path or a path relative to the user's "
                "home directory. This is intended for text files, not "
                "binary files. Avoid reading large files unless requested."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": (
                            "Path to the text file. Prefer the exact "
                            "absolute path returned by find_file."
                        ),
                    }
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "move_files",
            "description": (
                "Move one or more files or directories into an existing "
                "destination directory. Accepts absolute paths or paths "
                "relative to the user's home directory. Checks that sources "
                "exist and refuses to move an item if another item with the "
                "same name already exists at the destination. Returns which "
                "items were moved and which failed. This modifies the "
                "filesystem, so only call it when the user has clearly "
                "requested the move. Use exact absolute paths returned by "
                "search tools. Do not invent or guess paths. If multiple "
                "possible matches exist, clarify before moving."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "sources": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": (
                            "List of exact source file or directory paths "
                            "to move."
                        ),
                    },
                    "destination": {
                        "type": "string",
                        "description": (
                            "Existing destination directory. Prefer the "
                            "exact absolute path returned by find_directory."
                        ),
                    },
                },
                "required": ["sources", "destination"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "rename_file",
            "description": (
                "Rename an existing file or directory. Accepts an absolute "
                "path or a path relative to the user's home directory. "
                "If the destination name already exists, the tool returns "
                "a confirmation request. Archie must ask the user before "
                "retrying with overwrite enabled. Never assume permission "
                "to overwrite."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": (
                            "Absolute or home-relative path of the item "
                            "to rename."
                        ),
                    },
                    "name": {
                        "type": "string",
                        "description": (
                            "New name for the file or directory. "
                            "Do not include a directory path."
                        ),
                    },
                },
                "required": ["path", "name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "create_files",
            "description": (
                "Create multiple empty files. Accepts absolute paths or "
                "paths relative to the user's home directory. Parent "
                "directories must already exist. Does not overwrite "
                "existing files."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "paths": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Paths of the files to create."
                    }
                },
                "required": ["paths"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_directory",
            "description": (
                "Create a directory. Automatically creates any missing "
                "parent directories. Accepts an absolute path or a path "
                "relative to the user's home directory. If the directory "
                "already exists, it reports that without changing it."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path of the directory to create."
                    }
                },
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "copy_file",
            "description": (
                "Copy a file into an existing destination directory. "
                "Preserves file metadata. Refuses to overwrite an existing "
                "file. Accepts absolute paths or paths relative to the "
                "user's home directory."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "source": {
                        "type": "string",
                        "description": "Path of the file to copy."
                    },
                    "destination": {
                        "type": "string",
                        "description": (
                            "Existing directory into which the file "
                            "should be copied."
                        )
                    }
                },
                "required": ["source", "destination"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_file",
            "description": (
                "Permanently delete a file. Does not delete directories. "
                "This operation cannot easily be undone. Only call when "
                "the user explicitly requests deletion. Use the exact "
                "path of the intended file."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path of the file to delete."
                    }
                },
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": (
                "Create a new UTF-8 text file and write the supplied "
                "content into it. Parent directory must exist. Refuses "
                "to overwrite an existing file. Use append_file to add "
                "content to an existing file."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path of the new file."
                    },
                    "content": {
                        "type": "string",
                        "description": "Text content to write into the file."
                    }
                },
                "required": ["path", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "append_file",
            "description": (
                "Append UTF-8 text to the end of a file. Creates the file "
                "if it does not exist. Does not replace existing content."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path of the file to append to."
                    },
                    "content": {
                        "type": "string",
                        "description": "Text to append to the file."
                    }
                },
                "required": ["path", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "unzip_file",
            "description": (
                "Extract a ZIP archive into a destination directory. "
                "Creates the destination directory if it does not exist. "
                "Refuses to overwrite existing files and rejects unsafe "
                "archive paths that attempt to extract outside the destination. "
                "Only supports ZIP archives. Use the exact archive path."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "source": {
                        "type": "string",
                        "description": "Path to the ZIP archive."
                    },
                    "destination": {
                        "type": "string",
                        "description": (
                            "Directory where the archive contents should "
                            "be extracted."
                        )
                    }
                },
                "required": ["source", "destination"]
            }
        }
    },
]


available_functions = {
    "get_current_time": {
        "function": get_current_time,
        "requires_permission": False
    },
    "list_files": {
        "function": list_files,
        "requires_permission": False
    },
    "find_directory": {
        "function": find_directory,
        "requires_permission": False
    },
    "find_file": {
        "function": find_file,
        "requires_permission": False
    },
    "get_file_info": {
        "function": get_file_info,
        "requires_permission": False
    },
    "read_file": {
        "function": read_file,
        "requires_permission": False
    },
    "move_files": {
        "function": move_files,
        "requires_permission": True
    },
    "rename_file": {
        "function": rename_file,
        "requires_permission": False
    },
    "create_files": {
        "function": create_files,
        "requires_permission": True
    },
    "create_directory": {
        "function": create_directory,
        "requires_permission": True
    },
    "copy_file": {
        "function": copy_file,
        "requires_permission": True
    },
    "delete_file": {
        "function": delete_file,
        "requires_permission": True
    },
    "write_file": {
        "function": write_file,
        "requires_permission": True
    },
    "append_file": {
        "function": append_file,
        "requires_permission": True
    },
    "unzip_file": {
        "function": unzip_file,
        "requires_permission": True
    },
}
