from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import F, ExpressionWrapper, fields
from django.db import connection, transaction
from .models import Emprunt, Livre
from django.utils import timezone
from .forms import NewLoanForm
from django.views.decorators.csrf import csrf_exempt
from .forms import ReturnLoanForm


@csrf_exempt
def loan(request):
    user_id = request.session.get('user_id')
    emprunts = []
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id_livre, date_emprunt, date_retour_prevue, date_retour_effectif, livres.titre FROM emprunt JOIN livres on id_livre=livres.id WHERE id_utilisateur = %s", [user_id])
            rows = cursor.fetchall()
            for row in rows:
                emprunt = {
                    'id_livre': row[0],
                    'date_emprunt': row[1],
                    'date_retour_prevue': row[2],
                    'date_retour_effectif': row[3],
                    'titre': row[4],
                }
                emprunts.append(emprunt)
    except DatabaseError as e:
        print("An error occurred while fetching the loans: {}".format(e))
    return render(request, 'loan.html', {'emprunts': emprunts})

@csrf_exempt
def new_loan(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')  # Redirige vers la page de connexion si l'utilisateur n'est pas connecté

    # Get available book choices
    book_choices = []
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, titre FROM livres WHERE statut = 'disponible'")
            rows = cursor.fetchall()
            for row in rows:
                book_choices.append((row[0], row[1]))
    except DatabaseError as e:
        print("An error occurred while fetching the available books: {}".format(e))

    if request.method == 'POST':
        form = NewLoanForm(request.POST, book_choices=book_choices)
        if form.is_valid():
            book_id = form.cleaned_data['book_id']
            date_retour = form.cleaned_data['date_retour']
            try:
                with transaction.atomic(), connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO emprunt (id_utilisateur, id_livre, date_emprunt, date_retour_prevue) VALUES (%s, %s, NOW(), %s)",
                        [user_id, book_id, date_retour]
                    )
                    cursor.execute("UPDATE livres SET statut = 'emprunté' WHERE id = %s", [book_id])
                    return redirect('loan')  # Redirige vers la page des emprunts après un emprunt réussi
            except DatabaseError as e:
                print("An error occurred while creating the loan: {}".format(e))
                form.add_error(None, "Une erreur est survenue lors de la création de l'emprunt.")
    else:
        form = NewLoanForm(book_choices=book_choices)

    return render(request, 'new_loan.html', {'form': form})

@csrf_exempt
def return_loan(request):
    user_id = request.session.get('user_id')

    # Get ongoing loan choices
    emprunt_choices = []
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, id_livre FROM emprunt WHERE id_utilisateur = %s AND date_retour_effectif IS NULL", [user_id])
            rows = cursor.fetchall()
            for row in rows:
                emprunt_choices.append((row[0], row[1]))
    except DatabaseError as e:
        print("An error occurred while fetching the loans: {}".format(e))

    if request.method == 'POST':
        form = ReturnLoanForm(request.POST, emprunt_choices=emprunt_choices)
        if form.is_valid():
            emprunt_id = form.cleaned_data['emprunt_id']
            try:
                with transaction.atomic(), connection.cursor() as cursor:
                    cursor.execute("UPDATE emprunt SET date_retour_effectif = NOW() WHERE id = %s AND id_utilisateur = %s", [emprunt_id, user_id])
                    cursor.execute("UPDATE livres SET statut = 'disponible' WHERE id = (SELECT id_livre FROM emprunt WHERE id = %s)", [emprunt_id])
                    return redirect('loan')
            except DatabaseError as e:
                print("An error occurred while returning the loan: {}".format(e))
    else:
        form = ReturnLoanForm(emprunt_choices=emprunt_choices)

    return render(request, 'return_loan.html', {'form': form, 'emprunts_en_cours': emprunt_choices})