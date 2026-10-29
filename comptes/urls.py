from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

app_name = "comptes"

urlpatterns = [
    path("", views.accueil_vue, name="accueil"),
    path(
        "connexion/",
        auth_views.LoginView.as_view(
            template_name="comptes/connexion.html",
            next_page="/comptes/tableau-de-bord/",
        ),
        name="connexion",
    ),
    path(
        "deconnexion/",
        auth_views.LogoutView.as_view(next_page="comptes:accueil"),
        name="deconnexion",
    ),
    path("inscription/", views.demander_inscription, name="demander_inscription"),
    path("tableau-de-bord/", views.tableau_de_bord, name="tableau_de_bord"),
    path(
        "supprimer-document/<int:doc_id>/",
        views.supprimer_document,
        name="supprimer_document",
    ),
    path(
        "supprimer-livre/<int:livre_id>/",
        views.supprimer_livre,
        name="supprimer_livre",
    ),
    path(
        "supprimer-annonce/<int:annonce_id>/",
        views.supprimer_annonce,
        name="supprimer_annonce",
    ),
    path(
        "supprimer-flash/<int:flash_id>/",
        views.supprimer_flash,
        name="supprimer_flash",
    ),
    path(
        "supprimer-photo/<int:photo_id>/",
        views.supprimer_photo,
        name="supprimer_photo",
    ),
    path(
        "supprimer-tache/<int:tache_id>/",
        views.supprimer_tache,
        name="supprimer_tache",
    ),
    path(
        "supprimer-message/<int:msg_id>/",
        views.supprimer_message,
        name="supprimer_message",
    ),
]