
from .file_operations import *

OPERATION_REGISTRY = {

    # Folder operations
    "create_folder": create_folder,
    "update_folder": update_folder,
    "move_folder": move_folder,
    "move_folder_and_create_destination": move_folder_and_create_destination,
    "delete_folder": delete_folder,
    "favorite_folder": favorite_folder,

    # File operations
    "favorite_file": favorite_file,
    "delete_file": delete_file,
    "move_file_and_create_destination": move_file_and_create_destination,
    "move_file": move_file,
    "update_file": update_file,

}


