from django.core.management.base import BaseCommand

from file.models import File, TotalFileSize


class Command(BaseCommand):
    help = 'create instance in total file size'

    def handle(self, *args, **options):
        files = File.objects.all()
        try :
            total_size =TotalFileSize.objects.get(id=1)
        except TotalFileSize.DoesNotExist:
            total_size =TotalFileSize(id=1,total_size = 0).save()
        
        size = 0
        for file in files:
            size += file.file.size
        total_size.total_size= size/1024/1024
        total_size.save()
        pass  