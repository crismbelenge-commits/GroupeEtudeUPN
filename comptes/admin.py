from django.contrib import admin
from .models import (
    Annonce,
    DemandeInscription,
    DepenseCaisse,
    DocumentPartage,
    MessageChat,
    PaiementCaisse,
    PhotoGalerie,
    Presence,
    TacheGroupe,
)

admin.site.register(DemandeInscription)
admin.site.register(Annonce)
admin.site.register(DocumentPartage)
admin.site.register(PhotoGalerie)
admin.site.register(MessageChat)
admin.site.register(TacheGroupe)
admin.site.register(Presence)
admin.site.register(PaiementCaisse)
admin.site.register(DepenseCaisse)