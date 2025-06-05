from django.urls import path
from . import views

urlpatterns = [
    path("", views.formulaire_view, name='upload_etudiant'),
    path('etudiants_doc/', views.liste_etudiants, name='liste_etudiants'),
    path('export/excel/', views.export_etudiants_excel, name='export_excel'),
    path('export/pdf/', views.export_etudiants_pdf, name='export_pdf'),
    path("trouver", views.trouve_etudiant, name='etudiant')


]


