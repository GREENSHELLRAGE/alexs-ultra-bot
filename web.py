import requests
import discord
import re


# Urban Dictionary
def urban_dictionary(word_to_look_up):
    # Gets data from Urban Dictionary and handles any errors
    try:
        response = requests.get('https://api.urbandictionary.com/v0/define?term=' + word_to_look_up, timeout=(2, 3))
        response.raise_for_status()
        response.close()
    except requests.exceptions.Timeout:
        return 'Urban Dictionary took too long to respond. Try again. If this problem keeps happening, try again later.'
    except requests.exceptions.HTTPError as e:
        return ':warning:**An Error Occurred!**\nAn error occurred while looking up the definition of this word. ' \
               'Try another word. If this problem keeps happening, try again later.\n**Error Details:**\n' + str(e)
    except requests.exceptions.ConnectionError as e:
        return ':warning:**An Error Occurred!**\nAn error occurred while connecting to Urban Dictionary. ' \
               'Try again later.\n**Error Details:**\n' + str(e)
    # Looks for definition in the list of definitions that is shorter than 2000 characters
    list_of_definitions = response.json()['list']
    if list_of_definitions:
        for x in list_of_definitions:
            word = x['word'].replace('[', '').replace(']', '')
            definition = x['definition'].replace('[', '').replace(']', '')
            example = x['example'].replace('[', '').replace(']', '')
            if len('**' + word + '**\n\n**Definition:**\n' + definition + '\n\n**Examples:**\n' + example) <= 2000:
                return '**' + word + '**\n\n**Definition:**\n' + definition + '\n\n**Examples:**\n' + example
    else:
        return 'There is no definition for this word on Urban Dictionary. Try another word!'


# Urban Dictionary random
def urban_dictionary_random():
    # Gets data from Urban Dictionary and handles any errors
    try:
        response = requests.get('https://api.urbandictionary.com/v0/random', timeout=(2, 3))
        response.raise_for_status()
        response.close()
    except requests.exceptions.Timeout:
        return 'Urban Dictionary took too long to respond. Try again. If this problem keeps happening, try again later.'
    except requests.exceptions.HTTPError as e:
        return ':warning:**An Error Occurred!**\nAn error occurred while looking up a random definition. ' \
               'Try another word. If this problem keeps happening, try again later.\n**Error Details:**\n' + str(e)
    except requests.exceptions.ConnectionError as e:
        return ':warning:**An Error Occurred!**\nAn error occurred while connecting to Urban Dictionary. ' \
               'Try again later.\n**Error Details:**\n' + str(e)
    # Looks for definition in the list of definitions that is shorter than 2000 characters
    list_of_definitions = response.json()['list']
    for x in list_of_definitions:
        word = x['word'].replace('[', '').replace(']', '')
        definition = x['definition'].replace('[', '').replace(']', '')
        example = x['example'].replace('[', '').replace(']', '')
        if len('**' + word + '**\n\n**Definition:**\n' + definition + '\n\n**Examples:**\n' + example) <= 2000:
            return '**' + word + '**\n\n**Definition:**\n' + definition + '\n\n**Examples:**\n' + example


# Current weather
def current_weather(city):
    # Gets current weather data from WeatherAPI.com and handles any errors
    try:
        url = "https://weatherapi-com.p.rapidapi.com/current.json"
        querystring = {"q": city}
        headers = {
            'x-rapidapi-host': "weatherapi-com.p.rapidapi.com",
            'x-rapidapi-key': "15511b16cbmsh1f65be95837033dp132bbfjsna6fc7ea28269"
        }
        response = requests.request("GET", url, headers=headers, params=querystring, timeout=(2, 3))
        response.raise_for_status()
        response.close()

        weather_data = response.json()
        if not weather_data:
            return 'There is no weather for this city. Try another city!'
        location = weather_data['location']['name']
        country = weather_data['location']['country']
        image_url = weather_data['current']['condition']['icon']
        condition = weather_data['current']['condition']['text']
        temperature = weather_data['current']['temp_c']
        last_updated = weather_data['current']['last_updated']
        embed = discord.Embed(title='**' + location + ', ' + country + '**',
                              description='Weather from [WeatherAPI.com](https://www.weatherapi.com/)')
        embed.set_thumbnail(url='https:' + image_url)
        embed.add_field(name=str(temperature) + '°C',
                        value=condition, inline=False)
        embed.set_footer(text='Last updated: ' + last_updated)
        return embed
    except requests.exceptions.Timeout:
        return 'WeatherAPI took too long to respond. Try again. If this problem keeps happening, try again later.'
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 400:
            return 'There is no weather for this city. Try another city!'
        else:
            return ':warning:**An Error Occurred!**\nAn error occurred while looking up the weather. Try again. ' \
                   'If this problem keeps happening, try again later.\n**Error Details:**\n' + str(e)
    except requests.exceptions.ConnectionError as e:
        return ':warning:**An Error Occurred!**\nAn error occurred while connecting to WeatherAPI. ' \
               'Try again later.\n**Error Details:**\n' + str(e)


# News
def news(topic):
    # Gets current news data from NewsCatcher api and handles any errors
    try:
        url = "https://free-news.p.rapidapi.com/v1/search"
        querystring = {"q": topic, "lang": "en", "page": "1", "page_size": "10"}
        headers = {
            'x-rapidapi-host': "free-news.p.rapidapi.com",
            'x-rapidapi-key': "15511b16cbmsh1f65be95837033dp132bbfjsna6fc7ea28269"
        }
        response = requests.request("GET", url, headers=headers, params=querystring, timeout=(2, 3))
        response.raise_for_status()
        response.close()

        breaking_news = response.json()
        try:
            embed = discord.Embed(title='**News for: ' + topic + '**',
                                  description='News from [NewsCatcher API](https://newscatcherapi.com/)')
            for x in breaking_news['articles']:
                try:
                    embed.add_field(name=':red_circle:',
                                    value='[**' + x['title'] + '**](' + x['link'] + ')\n' +
                                    x['summary'][0:150].replace('\n\n', '\n') +
                                    '...\n\nSource: ' + x['clean_url'] + '\nPublished on: ' + x['published_date'],
                                    inline=False)
                except TypeError:
                    continue
            return embed
        except KeyError:
            return 'There is no news for this topic. Try another topic!'
    except requests.exceptions.Timeout:
        return 'NewsCatcher API took too long to respond. Try again. If this problem keeps happening, try again later.'
    except requests.exceptions.HTTPError as e:
        return ':warning:**An Error Occurred!**\nAn error occurred while looking up the news. Try again. ' \
               'If this problem keeps happening, try again later.\n**Error Details:**\n' + str(e)
    except requests.exceptions.ConnectionError as e:
        return ':warning:**An Error Occurred!**\nAn error occurred while connecting to NewsCatcher API. ' \
               'Try again later.\n**Error Details:**\n' + str(e)


def wiki(topic):
    try:
        url = "https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=" + topic + "&format=json"
        response = requests.request("GET", url, timeout=(2, 3))
        response.raise_for_status()
        response.close()

        try:
            article = response.json()
            title = article['query']['search'][0]['title']
            snippet = re.sub(re.compile('<.*?>'), '', article['query']['search'][0]['snippet'])
            pageid = article['query']['search'][0]['pageid']
            print(title + '\n' + snippet)
            return '**' + title + '**\n\n' + snippet + '...' + '\n\nhttps://en.wikipedia.org/?curid=' + str(pageid)
        except IndexError:
            return 'There is no Wikipedia article for this topic. Try another topic!'
    except requests.exceptions.Timeout:
        return 'Wikipedia took too long to respond. Try again. If this problem keeps happening, try again later.'
    except requests.exceptions.HTTPError as e:
        return ':warning:**An Error Occurred!**\nAn error occurred while looking up the article. Try again. ' \
               'If this problem keeps happening, try again later.\n**Error Details:**\n' + str(e)
    except requests.exceptions.ConnectionError as e:
        return ':warning:**An Error Occurred!**\nAn error occurred while connecting to Wikipedia. ' \
               'Try again later.\n**Error Details:**\n' + str(e)
