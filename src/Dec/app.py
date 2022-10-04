import toga
from toga.style.pack import *
import requests
import json


deck = []
requested_cards = []


def set_requested_cards(tab):
   global requested_cards  # Needed to modify global copy of globvar
   requested_cards = tab


def get_requested_cards():
   return requested_cards

def search_card(name):
   name = name.replace(' ','%20')
   response = requests.get('https://us.api.blizzard.com/hearthstone/cards?locale=en_US&access_token=EUk1x8qqMHqMox6x3uNVb0hjiPiKOvwKAV&textFilter=' + name)
   dict = json.loads(response.text)
   if len(dict['cards']) == 0:
      return -1
   else:
      return dict['cards']

def image_handler(widget):
   print(widget.id)
   print(get_requested_cards()[int(widget.id)]['name'])
def build(app):
   box = toga.Box()
   name_label = toga.Label('Name:', style=Pack(text_align=LEFT))
   name_input = toga.TextInput()
   salute_label = toga.Label("", style=Pack(text_align=LEFT))

   def create_visualisation_cartes(my_image, index):
      image_et_boutton = toga.Box()
      image_et_boutton.style.update(direction=COLUMN, width = 200, height = 500)
      view = toga.ImageView(id='viewcarte', image=my_image)
      view.style.update(width=200)
      button = toga.Button('Add card', on_press=image_handler, id=str(index))
      image_et_boutton.add(view, button)
      image_et_boutton.add(view, button)
      conteneur_image.add(image_et_boutton)

   def button_handler(widget):
      # salute_label.text = "Hello " + name_input.value
      set_requested_cards(search_card(name_input.value))
      if get_requested_cards() == -1:
         salute_label.text = "carte non trouvée"
      else:
         index = 0
         while index != len(get_requested_cards()):

            my_image = toga.Image(get_requested_cards()[index]['image'])
            create_visualisation_cartes(my_image, index)
            index += 1












   button = toga.Button('Salute', on_press=button_handler)


   button.style.padding = 20
   button.style.flex = 1
   name_label.style.update(width=100, padding_left=10)
   name_input.style.update(width=100, padding_top=10, padding_left=10)

   salute_label.style.update(width=100, padding_top=10, padding_left=10)



   box.add(name_label)
   box.add(name_input)
   box.add(salute_label)
   box.add(button)

   conteneur_image = toga.Box()
   conteneur_image.style.update(direction=ROW, padding=10, alignment='center', width=1000, height=400)
   box.add(conteneur_image)



   box.style.update(direction=COLUMN, width=1000, height=1000, padding_top=10)





   return box




def main():
   return toga.App('DeckMaker', "deck_maker", startup=build)


if __name__ == '__main__':
   main().main_loop()