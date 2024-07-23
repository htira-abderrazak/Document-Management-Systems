from django.http import Http404
from file.models import File, Recent


class MediaServeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Check if the request is for a media file
        if request.path.startswith('/uploads/'):
            try:
                
                file = File.objects.get(file = request.path[len('/uploads/'):])
                user=file.user
                recent_files = Recent.objects.filter(user =user)
                if not recent_files.filter(files = file).exists():
                    if recent_files.count() < 10 :
                        Recent(files =file,user = user).save()
                    else :
                        #delte the oldest file in recent and add the neww recent file
                        first = recent_files.first()
                        first.delete()
                        Recent(files =file,user = user).save()    
                
            except  File.DoesNotExist :
                # raise Http404("Page not found")
                return response
        
        return response