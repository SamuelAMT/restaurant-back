from django.template.loader import get_template
from django.http import HttpResponse
from django.conf import settings

def debug_templates(request):
    try:
        template = get_template('core/home.html')
        return HttpResponse(f"Template found! Path: {template.origin.name}")
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}\nTemplate dirs: {settings.TEMPLATES[0]['DIRS']}")