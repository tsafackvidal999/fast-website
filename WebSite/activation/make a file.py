from django.http import HttpResponse
from .models import License

def download_license(request, license_id):
    try:
        license = License.objects.get(id=license_id, user=request.user)
    except License.DoesNotExist:
        return HttpResponse("License not found.", status=404)

    # Créer le contenu du fichier
    content = f"License Key: {license.license_key}\nCreated At: {license.created_at}"

    # Créer la réponse HTTP
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="license_{license_id}.txt"'

    return response