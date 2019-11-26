from django.shortcuts import render, get_object_or_404, redirect
from .forms import MoveForm
from .models import Animal, Equipement

# Create your views here.
def animal_list(request):
    animals = Animal.objects.filter()
    return render(request, 'animalerie/animal_list.html', {'animals': animals})

def animal_detail(request, id_animal, message="OK"):
    animal = get_object_or_404(Animal, id_animal=id_animal)
    lieu = animal.lieu
    ancien_lieu = get_object_or_404(Equipement, id_equip=lieu.id_equip)
    if request.method == "POST":
        form = MoveForm(request.POST, instance=animal)
        if form.is_valid():
            form.save(commit=False)
            nouveau_lieu = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)
            update = True
            if animal.lieu.id_equip == "mangeoire" :
                if animal.lieu.disponibilite == "libre" and animal.etat == "affamé":
                    ancien_lieu.disponibilite = "libre"
                    animal.etat = "repus"
                    nouveau_lieu.disponibilite = "occupé"
                elif animal.etat != "affamé":
                    message = "désolé, l'animal n'a pas faim!"
                    update = False
                else:
                    message = "désolé, la mangeoire est occupée!"
                    update = False
            elif animal.lieu.id_equip == "roue":
                if animal.etat == "affamé":
                    message = "désolé, l'animal est affamé!"
                    update = False
                elif animal.lieu.disponibilite == "libre":
                    ancien_lieu.disponibilite = "libre"
                    animal.etat = "fatigué"
                    nouveau_lieu.disponibilite = "occupé"
                else:
                    message = "désolé, la roue est occupée"
                    update = False
            elif animal.lieu.id_equip == "nid":
                if animal.lieu.disponibilite == "libre" and animal.etat == "fatigué":
                    ancien_lieu.disponibilite = "libre"
                    animal.etat = "endormi"
                    nouveau_lieu.disponibilite = "occupé"
                elif animal.etat != "fatigué":
                    message = "désolé, l'animal n'est pas fatigué!"
                    update = False
                else:
                    message = "désolé, le nid est occupé"
                    update = False
            else:
                ancien_lieu.disponibilite = "libre"
                animal.etat = "affamé"
            print("ancien lieu", ancien_lieu, ancien_lieu.disponibilite)
            print("nouveau lieu", animal.lieu, nouveau_lieu.disponibilite)
            print(message)
            if update:
                animal.save()
                ancien_lieu.save()
                nouveau_lieu.save()
            return redirect('animal_detail_mes', id_animal=id_animal, message=message)
    else:
        form=MoveForm()


    return render(request,
                  'animalerie/animal_detail.html',
                  {'animal': animal, 'lieu': lieu, 'form': form, 'message': message})





