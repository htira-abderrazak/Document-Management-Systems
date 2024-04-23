from file.models import File, Recent


class MediaServeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Check if the request is for a media file
        if request.path.startswith('/uploads/'):
            try:
                recent_files = Recent.objects.all()
                file = File.objects.get(file = (request.path).lstrip("/"))
                if not Recent.objects.filter(files = file).exists():
                    if recent_files.count() < 10 :
                        Recent(files =file).save()
                    else :
                        #delte the oldest file in recent and add the neww recent file
                        first = recent_files.first()
                        first.delete()
                        Recent(files =file).save()    
                
            except  File.DoesNotExist :
                return response
            
        
        return response