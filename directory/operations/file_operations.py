from file.models import File
from ..models import Directory

# folder Operation
def create_folder(name, parent_id, user):
    if not name or not user:
        return None

    try : 
        parent = Directory.objects.get(id=parent_id)
    except Directory.DoesNotExist:
        return None
    
    Directory.objects.create(name=name,parent=parent,user=user)


def update_folder(folder_id, new_name):
    if not new_name :
        return None
    try : 
        folder = Directory.objects.get(id=folder_id)
    except Directory.DoesNotExist:
        return None
    folder.name = new_name
    folder.save()

def move_folder_to_existing_folder(folder_id, destination_id):

    try : 
        folder = Directory.objects.get(id=folder_id)
        destination_folder = Directory.objects.get(id=destination_id)
    except Directory.DoesNotExist:
        return None

    folder.parent = destination_folder
    folder.save()

def move_folder_after_creating_destination_folder(folder_id, new_folder_name, parent_id, user) :
    if not new_folder_name or not user:
        return None

    try : 
        parent = Directory.objects.get(id=parent_id)
        folder = Directory.objects.get(id=folder_id)
    except Directory.DoesNotExist:
        return None
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
        return None
    folder.is_deleted=True
    folder.save()


def favorite_folder(folder_id, is_favorite):

    try :
        folder = Directory.objects.get(id =folder_id)
    except Directory.DoesNotExist :
        return None
    folder.favorite =is_favorite
    folder.save()
