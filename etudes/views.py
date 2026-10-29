from django.shortcuts import redirect, render
from .forms import DemandeInscriptionForm


def demander_inscription(request):
    if request.method == "POST":
        form = DemandeInscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "comptes/demande_succes.html")
    else:
        form = DemandeInscriptionForm()
    return render(request, "comptes/demande_inscription.html", {"form": form})