from django.conf import settings

def getSettings(request):
	return {'baseUrl': settings.BASEURL}