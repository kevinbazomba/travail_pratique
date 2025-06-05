from django.shortcuts import render, redirect

# Create your views here.


def index(request):
      return render(request, 'index.html')

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .models import Etudiant, Photo

@csrf_exempt
def formulaire_view(request):
    if request.method == 'GET':
        return render(request, 'formulaire.html')
    elif request.method == 'POST':
        nom = request.POST.get('nom_complet')
        files = request.FILES.getlist('photos')

        etudiant = Etudiant.objects.create(nom_complet=nom)

        for f in files:
            Photo.objects.create(etudiant=etudiant, image=f)

        return JsonResponse({'message': 'Enregistrement réussi'})


def liste_etudiants(request):
    etudiants = Etudiant.objects.prefetch_related('photos').order_by('nom_complet')
    return render(request, 'liste_etudiant.html', {'etudiants': etudiants})


import openpyxl
from django.http import HttpResponse


from django.http import FileResponse
from io import BytesIO
from reportlab.pdfgen import canvas

def trouve_etudiant(request):
    identifiant = 'ctkionga'
    motdepasse = 'ctkionga2025'
    if request.method == 'POST':
        nom = request.POST.get('username')
        password = request.POST.get('password')
        if identifiant == nom and motdepasse ==password:
            return redirect('liste_etudiants')
        else:
            return render(request, 'formulaire.html')
    return render(request, 'trouve.html')



from io import BytesIO
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from .models import Etudiant  # ou adapte selon l'emplacement de ton modèle

def export_etudiants_pdf(request):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    largeur, hauteur = A4

    # Entête
    p.setFont("Helvetica-Bold", 14)
    p.drawCentredString(largeur / 2, hauteur - 50, "Université Président Joseph Kasa-Vubu")
    p.setFont("Helvetica", 12)
    p.drawCentredString(largeur / 2, hauteur - 75, "Cours de Biophysique, BAC 1")

    # Données des étudiants
    
    etudiants = Etudiant.objects.all().order_by('nom_complet') 
    data = [["Nom de l'Étudiant", "Cote TP", "Interro", "Examen"]]

    for etu in etudiants:
        data.append([etu.nom_complet.upper(), "", "", ""])

    # Création du tableau
    table = Table(data, colWidths=[250, 80, 80, 80])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (1, 1), (-1, -1), 'CENTER')
    ]))

    # Placement du tableau
    table.wrapOn(p, largeur, hauteur)
    table.drawOn(p, 50, hauteur - 120 - 20 * len(data))

    # Finaliser le PDF
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='etudiants.pdf')



def export_etudiants_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Étudiants"
    ws.append(['Nom complet'])

    for etudiant in Etudiant.objects.all().order_by('nom_complet'):
        ws.append([etudiant.nom_complet])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="etudiants.xlsx"'
    wb.save(response)
    return response
