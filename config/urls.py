from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from django.urls import include, path


def redirection_accueil(request):
    """Redirige automatiquement la racine du site vers la page de connexion"""
    return redirect("comptes:connexion")


urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "comptes/", include("comptes.urls")
    ),  # Intègre toutes les routes de l'application comptes
    path("", redirection_accueil),  # Page d'accueil racine
]

# Permet à Django de servir les fichiers PDF et images téléchargés en mode développement
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )