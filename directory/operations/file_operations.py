from file.models import File
from ..models import Directory


class OperationError(Exception):
    pass

# folder Operation
def create_folder(name, parent_id, user):
    if not name or not user:
        raise OperationError("no name or user")
    
    try : 
        parent = Directory.objects.get(id=parent_id,is_deleted=False)
    except Directory.DoesNotExist:
        raise OperationError(f"folder {parent_id} does not exist")
    Directory.objects.create(name=name,parent=parent,user=user)


def update_folder(folder_id, new_name):
    if not new_name :
        raise OperationError("no name or user")
    try : 
        folder = Directory.objects.get(id=folder_id,is_deleted=False)
    except Directory.DoesNotExist:
        raise OperationError(f"folder {folder_id} does not exist")
    folder.name = new_name
    folder.save()

def move_folder_to_existing_folder(folder_id, destination_id):

    try : 
        folder = Directory.objects.get(id=folder_id,is_deleted=False)
        destination_folder = Directory.objects.get(id=destination_id,is_deleted=False)
    except Directory.DoesNotExist:
        raise OperationError(f"folder {folder_id} or {destination_id} does not exist")

    folder.parent = destination_folder
    folder.save()

def move_folder_after_creating_destination_folder(folder_id, new_folder_name, parent_id, user) :
    if not new_folder_name or not user:
        raise OperationError("no name or user")

    try : 
        parent = Directory.objects.get(id=parent_id,is_deleted=False)
        folder = Directory.objects.get(id=folder_id,is_deleted=False)
    except Directory.DoesNotExist:
        raise OperationError(f"folder {folder_id} or parent {parent_id} does not exist")
    # Check if the distination folder already exist
    try :
        existed_folder = Directory.objects.get(name=new_folder_name,parent=parent_id,is_deleted=False)
    except Directory.DoesNotExist:
        # If the distination folder exist
        new_folder=Directory.objects.create(name=new_folder_name, parent=parent_id,user =user)
        folder.parent = new_folder
        folder.save()
        return None
    folder.parent = existed_folder
    folder.save()
    

    
def delete_folder(folder_id):

    try :
        folder = Directory.objects.get(id =folder_id,is_deleted=False)
    except Directory.DoesNotExist :
        raise OperationError(f"folder {folder_id} does not exist")
    folder.is_deleted=True
    folder.save()


def favorite_folder(folder_id, is_favorite):

    try :
        folder = Directory.objects.get(id =folder_id,is_deleted=False)
    except Directory.DoesNotExist :
        raise OperationError(f"folder {folder_id} does not exist")
    folder.favorite =is_favorite
    folder.save()


# File operations

def favorite_file(file_id, is_favorite):

    try :
        file = File.objects.get(id =file_id,is_deleted=False)
    except File.DoesNotExist :
        raise OperationError(f"file {file_id} does not exist")
    file.favorite =is_favorite
    file.save()

def delete_file(file_id):

    try :
        file = File.objects.get(id =file_id,is_deleted=False)
    except File.DoesNotExist :
        raise OperationError(f"file {file_id} does not exist")
    file.is_deleted=True
    file.save()

def move_file_after_creating_destination_folder(file_id, new_folder_name, parent_id, user) :
    if not new_folder_name or not user:
        raise OperationError(f"no name or user")

    try : 
        directory = Directory.objects.get(id=parent_id,is_deleted=False)
        file = File.objects.get(id=file_id,is_deleted=False)
    except Directory.DoesNotExist:
        raise OperationError(f"folder {parent_id} does not exist")
    except File.DoesNotExist:
        raise OperationError(f"file {file_id} does not exist")

    # Check if the distination folder already exist
    try :
        existed_file = Directory.objects.get(name=new_folder_name,parent=parent_id,is_deleted=False)
    except Directory.DoesNotExist:
        # If the distination folder exist
        created_folder=Directory.objects.create(name=new_folder_name, parent=parent_id,user =user)
        file.directory = created_folder
        file.save()
        return None
    file.parent = existed_file
    file.save()


def move_file_to_existing_folder(file_id, destination_id):

    try : 
        file = File.objects.get(id=file_id)
        destination_folder = Directory.objects.get(id=destination_id,is_deleted=False)
    except File.DoesNotExist:
        raise OperationError(f"file {file_id} does not exist")
    except Directory.DoesNotExist:
        raise OperationError(f"destination folder {destination_id} does not exist")

    file.parent = destination_folder
    file.save()

def update_file(file_id, new_name):
    if not new_name :
        raise OperationError("no name provided for update")
    try : 
        file = File.objects.get(id=file_id,is_deleted=False)
    except File.DoesNotExist:
        raise OperationError(f"file {file_id} does not exist")
    file.name = new_name
    file.save()
