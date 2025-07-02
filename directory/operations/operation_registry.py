
from .file_operations import *

operation_FOLDER_REGISTRY = {
    "create_folder": create_folder,
    "update_folder": update_folder,
    "move_folder_to_existing_folder": move_folder_to_existing_folder,
    "move_folder_after_creating_destination_folder": move_folder_after_creating_destination_folder,
    "delete_folder": delete_folder,
    "favorite_folder": favorite_folder,
}


# METHOD_FILE_REGISTRY={
#     "favorite_file": favorite_file,
#     "delete_file": delete_file,
#     "move_file_after_creating_destination_folder": move_file_after_creating_destination_folder,
#     "move_file_to_existing_folder": move_file_to_existing_folder,
#     "update_file": update_file,
# }