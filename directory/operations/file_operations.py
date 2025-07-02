from file.models import File
from ..models import Directory


class OperationError(Exception):
    pass

# folder Operation
def create_folder(name, parent_id, user):
    if not name or not user:
        raise OperationError("no name or user")

    try : 
        parent = Directory.objects.get(id=parent_id)
    except Directory.DoesNotExist:
        raise OperationError(f"folder {parent_id} does not exist")
    Directory.objects.create(name=name,parent=parent,user=user)


def update_folder(folder_id, new_name):
    if not new_name :
        raise OperationError("no name or user")
    try : 
        folder = Directory.objects.get(id=folder_id)
    except Directory.DoesNotExist:
        raise OperationError(f"folder {folder_id} does not exist")
    folder.name = new_name
    folder.save()

def move_folder_to_existing_folder(folder_id, destination_id):

    try : 
        folder = Directory.objects.get(id=folder_id)
        destination_folder = Directory.objects.get(id=destination_id)
    except Directory.DoesNotExist:
        raise OperationError(f"folder {folder_id} or {destination_id} does not exist")

    folder.parent = destination_folder
    folder.save()

def move_folder_after_creating_destination_folder(folder_id, new_folder_name, parent_id, user) :
    if not new_folder_name or not user:
        raise OperationError("no name or user")

    try : 
        parent = Directory.objects.get(id=parent_id)
        folder = Directory.objects.get(id=folder_id)
    except Directory.DoesNotExist:
        raise OperationError()
    # Check if the distination folder already exist
    try :
        existed_folder = Directory.objects.get(name=new_folder_name,parent=parent_id)
    except Directory.DoesNotExist:
        # If the distination folder exist
        Directory.objects.create(name=new_folder_name, parent=parent_id,user =user)
        folder.parent = parent
        folder.save()
        return None
    folder.parent = existed_folder
    folder.save()
    

    
def delete_folder(folder_id):

    try :
        folder = Directory.objects.get(id =folder_id)
    except Directory.DoesNotExist :
        raise OperationError()
    folder.is_deleted=True
    folder.save()


def favorite_folder(folder_id, is_favorite):

    try :
        folder = Directory.objects.get(id =folder_id)
    except Directory.DoesNotExist :
        raise OperationError()
    folder.favorite =is_favorite
    folder.save()


# File operations

def favorite_file(file_id, is_favorite):

    try :
        file = File.objects.get(id =file_id)
    except File.DoesNotExist :
        raise OperationError()
    file.favorite =is_favorite
    file.save()

def delete_file(file_id):

    try :
        file = File.objects.get(id =file_id)
    except File.DoesNotExist :
        raise OperationError()
    file.is_deleted=True
    file.save()

def move_file_after_creating_destination_folder(file_id, new_folder_name, parent_id, user) :
    if not new_folder_name or not user:
        raise OperationError(f"no name or user")

    try : 
        directory = Directory.objects.get(id=parent_id)
        file = File.objects.get(id=file_id)
    except Directory.DoesNotExist or File.DoesNotExist:
        raise OperationError(f"file {file_id} or folder {parent_id} not exist")
    # Check if the distination folder already exist
    try :
        existed_file = Directory.objects.get(name=new_folder_name,parent=parent_id)
    except Directory.DoesNotExist:
        # If the distination folder exist
        directory.objects.create(name=new_folder_name, parent=parent_id,user =user)
        file.directory = directory
        file.save()
        return None
    file.parent = existed_file
    file.save()


def move_file_to_existing_folder(file_id, destination_id):

    try : 
        file = File.objects.get(id=file_id)
        destination_folder = Directory.objects.get(id=destination_id)
    except File.DoesNotExist:
        raise OperationError()

    file.parent = destination_folder
    file.save()

def update_file(file_id, new_name):
    if not new_name :
        raise OperationError()
    try : 
        file = File.objects.get(id=file_id)
    except File.DoesNotExist:
        raise OperationError()
    file.name = new_name
    file.save()