import telebot
import requests

bot_token = "The bot token"
bot = telebot.TeleBot(bot_token, parse_mode=None)


def request_hanedl_by_ip(text):     #to get info from IP address from API
    response = requests.get("http://ip-api.com/json/" + str(text).lower() + "?fields=53049")
    return response


def request_handle_by_name(text):   #to get info from a name from API
    response = requests.get("https://restcountries.eu/rest/v2/name/" + str(text) + "?fullText = true")
    return response


@bot.message_handler(commands=['start', 'help'])   #This is for when /help or /start has been given
def send_welcome(message):
    bot.reply_to(message, "Hello this bot can give you information about countries enter ip address or country name")


@bot.message_handler(regexp="^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)(\.(?!$)|$)){4}$")       #to know when user enters IP address
def check_by_ip(message):
    response = request_hanedl_by_ip(message.text)
    tmpstring = ""          #for pretty formatting
    utilities = ['country', 'regionName', 'city', 'isp']    #the wanted info
    my_dict = {}
    for item in utilities:
        my_dict[item] = response.json()[item]       #pour the dict with info gotten from API
    for key, value in my_dict.items():
        tmpstring = tmpstring + "{0:<20} {1}".format(key, value) + "\n"
    bot.send_message(message.chat.id, str(tmpstring))
    bot.send_photo(message.chat.id, "https://www.countryflags.io/" + str(request_handle_by_name(response.json()['country']).json()[0]['alpha2Code']) + "/flat/64.png")
    # this api did not have country alpha2code so we use the other one to get it from its name inside this API

@bot.message_handler(func=lambda message: True, content_types=['text'])     #when any text is entered
def hello_message(message):
    tmpstring = ""
    response = request_handle_by_name(message.text)
    utilities = ['name', 'population', 'capital', 'alpha2Code', 'region', 'currencies', 'subregion']
    my_dict = {}
    for item in utilities:
        my_dict[item] = response.json()[0][item]
    for key, value in my_dict.items():
        tmpstring = tmpstring + "{0:<20} {1}".format(key, value) + "\n"
    bot.send_message(message.chat.id, str(tmpstring))
    bot.send_photo(message.chat.id, "https://www.countryflags.io/" + response.json()[0]['alpha2Code'] + "/flat/64.png")
    print(response.json())


bot.polling()
