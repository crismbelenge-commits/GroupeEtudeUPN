from django.contrib import admin
from .models import (
    ProfilEtudiant,
    DemandeInscription,
    Annonce,
    FlashInfo,
    AnnonceUniversitaire,
    DocumentPartage,
    LivreBibliotheque,
    PhotoGalerie,
    MessageChat,
    TacheGroupe,
    Presence,
    PaiementCaisse,
    DepenseCaisse,
)

admin.site.register(ProfilEtudiant)
admin.site.register(DemandeInscription)
admin.site.register(Annonce)
admin.site.register(FlashInfo)
admin.site.register(AnnonceUniversitaire)
admin.site.register(DocumentPartage)
admin.site.register(LivreBibliotheque)
admin.site.register(PhotoGalerie)
admin.site.register(MessageChat)
admin.site.register(TacheGroupe)
admin.site.register(Presence)
admin.site.register(PaiementCaisse)
admin.site.register(DepenseCaisse)