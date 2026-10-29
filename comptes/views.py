from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from .models import (
    Annonce,
    AnnonceUniversitaire,
    DemandeInscription,
    DepenseCaisse,
    DocumentPartage,
    FlashInfo,
    LivreBibliotheque,
    MessageChat,
    PaiementCaisse,
    PhotoGalerie,
    Presence,
    ProfilEtudiant,
    TacheGroupe,
)


def accueil_vue(request):
    return render(request, "comptes/accueil.html")


def demander_inscription(request):
    if request.method == "POST":
        nom = request.POST.get("nom")
        email = request.POST.get("email")
        if nom and email:
            DemandeInscription.objects.get_or_create(nom=nom, email=email)
            return redirect("comptes:accueil")
    return render(request, "comptes/demander_inscription.html")


@login_required(login_url="comptes:connexion")
def valider_demande(request, demande_id):
    if request.user.is_superuser:
        demande = get_object_or_404(DemandeInscription, id=demande_id)
        demande.statut = DemandeInscription.Statut.ACCEPTEE
        demande.validee = True
        demande.save()
    return redirect("comptes:tableau_de_bord")


@login_required(login_url="comptes:connexion")
def refuser_demande(request, demande_id):
    if request.user.is_superuser:
        demande = get_object_or_404(DemandeInscription, id=demande_id)
        demande.statut = DemandeInscription.Statut.REFUSEE
        demande.validee = False
        demande.save()
    return redirect("comptes:tableau_de_bord")


@login_required(login_url="comptes:connexion")
def tableau_de_bord(request):
    profil, _ = ProfilEtudiant.objects.get_or_create(user=request.user)

    if request.method == "POST":
        if "ajouter_paiement" in request.POST and request.user.is_superuser:
            membre_id = request.POST.get("membre_id")
            montant = request.POST.get("montant")
            type_paiement = request.POST.get("type_paiement")
            commentaire = request.POST.get("commentaire", "")
            if membre_id and montant:
                membre_obj = get_object_or_404(User, id=membre_id)
                PaiementCaisse.objects.create(
                    membre=membre_obj,
                    montant=montant,
                    type_paiement=type_paiement,
                    commentaire=commentaire,
                )
            return redirect("comptes:tableau_de_bord")

        elif "ajouter_depense" in request.POST and request.user.is_superuser:
            titre = request.POST.get("titre_depense")
            montant = request.POST.get("montant_depense")
            justificatif = request.FILES.get("justificatif_depense")
            if titre and montant:
                DepenseCaisse.objects.create(
                    titre=titre, montant=montant, justificatif=justificatif
                )
            return redirect("comptes:tableau_de_bord")

        elif "ajouter_flash" in request.POST and request.user.is_superuser:
            titre = request.POST.get("titre_flash")
            contenu = request.POST.get("contenu_flash")
            if titre and contenu:
                FlashInfo.objects.create(titre=titre, contenu=contenu)
            return redirect("comptes:tableau_de_bord")

        elif "creer_presence" in request.POST and request.user.is_superuser:
            titre_reunion = request.POST.get("titre_reunion")
            date_reunion = request.POST.get("date_reunion")
            if titre_reunion and date_reunion:
                Presence.objects.create(
                    titre_reunion=titre_reunion, date_reunion=date_reunion
                )
            return redirect("comptes:tableau_de_bord")

        elif "ajouter_annonce" in request.POST and request.user.is_superuser:
            titre = request.POST.get("titre_annonce")
            contenu = request.POST.get("contenu_annonce")
            if titre and contenu:
                AnnonceUniversitaire.objects.create(
                    titre=titre, contenu=contenu, publie_par=request.user
                )
            return redirect("comptes:tableau_de_bord")

        elif "modifier_profil" in request.POST:
            profil.bio = request.POST.get("bio", "")
            profil.competences = request.POST.get("competences", "")
            profil.telephone = request.POST.get("telephone", "")
            profil.save()
            return redirect("comptes:tableau_de_bord")

        elif "ajouter_document" in request.POST:
            titre = request.POST.get("titre_doc")
            categorie = request.POST.get("categorie_doc")
            fichier = request.FILES.get("fichier_doc")
            if titre and fichier:
                DocumentPartage.objects.create(
                    titre=titre, categorie=categorie, fichier=fichier
                )
            return redirect("comptes:tableau_de_bord")

        elif "ajouter_livre" in request.POST:
            titre = request.POST.get("titre_livre")
            auteur = request.POST.get("auteur_livre", "")
            fichier = request.FILES.get("fichier_livre")
            if titre and fichier:
                LivreBibliotheque.objects.create(
                    titre=titre, auteur=auteur, fichier_livre=fichier
                )
            return redirect("comptes:tableau_de_bord")

        elif "ajouter_photo" in request.POST:
            titre = request.POST.get("titre_photo")
            image = request.FILES.get("image_photo")
            if titre and image:
                PhotoGalerie.objects.create(titre=titre, image=image)
            return redirect("comptes:tableau_de_bord")

        elif "texte_message" in request.POST:
            texte = request.POST.get("texte_message")
            if texte and texte.strip():
                MessageChat.objects.create(expediteur=request.user, texte=texte)

        elif "titre_tache" in request.POST:
            titre_tache = request.POST.get("titre_tache")
            if titre_tache and titre_tache.strip():
                TacheGroupe.objects.create(titre=titre_tache)

        return redirect("comptes:tableau_de_bord")

    context = {
        "profil": profil,
        "documents": DocumentPartage.objects.all().order_by("-date_ajout"),
        "livres_biblio": LivreBibliotheque.objects.all().order_by("-date_ajout"),
        "annonces_univ": AnnonceUniversitaire.objects.all().order_by(
            "-date_publication"
        ),
        "flash_infos": FlashInfo.objects.filter(actif=True).order_by(
            "-date_publication"
        ),
        "messages_chat": MessageChat.objects.all().order_by("date_envoi"),
        "taches": TacheGroupe.objects.all(),
        "photos": PhotoGalerie.objects.all().order_by("-date_ajout"),
        "tous_les_membres": User.objects.all(),
        "profils_etudiants": ProfilEtudiant.objects.all(),
        "reunions": Presence.objects.all().order_by("-date_reunion"),
        "demandes_attente": DemandeInscription.objects.filter(
            statut=DemandeInscription.Statut.EN_ATTENTE
        ),
    }

    if request.user.is_superuser:
        tous_les_paiements = PaiementCaisse.objects.all()
        toutes_les_depenses = DepenseCaisse.objects.all().order_by(
            "-date_depense"
        )
        membres_details = []
        for m in User.objects.all():
            s1 = (
                PaiementCaisse.objects.filter(
                    membre=m, type_paiement=PaiementCaisse.TypePaiement.SEMAINE_1
                ).aggregate(total=Sum("montant"))["total"]
                or Decimal("0.00")
            )
            s2 = (
                PaiementCaisse.objects.filter(
                    membre=m, type_paiement=PaiementCaisse.TypePaiement.SEMAINE_2
                ).aggregate(total=Sum("montant"))["total"]
                or Decimal("0.00")
            )
            s3 = (
                PaiementCaisse.objects.filter(
                    membre=m, type_paiement=PaiementCaisse.TypePaiement.SEMAINE_3
                ).aggregate(total=Sum("montant"))["total"]
                or Decimal("0.00")
            )
            s4 = (
                PaiementCaisse.objects.filter(
                    membre=m, type_paiement=PaiementCaisse.TypePaiement.SEMAINE_4
                ).aggregate(total=Sum("montant"))["total"]
                or Decimal("0.00")
            )
            total_m = (
                PaiementCaisse.objects.filter(membre=m).aggregate(
                    total=Sum("montant")
                )["total"]
                or Decimal("0.00")
            )
            membres_details.append(
                {
                    "username": m.username,
                    "semaine_1": s1,
                    "semaine_2": s2,
                    "semaine_3": s3,
                    "semaine_4": s4,
                    "total": total_m,
                }
            )

        total_rec = (
            tous_les_paiements.aggregate(total=Sum("montant"))["total"] or 0
        )
        total_dep = (
            toutes_les_depenses.aggregate(total=Sum("montant"))["total"] or 0
        )
        context.update(
            {
                "tous_les_paiements": tous_les_paiements,
                "toutes_les_depenses": toutes_les_depenses,
                "membres_details": membres_details,
                "total_recettes": total_rec,
                "total_depenses": total_dep,
                "solde_caisse": total_rec - total_dep,
            }
        )

    return render(request, "comptes/tableau_de_bord.html", context)


@login_required(login_url="comptes:connexion")
def supprimer_document(request, doc_id):
    DocumentPartage.objects.filter(id=doc_id).delete()
    return redirect("comptes:tableau_de_bord")


@login_required(login_url="comptes:connexion")
def supprimer_livre(request, livre_id):
    if request.user.is_superuser:
        LivreBibliotheque.objects.filter(id=livre_id).delete()
    return redirect("comptes:tableau_de_bord")


@login_required(login_url="comptes:connexion")
def supprimer_annonce(request, annonce_id):
    if request.user.is_superuser:
        AnnonceUniversitaire.objects.filter(id=annonce_id).delete()
    return redirect("comptes:tableau_de_bord")


@login_required(login_url="comptes:connexion")
def supprimer_flash(request, flash_id):
    if request.user.is_superuser:
        FlashInfo.objects.filter(id=flash_id).delete()
    return redirect("comptes:tableau_de_bord")


@login_required(login_url="comptes:connexion")
def supprimer_photo(request, photo_id):
    PhotoGalerie.objects.filter(id=photo_id).delete()
    return redirect("comptes:tableau_de_bord")


@login_required(login_url="comptes:connexion")
def supprimer_tache(request, tache_id):
    TacheGroupe.objects.filter(id=tache_id).delete()
    return redirect("comptes:tableau_de_bord")


@login_required(login_url="comptes:connexion")
def supprimer_message(request, msg_id):
    msg = get_object_or_404(MessageChat, id=msg_id)
    if msg.expediteur == request.user or request.user.is_superuser:
        msg.delete()
    return redirect("comptes:tableau_de_bord")