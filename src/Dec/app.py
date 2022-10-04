import toga
from toga.style.pack import *
import requests
import json



def search_card(name):
   name = name.replace(' ','%20')
   response = requests.get('https://us.api.blizzard.com/hearthstone/cards?locale=en_US&access_token=EU6xNtrx69b7CaCX2ZDycZo2u6EL15lFxZ&textFilter=' + name)
   dict = json.loads(response.text)
   if len(dict['cards']) == 0:
      return -1
   else:
      return dict['cards'][0]


def build(app):
   box = toga.Box()
   name_label = toga.Label('Name:', style=Pack(text_align=LEFT))
   name_input = toga.TextInput()
   salute_label = toga.Label("", style=Pack(text_align=LEFT))



   def button_handler(widget):
      # salute_label.text = "Hello " + name_input.value
      card = search_card(name_input.value)
      if card == -1:
         salute_label.text = "carte non trouvée"
      else:
         salute_label.text = card['name']
         my_image = toga.Image(card['image'])
         view = toga.ImageView(id='view1', image=my_image)
         view.style.update(height=200)
         box.add(view)

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

   box.style.update(direction=COLUMN, width=1000, height=1000, padding_top=10)





   return box




def main():
   return toga.App('DeckMaker', "deck_maker", startup=build)


if __name__ == '__main__':
   main().main_loop()