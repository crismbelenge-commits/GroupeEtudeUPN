from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class ProfilEtudiant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    competences = models.CharField(
        max_length=255, blank=True, null=True, help_text="Ex: Python, Django, SQL"
    )
    telephone = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return f"Profil de {self.user.username}"


class DemandeInscription(models.Model):
    class Statut(models.TextChoices):
        EN_ATTENTE = "EN_ATTENTE", "En attente"
        ACCEPTEE = "ACCEPTEE", "Acceptée"
        REFUSEE = "REFUSEE", "Refusée"

    nom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    identifiant = models.CharField(max_length=150, unique=True, blank=True, null=True)
    date_demande = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(
        max_length=20,
        choices=Statut.choices,
        default=Statut.EN_ATTENTE,
    )
    validee = models.BooleanField(default=False)
    traite_par = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="demandes_traitees",
    )
    date_traitement = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.nom} — {self.get_statut_display()}"

    class Meta:
        ordering = ["-date_demande"]
        verbose_name = "Demande d'inscription"
        verbose_name_plural = "Demandes d'inscription"


class Annonce(models.Model):
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    date_publication = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre


class FlashInfo(models.Model):
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    actif = models.BooleanField(default=True)
    date_publication = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre


class AnnonceUniversitaire(models.Model):
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    date_publication = models.DateTimeField(auto_now_add=True)
    publie_par = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.titre


class DocumentPartage(models.Model):
    class CategorieDoc(models.TextChoices):
        COURS = "COURS", "Cours"
        TP = "TP", "Travaux Pratiques (TP)"
        EXERCICE = "EXERCICE", "Exercice / Devoir"
        AUTRE = "AUTRE", "Autre Document"

    titre = models.CharField(max_length=200)
    categorie = models.CharField(
        max_length=20, choices=CategorieDoc.choices, default=CategorieDoc.COURS
    )
    description = models.TextField(blank=True, null=True)
    fichier = models.FileField(upload_to="documents/")
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.get_categorie_display()}] {self.titre}"


class LivreBibliotheque(models.Model):
    titre = models.CharField(max_length=200)
    auteur = models.CharField(max_length=150, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    fichier_livre = models.FileField(upload_to="bibliotheque/")
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titre} - {self.auteur or 'Auteur inconnu'}"


class PhotoGalerie(models.Model):
    titre = models.CharField(max_length=200)
    image = models.ImageField(upload_to="photos/")
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre


class MessageChat(models.Model):
    expediteur = models.ForeignKey(User, on_delete=models.CASCADE)
    texte = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.expediteur.username}: {self.texte[:30]}"

    class Meta:
        ordering = ["date_envoi"]  # Du plus ancien au plus récent pour le chat


class TacheGroupe(models.Model):
    titre = models.CharField(max_length=200)
    terminee = models.BooleanField(default=False)

    def __str__(self):
        return self.titre


class Presence(models.Model):
    titre_reunion = models.CharField(max_length=200)
    date_reunion = models.DateTimeField()
    membres_presents = models.ManyToManyField(
        User, blank=True, related_name="reunions_presentes"
    )

    def __str__(self):
        return self.titre_reunion


class PaiementCaisse(models.Model):
    class TypePaiement(models.TextChoices):
        SEMAINE_1 = "SEMAINE_1", "Semaine 1"
        SEMAINE_2 = "SEMAINE_2", "Semaine 2"
        SEMAINE_3 = "SEMAINE_3", "Semaine 3"
        SEMAINE_4 = "SEMAINE_4", "Semaine 4"
        COTISATION_MENSUELLE = "MENSUELLE", "Mois (Global)"
        FRAIS_ADHESION = "ADHESION", "Frais d'Adhésion"
        ANNIVERSAIRE = "ANNIVERSAIRE", "Anniversaire"
        VISITE = "VISITE", "Visite"
        ACHAT_SUPPORT = "ACHAT_SUPPORT", "Achat support"
        DA = "DA", "D.A"
        PRATIQUE = "PRATIQUE", "Pratique"
        AUTRE = "AUTRE", "Autre Paiement"

    membre = models.ForeignKey(User, on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    type_paiement = models.CharField(
        max_length=30,
        choices=TypePaiement.choices,
        default=TypePaiement.SEMAINE_1,
    )
    commentaire = models.TextField(blank=True, null=True)
    date_paiement = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.membre.username} - {self.get_type_paiement_display()} ({self.montant} FC)"


class DepenseCaisse(models.Model):
    titre = models.CharField(max_length=200)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    justificatif = models.FileField(
        upload_to="justificatifs/", blank=True, null=True
    )
    date_depense = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titre} (-{self.montant} FC)"