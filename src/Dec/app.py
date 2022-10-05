from io import BytesIO

import toga
from toga.style.pack import *
import requests
import json
from toga.constants import TRANSPARENT
from PIL import Image, ImageFont, ImageDraw



deck = []
requested_cards = []


def set_requested_cards(tab):
   global requested_cards  # Needed to modify global copy of globvar
   requested_cards = tab


def get_requested_cards():
   return requested_cards

def search_card(name):
   name = name.replace(' ','%20')
   response = requests.get('https://us.api.blizzard.com/hearthstone/cards?locale=en_US&access_token=EUIF2G9N5gGcTVYLVhPwDsbecgKIdgAu57&textFilter=' + name)
   dict = json.loads(response.text)
   if len(dict['cards']) == 0:
      return -1
   else:
      return dict['cards']


def build(app):
   parent_box=toga.Box()
   search_box=toga.Box()
   deck_box=toga.Box()
   parent_box.add(search_box, deck_box)
   parent_box.style.update(direction=ROW)


   name_input = toga.TextInput()
   salute_label = toga.Label("", style=Pack(text_align=LEFT))


   def create_img_with_text(clicked_carte):
      response = requests.get(clicked_carte['cropImage'])
      img = Image.open(BytesIO(response.content))
      d1 = ImageDraw.Draw(img)

      font = ImageFont.truetype("commando.ttf", 22)
      d1.text((5, 20), clicked_carte['name'], fill='white', font=font)
      buffer = BytesIO()
      img.save(buffer, format='png', compress_level=0)

      image_from_bytes = toga.Image(data=buffer.getvalue())
      return toga.ImageView(id='crop_image', image=image_from_bytes)



   def image_handler(widget):
      clicked_carte = get_requested_cards()[int(widget.id)]
      result_view = create_img_with_text(clicked_carte)


      deck_and_name_box = toga.Box()
      deck_and_name_box.style.update(width=300, height=30, direction=COLUMN)
      
      deck_and_name_box.add(result_view)
      deck_box.add(deck_and_name_box)







   def create_visualisation_cartes(my_image, index):
      image_et_boutton = toga.Box()
      image_et_boutton.style.update(direction=COLUMN, width = 200, height = 500)
      view = toga.ImageView(id='viewcarte', image=my_image)
      view.style.update(width=200)
      button = toga.Button('Add card', on_press=image_handler, id=str(index))
      button.style.update(padding_top = -200, width = 20, padding_left = 100)
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

   name_input.style.update(width=100, padding_top=10, padding_left=10)

   salute_label.style.update(width=100, padding_top=10, padding_left=10)




   search_box.add(name_input)
   search_box.add(salute_label)
   search_box.add(button)

   conteneur_image = toga.Box()
   conteneur_image.style.update(direction=ROW, padding=10, alignment='center', width=1000, height=400)
   search_box.add(conteneur_image)
   search_box.style.update(direction=COLUMN, width=500, height=1000, padding_top=10)

   return parent_box

def main():
   return toga.App('DeckMaker', "deck_maker", startup=build)

if __name__ == '__main__':
   main().main_loop()