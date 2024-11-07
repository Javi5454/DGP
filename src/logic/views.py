from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.http import JsonResponse
from .models import Person, Pictogram, PictogramSequence

import json

# Create your views here.
def pictogram_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('person_id')
        selected_sequence = data.get('pictogram_sequence', [])

        person = get_object_or_404(Person, user__username= username)
        try:
            pictogram_sequence = PictogramSequence.objects.get(person=person)
        except:
            return JsonResponse({"error": "Secuencia de pictogramas no encontrada para esta persona."}, status=400)
        

        correct_sequence = [po.pictogram.id for po in pictogram_sequence.pictogramorder_set.all()]
        print(selected_sequence)
        print(list(map(str, correct_sequence)))

        if selected_sequence == list(map(str, correct_sequence)):
            login(request, person.user)
            return JsonResponse({"success": True, "redirect_url": "/dashboard"})
        else:
            return JsonResponse({"success": False})
        
    persons = Person.objects.filter(pictogramsequence__isnull=False)
    return render(request, 'pictogram_login.html', {'persons': persons, 'pictograms': Pictogram.objects.all()})
