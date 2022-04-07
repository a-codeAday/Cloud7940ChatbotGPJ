from cgi import print_exception
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

import os
import configparser
import logging


import random
import connection
#create connection to mysqldb
conn = connection.connect()
mycursor = conn.cursor()

from spoonacular import API
SPOON_KEY='3ee7d67b42f94c428880b12b632e1177'

from html.parser import HTMLParser
from io import StringIO

class HTMLStripper(HTMLParser):
    """Created by Eloff: https://stackoverflow.com/a/925630"""

    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = StringIO()

    def handle_data(self, data):
        self.text.write(data)

    def get_data(self):
        return self.text.getvalue()

def strip_tags(html):
    """Strips text of HTML tags to avoid telegram errors.
    Args:
        html: string, representing recipe data.
    Returns:
        Cleaned string sans html.
    """
    if not html:
        return
    stripper = HTMLStripper()
    stripper.feed(html)
    return stripper.get_data()



def main():
    # Load your token and create an Updater for your Bot
    
    config = configparser.ConfigParser()
    config.read('config.ini')
    updater = Updater(token=(config['TELEGRAM']['ACCESS_TOKEN']), use_context=True)
    dispatcher = updater.dispatcher
    


    # You can set this logging module, so you will know when and why things do not work as expected
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    
    # register a dispatcher to handle message: here we register an echo dispatcher
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("wineExamples", wineExamples_command))
    dispatcher.add_handler(CommandHandler("hungry",random_food_tg))
    dispatcher.add_handler(CommandHandler("thirsty",random_drink_tg))
    dispatcher.add_handler(CommandHandler("recipe",recipe_tg))
    dispatcher.add_handler(CommandHandler("joke",joke))
    dispatcher.add_handler(CommandHandler("pairWine",wine_pair_tg))
    dispatcher.add_handler(CommandHandler("pairDish",dish_wine_tg))
    dispatcher.add_handler(CommandHandler("joke",joke))
    dispatcher.add_handler(CommandHandler("video",video))
    
    # To start the bot:
    updater.start_polling()
    updater.idle()
    

def echo(update, context):
    reply_message = update.message.text.upper()
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text= reply_message)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Helping you helping you.\nType \n/wineExamples -Get some examples  of wine.\n/hungry -Get a random food recipe.\n/thirsty -Get a random drink recipe.\n/recipe (food ingredient) -Get a recipes with specified ingredients. \n/pairWine (dish food) -Get a Wine with specified food. \n/pairDish (dish wine) -Get ingredients with specified wine. \n/joke -Get a food joke. Funny!')
    
def wineExamples_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Here are some wines examples.\n -white_wine \n pinot_blanc \n greco \n riesling \n -red_wine \n marsala \n merlot \n dolcetto ')

###
def random_food_tg(update: Update, context: CallbackContext) -> None:
    """Send a random food from spoonacular API"""
    try:      
        client = API(SPOON_KEY)
        response = client.get_random_recipes()
        response = response.json()["recipes"][0]
        title = response['title']
        image = response['image']
        time = str(response['readyInMinutes'])
        instruction = strip_tags(response['instructions'])
        ingredient = "\n".join([i["original"] for i in response["extendedIngredients"]])
        
        update.message.reply_text('Cuisine: '+ title)
        update.message.reply_photo(image)
        update.message.reply_text('Preparation time: ' + time + ' mins')
        update.message.reply_text('Ingredients: '+ '\n' + ingredient)
        update.message.reply_text('Steps: ' + '\n' + instruction)
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /hungry')

         
def random_drink_tg(update: Update, context: CallbackContext) -> None:
    """Send a random drink from spoonacular API"""
    try:      
        client = API(SPOON_KEY)
        response = client.get_random_recipes(tags=['drink','beverage'])
        response = response.json()["recipes"][0]
        title = response['title']
        image = response['image']
        time = str(response['readyInMinutes'])
        instruction = strip_tags(response['instructions'])
        ingredient = "\n".join([i["original"] for i in response["extendedIngredients"]])
        
        update.message.reply_text('Cuisine: '+ title)
        update.message.reply_photo(image)
        update.message.reply_text('Preparation time: ' + time + ' mins')
        update.message.reply_text('Ingredients: '+ '\n' + ingredient)
        update.message.reply_text('Steps: ' + '\n' + instruction)
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /thirsty')
         

###
def recipe_tg(update: Update, context: CallbackContext) -> None:
    try:
        logging.info(context.args[0])
        ingred = context.args[0]
         
        client = API(SPOON_KEY)
        response = client.search_recipes_by_ingredients(ingredients=ingred)
        food_id = response.json()[0]['id']
        response = client.get_recipe_information(food_id).json()
        title = response['title']
        image = response['image']
        time = str(response['readyInMinutes'])
        instruction = strip_tags(response['instructions'])
        ingredient = "\n".join([i["original"] for i in response["extendedIngredients"]])

        update.message.reply_text('Cuisine: '+ title)
        update.message.reply_photo(image)
        update.message.reply_text('Preparation time: ' + time + ' mins')
        update.message.reply_text('Ingredients: '+ '\n' + ingredient)
        update.message.reply_text('Steps: ' + '\n' + instruction)
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /recipe <kw>')

def joke(update: Update, context: CallbackContext) -> None:
    try:
        sql = """SELECT joke FROM joke WHERE joke_id = %s"""  
        randomJoke_id = random.randint(0, 11)
        param = (randomJoke_id)
        
        # EXECUTE WITH PARAMS
        try:
            mycursor.execute(sql,param)
            myresult = mycursor.fetchone()
            if (myresult):
                joke = myresult[0]
                update.message.reply_text(joke)
            else:
                print("joke does not exist.")
        except:
            print("Something went wrong in selection.")

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /joke')
        
###
def wine_pair_tg(update: Update, context: CallbackContext) -> None:
    try:
        logging.info(context.args[0])
        dish = context.args[0]
         
        client = API(SPOON_KEY)
        response = client.get_wine_pairing(food=dish).json()
        paired_wines = response['pairingText']
        wine_title = response['productMatches'][0]['title']
        avg_rating = response['productMatches'][0]['averageRating']
        image = response['productMatches'][0]['imageUrl']
        link = response['productMatches'][0]['link']
        price = response['productMatches'][0]['price']
        
        update.message.reply_text('Pair Results: '+ paired_wines)
        update.message.reply_text('Wine: ' + '\n' + wine_title)
        update.message.reply_text('Average Rating: ' + '\n' + str(round(avg_rating,2)))
        update.message.reply_photo(image)
        update.message.reply_html(link)
        update.message.reply_text('Price: '+ price)

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /WinePair <kw>')
        
def dish_wine_tg(update: Update, context: CallbackContext) -> None:
    try:
        logging.info(context.args[0])
        wine = context.args[0]
        
        client = API(SPOON_KEY)
        response = client.get_dish_pairing_for_wine(wine=wine).json()
        paired_dishes = response['text']
        update.message.reply_text('Pair Results: '+ paired_dishes)
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /DishPair <kw>')

        
        
import requests      
def video(update: Update, context: CallbackContext) -> None:
    try:
        logging.info(context.args[0])
        v_ingred = context.args[0]   # /add keyword <-- this should store the keyword
        url = 'https://api.spoonacular.com/food/videos/search'+'?apiKey='+SPOON_KEY +'&query='+ v_ingred+ '&number=1'
        response = requests.get(url)
        options = response.json()
        y_id = options['videos'][0]['youTubeId']
        youtube_link = 'http://www.youtube.com/watch?v='+y_id
        
        shortTitle = options['videos'][0]['shortTitle']
        thumbnail = options['videos'][0]['thumbnail']
        
        update.message.reply_text(shortTitle)
        update.message.reply_photo(thumbnail)
        update.message.reply_text(youtube_link)
        update.message.reply_video(youtube_link)
        
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /video')        
if __name__ == '__main__':
    main()
