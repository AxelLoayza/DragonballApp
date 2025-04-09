from django.urls import path
from .views import characters_list,create_character,update_character,delete_character,importar_manual,filtrar_personajes,audio_page

urlpatterns = [
    path('characters/', characters_list, name='characters_list'),
    path('characters/new/',create_character,name="create_character"),
    path('characters/edit/<int:character_id>/',update_character,name="update_character"),
    path('characters/delete/<int:character_id>/',delete_character,name="delete_character"),
    path('characters/importar/', importar_manual, name='importar_manual'),
    path('filtrar/', filtrar_personajes, name='filtrar_personajes'),
    path("audio/", audio_page, name="audio_page"), 
]
