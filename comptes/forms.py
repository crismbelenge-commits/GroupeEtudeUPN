from django import forms
from django.contrib.auth.models import User
from .models import DemandeInscription


class DemandeInscriptionForm(forms.ModelForm):
    class Meta:
        model = DemandeInscription
        fields = ["nom_complet", "email", "identifiant"]
        widgets = {
            "nom_complet": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "identifiant": forms.TextInput(attrs={"class": "form-control"}),
        }


class ModifierProfilForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "email"]
        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Votre nom complet",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "votre@email.com",
                }
            ),
        }