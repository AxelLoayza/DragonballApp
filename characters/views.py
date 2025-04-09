from django.shortcuts import render,redirect,get_object_or_404
import requests , json
from .models import Character
from .forms import CharacterForm 
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

API_URL = "https://dragonball-api.com/api/characters?limit=1000"

from django.shortcuts import render
from .models import Character



def import_api_characters():
    response = requests.get(API_URL)

    if response.status_code == 200:
        try:
            api_characters = response.json() 
            characters_list = api_characters.get("items", [])  

            
            if not isinstance(characters_list, list):
                print("Error: La API no devolvió una lista válida.")
                return
            
            for char in characters_list:
                print(f"Claves disponibles en personaje {char.get('name', 'Sin nombre')}: {char.keys()}")  

            for char in characters_list:
                ki_text = char.get("ki", "No disponible")
                max_ki_text = char.get("maxKi", "No disponible") 
                obj, created = Character.objects.get_or_create(
                    name=char["name"],
                    defaults={  
                        "race": char.get("race", ""),
                        "gender": char.get("gender", ""),
                        "ki": ki_text,  
                        "max_ki": max_ki_text,
                        "image": char.get("image", ""),
                        "description": char.get("description", ""),
                        "affiliation": char.get("affiliation", ""),
                        "origin_planet": char.get("origin_planet", "")
                    }
                )

                if not created:  
                    obj.ki = ki_text
                    obj.max_ki = max_ki_text
                    obj.save(update_fields=['ki', 'max_ki'])
                    obj.save()

            print(" Importación completada con éxito.")

        except Exception as e:
            print(f"Error al procesar los datos de la API: {e}")



def format_ki(value):

    value = value.replace(".", "")  
    num = int(value) if value.isdigit() else 0
    
    if num >= 1_000_000_000:
        return f"{num // 1_000_000_000} mil millones"
    elif num >= 1_000_000:
        return f"{num // 1_000_000} millones"
    elif num >= 1_000:
        return f"{num // 1_000} mil"
    else:
        return str(num)

def convert_large_ki(value):

    conversion_map = {
        "Septillion": 1_000_000_000_000_000_000_000,
        "Trillion": 1_000_000_000_000,
        "Billion": 1_000_000_000,
        "Million": 1_000_000,
    }

    for unit, factor in conversion_map.items():
        if unit in value:  
            number_part = int(value.split(" ")[0])  
            return number_part * factor  

    return value  


def characters_list(request):
    characters = Character.objects.all()  

    return render(request, "dbz/characters_list.html", {"characters": characters})


def create_character(request):
    db_characters =list(Character.objects.all())
    
    if request.method == "POST":
        form = CharacterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("characters_list")
        else:
            print("Errores en el formulario:",form.errors)
    else:
        form = CharacterForm()
    return render(request, "dbz/character_form.html", {"form": form})


def update_character(request, character_id):
    character = get_object_or_404(Character, id=character_id)
    if request.method == "POST":
        form = CharacterForm(request.POST, instance=character)
        if form.is_valid():
            form.save()
            return redirect("characters_list")
    else:
        form = CharacterForm(instance=character)
    return render(request, "dbz/character_form.html", {"form": form})


def delete_character(request, character_id):
    character = get_object_or_404(Character, id=character_id)
    if request.method == "POST":
        character.delete()
        return redirect("characters_list")
    return render(request, "dbz/character_confirm_delete.html", {"character": character})




def update_api_character(request, character_id):
    if request.method == "POST":
        data = request.POST.dict()  
        response = requests.put(f"{API_URL}/{character_id}", json=data)
        if response.status_code == 200:
            return redirect("characters_list")
    return render(request, "dbz/api_character_form.html")

def importar_manual(request):
    import_api_characters()
    return redirect("characters_list")


def filtrar_personajes(request):
    nombre = request.GET.get('nombre', '')
    raza = request.GET.get('raza', '')

    characters = Character.objects.all()

    if nombre:
        characters = characters.filter(name__icontains=nombre) 
    if raza:
        characters = characters.filter(race=raza)  

    return render(request, 'dbz/characters_list.html', {'characters': characters})

def audio_page(request):
    return render(request, "dbz/audio.html")

def favorites_view(request):
    favorite_ids = list(request.session.get("favorites", {}).keys())
    favorites = Character.objects.filter(id__in=favorite_ids)
    return render(request, "dbz/favorites.html", {"favorites": favorites})

def add_favorite(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            character_id = str(data.get("character_id"))

            if character_id:
                favorites = request.session.get("favorites", {})
                if character_id in favorites:
                    del favorites[character_id]  
                else:
                    favorites[character_id] = True  

                request.session["favorites"] = favorites
                request.session.modified = True
                return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False})
