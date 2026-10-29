from django.conf import settings
from django.db import models


class DemandeInscription(models.Model):
    class Statut(models.TextChoices):
        EN_ATTENTE = "EN_ATTENTE", "En attente"
        ACCEPTEE = "ACCEPTEE", "Acceptée"
        REFUSEE = "REFUSEE", "Refusée"

    nom_complet = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    identifiant = models.CharField(max_length=150, unique=True)
    date_demande = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(
        max_length=20,
        choices=Statut.choices,
        default=Statut.EN_ATTENTE,
    )
    traite_par = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="comptes_demandes_traitees",
    )
    date_traitement = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.nom_complet} — {self.get_statut_display()}"

    class Meta:
        ordering = ["-date_demande"]
        verbose_name = "Demande d'inscription"
        verbose_name_plural = "Demandes d'inscription"