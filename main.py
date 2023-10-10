# Packages that need to be downloaded:
# pip install discord.py
# pip install requests
# pip install fuzzywuzzy
import discord
import time
import json
import base64
import random
import os
import sys
import glob
# My own Python files
import blocktext
import lottery
import censor
import web


# Read from the config.json file
def read_config():
    file = open('config.json', 'r')
    config = json.loads(file.read())
    file.close()
    return config


# Write to the config.json file
def write_config(config):
    file = open('config.json', 'w')
    json_config = json.dumps(config, indent=4)
    file.write(json_config)
    file.close()


# Read from text file
def text_file(txt_file):
    file = open(txt_file, 'r')
    text = file.read()
    file.close()
    return text


# Stores the time that the bot was started
start_time = time.time()


# Calculates the amount of seconds between when the function was called, and the time the bot was started
# Then formats it into a readable format
def uptime():
    current_time = time.time()
    difference = int(round(current_time - start_time))
    days = int(difference / (3600*24))
    hours = int(difference % (3600*24) / 3600)
    minutes = int(difference % 3600 / 60)
    seconds = int(difference % 60)
    return 'Uptime since last restart: ' + str(days) + ' days, ' + str(hours) + ' hours, ' + str(minutes) + \
           ' minutes, ' + str(seconds) + ' seconds'


# Initiates the Discord client
client = discord.Client()


@client.event
async def on_ready():
    # Logs the login
    print(str(time.ctime()) + ' Login: ' + str(client.user))
    # Sets rich presence
    await client.change_presence(activity=discord.Game(name="type " + read_config()['command_prefix'] + 'help'))


@client.event
async def on_message(message):
    # Checks if the message came from a DM channel or a Group channel
    if isinstance(message.channel, discord.channel.DMChannel) or \
       isinstance(message.channel, discord.channel.GroupChannel):
        if message.author != client.user:
            await message.channel.send('This bot can only be used in Discord server channels. Also if you\'re sliding '
                                       'in the DMs of a Discord bot, you must be pretty desperate. So here\'s a free '
                                       'rickroll! https://www.youtube.com/watch?v=dQw4w9WgXcQ')
            return

    # Deletes message if it contains fortnite
    if censor.fortnite(message.content) and read_config()['censor']:
        print(str(time.ctime()) + ' Deleted message from ' + message.author.display_name + ': ' + message.content)
        await message.delete()
        await message.channel.send('A message from ' + message.author.display_name +
                                   ' was deleted.<@!496350622715740170>')
        return

    # Bot does not reply to itself
    if message.author == client.user:
        return

    # Replies with WHO PINGED ME if the bot gets pinged
    if client.user in message.mentions and read_config()['reply_to_pings']:
        await message.channel.send(message.author.mention + 'https://www.youtube.com/watch?v=fPq60AoPPlo')
        return

    # Message logging (only logs messages that start with command prefix)
    if message.content.startswith(read_config()['command_prefix']):
        print(str(time.ctime()) + ' Message: ' + message.author.display_name + ': ' + message.content)

    # Syntax error message
    syntax_error_message = 'Syntax error, this command needs an additional argument. Type `' + \
                           read_config()['command_prefix'] + 'help` for more info on this command.'

    # Commands disabled messages
    regular_disabled_message = 'Regular commands are currently disabled, type `' + read_config()['command_prefix'] + \
                               'help` for a list of currently available commands.'
    web_disabled_message = 'Web commands are currently disabled, type `' + read_config()['command_prefix'] + \
                           'help` for a list of currently available commands.'
    lottery_disabled_message = 'Lottery commands are currently disabled, type `' + read_config()['command_prefix'] + \
                               'help` for a list of currently available commands.'

    # Admin commands access denied message
    access_denied_message = 'You do not have access to admin commands.'

    # HELP COMMAND

    # Help (shows commands that are currently enabled to regular users, always shows all commands to admin user)
    if message.content.lower() == read_config()['command_prefix'] + 'help':
        help_text = []
        if read_config()['regular_commands'] or str(message.author) == read_config()['admin_user']:
            help_text.append(text_file('regular.txt').replace('(prefix)', read_config()['command_prefix'])
                             .replace('(argument)', read_config()['argument_separator']))
        if read_config()['web_commands'] or str(message.author) == read_config()['admin_user']:
            help_text.append(text_file('web.txt').replace('(prefix)', read_config()['command_prefix'])
                             .replace('(argument)', read_config()['argument_separator']))
        if read_config()['lottery_commands'] or str(message.author) == read_config()['admin_user']:
            help_text.append(text_file('lottery.txt').replace('(prefix)', read_config()['command_prefix'])
                             .replace('(argument)', read_config()['argument_separator']))
        if str(message.author) == read_config()['admin_user']:
            help_text.append(text_file('admin.txt').replace('(prefix)', read_config()['command_prefix'])
                             .replace('(argument)', read_config()['argument_separator']))
        if not help_text:
            help_text.append('All commands are currently disabled, this was probably done either for maintenance or '
                             'because there is a serious bug that desperately needs to be fixed.')
        await message.channel.send('\n'.join(help_text))
        return

    # SIMPLE COMMANDS (commands that do not take additional arguments, have fixed replies, and don't use message embeds)

    # Simple commands dictionary
    simple_commands = {
        # SIMPLE ADMIN COMMANDS
        'config': [json.dumps(read_config(), indent=2), 'admin_commands'],
        'files': ['---Python Files---\n`' + '\n'.join(glob.glob('*.py')) + '`\n---JSON Files---\n`' +
                  '\n'.join(glob.glob('*.json')) + '`\n---Text Files---\n`' + '\n'.join(glob.glob('*.txt')) + '`',
                  'admin_commands'],

        # SIMPLE REGULAR COMMANDS
        'time': [str(time.ctime()), 'regular_commands'],
        'rickroll': ['https://www.youtube.com/watch?v=dQw4w9WgXcQ', 'regular_commands'],
        'ussr': ['https://www.youtube.com/watch?v=U06jlgpMtQs', 'regular_commands'],
        'beemovie': ['https://cdn.discordapp.com/attachments/419074439703953411/437179464619786261/beemovie.mp4',
                     'regular_commands'],
        'uptime': [uptime, 'regular_commands', False],
        'truth or dare': [random.choice(['Truth!', 'Dare!']), 'regular_commands'],
        'about': ['**About Alex\'s Ultra Bot:**\nAlex\'s Ultra Bot is a Discord bot written in Python to replace '
                  'Alex\'s Super Bot and Alex\'s Web Bot. This bot fixes many of the issues that the previous bots had '
                  'while adding more features and improving reliability. This bot is also highy configurable, can be '
                  'easily updated remotely, and has several more features that make development and maintainance much '
                  'easier. Alex\'s Ultra Bot was launched on Wednesday, September 29, 2021 at 8:47PM.',
                  'regular_commands'],

        # SIMPLE WEB COMMANDS
        'randomud': [web.urban_dictionary_random, 'web_commands', False],

        # SIMPLE LOTTERY COMMANDS
        'lottery': [lottery.lottery, 'lottery_commands', message.author],
        'lotteryinfo': ['https://en.wikipedia.org/wiki/Powerball', 'lottery_commands'],
        'lotterydata': [lottery.my_data, 'lottery_commands', message.author],
        'deletedata': [lottery.delete_data, 'lottery_commands', message.author],
    }

    # Simple command handler
    if message.content.startswith(read_config()['command_prefix']):
        user_command = message.content.lower().replace(read_config()['command_prefix'], '', 1)
        if user_command in simple_commands:
            if simple_commands[user_command][1] == 'admin_commands':
                if str(message.author) == read_config()['admin_user']:
                    await message.channel.send(simple_commands[user_command][0])
                    return
                else:
                    await message.channel.send(access_denied_message)
                    return
            elif read_config()[simple_commands[user_command][1]] or str(message.author) == read_config()['admin_user']:
                if callable(simple_commands[user_command][0]):
                    if simple_commands[user_command][2]:
                        await message.channel.send(simple_commands[user_command][0](simple_commands[user_command][2]))
                        return
                    else:
                        await message.channel.send(simple_commands[user_command][0]())
                else:
                    await message.channel.send(simple_commands[user_command][0])
                    return
            else:
                if simple_commands[user_command][1] == 'regular_commands':
                    await message.channel.send(regular_disabled_message)
                    return
                elif simple_commands[user_command][1] == 'web_commands':
                    await message.channel.send(web_disabled_message)
                    return
                elif simple_commands[user_command][1] == 'lottery_commands':
                    await message.channel.send(lottery_disabled_message)
                    return

    # REGULAR COMMANDS

    # Rock paper scissors
    if message.content.lower().startswith(read_config()['command_prefix'] + 'rps'):
        if read_config()['regular_commands'] or str(message.author) == read_config()['admin_user']:
            try:
                user_choice = message.content.split(read_config()['argument_separator'], 1)[1]
                if user_choice.lower() == 'rock' or user_choice.lower() == 'paper' or user_choice.lower() == 'scissors':
                    bot_choice = random.choice(['rock', 'paper', 'scissors'])
                    winner = ''
                    if bot_choice == 'rock' and user_choice.lower() == 'scissors':
                        winner = '**' + client.user.display_name + '** wins!'
                    elif bot_choice == 'rock' and user_choice.lower() == 'paper':
                        winner = '**' + message.author.display_name + '** wins!'
                    elif bot_choice == 'paper' and user_choice.lower() == 'rock':
                        winner = '**' + client.user.display_name + '** wins!'
                    elif bot_choice == 'paper' and user_choice.lower() == 'scissors':
                        winner = '**' + message.author.display_name + '** wins!'
                    elif bot_choice == 'scissors' and user_choice.lower() == 'paper':
                        winner = '**' + client.user.display_name + '** wins!'
                    elif bot_choice == 'scissors' and user_choice.lower() == 'rock':
                        winner = '**' + message.author.display_name + '** wins!'
                    elif bot_choice == user_choice.lower():
                        winner = '**Tie!**'
                    await message.channel.send('**' + message.author.display_name + '**: ' + user_choice.lower() +
                                               '\n**' + client.user.display_name + '**: ' + bot_choice + '\n\n' +
                                               winner)
                    return
                else:
                    await message.channel.send('Please enter either rock, paper, or scissors after `' +
                                               read_config()['command_prefix'] + 'rps' +
                                               read_config()['argument_separator'] + '`, type `' +
                                               read_config()['command_prefix'] + 'help` for more info on this command.')
                    return
            except (ValueError, IndexError):
                await message.channel.send(syntax_error_message)
                return
        else:
            await message.channel.send(regular_disabled_message)

    # Dice
    if message.content.lower().startswith(read_config()['command_prefix'] + 'dice'):
        if read_config()['regular_commands'] or str(message.author) == read_config()['admin_user']:
            try:
                dice_number = message.content.split(read_config()['argument_separator'], 1)[1]
                if dice_number.isnumeric() and 1 <= int(dice_number) <= 648:
                    dice_reply = []
                    dice_stats = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
                    for x in range(int(dice_number)):
                        roll = random.randint(1, 6)
                        dice_reply.append(str(roll))
                        dice_stats[roll] += 1
                    await message.channel.send(', '.join(dice_reply) + '\nStats: ' + str(dice_stats))
                    return
                else:
                    await message.channel.send('Please enter a number between 1 and 648 after `' +
                                               read_config()['command_prefix'] + 'dice' +
                                               read_config()['argument_separator'] + '`, type `' +
                                               read_config()['command_prefix'] + 'help` for more info on this command.')
                    return
            except (ValueError, IndexError):
                await message.channel.send(syntax_error_message)
                return
        else:
            await message.channel.send(regular_disabled_message)
            return

    # Coin
    if message.content.lower().startswith(read_config()['command_prefix'] + 'coin'):
        if read_config()['regular_commands'] or str(message.author) == read_config()['admin_user']:
            try:
                coin_number = message.content.split(read_config()['argument_separator'], 1)[1]
                if coin_number.isnumeric() and 1 <= int(coin_number) <= 280:
                    coin_reply = []
                    coin_stats = {'Heads': 0, 'Tails': 0}
                    for y in range(int(coin_number)):
                        flip = random.choice(['Heads', 'Tails'])
                        coin_reply.append(flip)
                        coin_stats[flip] += 1
                    await message.channel.send(', '.join(coin_reply) + '\nStats: ' + str(coin_stats))
                    return
                else:
                    await message.channel.send('Please enter a number between 1 and 280 after `' +
                                               read_config()['command_prefix'] + 'coin' +
                                               read_config()['argument_separator'] + '`, type `' +
                                               read_config()['command_prefix'] + 'help` for more info on this command.')
                    return
            except (ValueError, IndexError):
                await message.channel.send(syntax_error_message)
                return
        else:
            await message.channel.send(regular_disabled_message)
            return

    # Block text
    if message.content.lower().startswith(read_config()['command_prefix'] + 'bt'):
        if read_config()['regular_commands'] or str(message.author) == read_config()['admin_user']:
            try:
                text = message.content.split(read_config()['argument_separator'], 1)[1]
                block_text = blocktext.blocktext(text)
                if block_text:
                    if len(block_text) <= 2000:
                        await message.channel.send(block_text)
                    else:
                        await message.channel.send('Message too long! Try converting something shorter.')
                        return
                else:
                    await message.channel.send('Please enter supported text after `' + read_config()['command_prefix'] +
                                               'bt' + read_config()['argument_separator'] + '`, type `' +
                                               read_config()['command_prefix'] + 'help` for more info on this command.')
                    return
            except (ValueError, IndexError):
                await message.channel.send(syntax_error_message)
                return
        else:
            await message.channel.send(regular_disabled_message)
            return

    # Base64 encode
    if message.content.lower().startswith(read_config()['command_prefix'] + 'b64encode'):
        if read_config()['regular_commands'] or str(message.author) == read_config()['admin_user']:
            try:
                text_to_encode = message.content.split(read_config()['argument_separator'], 1)[1]
                try:
                    encoded_text = base64.b64encode(text_to_encode.encode('ascii')).decode('ascii')
                    if encoded_text:
                        if len(encoded_text) <= 2000:
                            await message.channel.send(encoded_text)
                            return
                        else:
                            await message.channel.send('Message too long! Try encoding something shorter.')
                            return
                    else:
                        await message.channel.send('Please enter supported text after `' +
                                                   read_config()['command_prefix'] + 'b64encode' +
                                                   read_config()['argument_separator'] + '`, type `' +
                                                   read_config()['command_prefix'] +
                                                   'help` for more info on this command.')
                        return
                except UnicodeEncodeError:
                    await message.channel.send('Could not encode message! Make sure all characters in your message are '
                                               'ascii characters and try again.')
                    return
            except (ValueError, IndexError):
                await message.channel.send(syntax_error_message)
                return
        else:
            await message.channel.send(regular_disabled_message)
            return

    # Base64 decode
    if message.content.lower().startswith(read_config()['command_prefix'] + 'b64decode'):
        if read_config()['regular_commands'] or str(message.author) == read_config()['admin_user']:
            try:
                text_to_decode = message.content.split(read_config()['argument_separator'], 1)[1]
                try:
                    decoded_text = base64.b64decode(text_to_decode.encode('ascii')).decode('ascii')
                    if decoded_text:
                        if len(decoded_text) <= 2000:
                            await message.channel.send(decoded_text)
                            return
                        else:
                            await message.channel.send('Message too long! Try decoding something shorter.')
                            return
                    else:
                        await message.channel.send('Please enter supported text after `' +
                                                   read_config()['command_prefix'] + 'b64decode' +
                                                   read_config()['argument_separator'] + '`, type `' +
                                                   read_config()['command_prefix'] +
                                                   'help` for more info on this command.')
                        return
                except (__import__('binascii').Error, UnicodeEncodeError):
                    await message.channel.send('Could not decode message! Make sure your message is a valid base64 '
                                               'string and try again.')
                    return
            except (ValueError, IndexError):
                await message.channel.send(syntax_error_message)
                return
        else:
            await message.channel.send(regular_disabled_message)
            return

    # WEB COMMANDS

    # Urban dictionary
    if message.content.lower().startswith(read_config()['command_prefix'] + 'ud'):
        if read_config()['web_commands'] or str(message.author) == read_config()['admin_user']:
            try:
                word = message.content.split(read_config()['argument_separator'], 1)[1]
                if word != '':
                    urban_dictionary_definition = web.urban_dictionary(word)
                    await message.channel.send(urban_dictionary_definition)
                else:
                    await message.channel.send('Please enter the word you want to look up after `' +
                                               read_config()['command_prefix'] + 'ud' +
                                               read_config()['argument_separator'] + '`, type `' +
                                               read_config()['command_prefix'] + 'help` for more info on this command.')
                    return
            except (ValueError, IndexError):
                await message.channel.send(syntax_error_message)
                return
        else:
            await message.channel.send(web_disabled_message)
            return

    # Wikipedia
    if message.content.lower().startswith(read_config()['command_prefix'] + 'wiki'):
        if read_config()['web_commands'] or str(message.author) == read_config()['admin_user']:
            try:
                topic = message.content.split(read_config()['argument_separator'], 1)[1]
                if topic != '':
                    wiki_article = web.wiki(topic)
                    await message.channel.send(wiki_article)
                else:
                    await message.channel.send('Please enter the word you want to look up after `' +
                                               read_config()['command_prefix'] + 'wiki' +
                                               read_config()['argument_separator'] + '`, type `' +
                                               read_config()['command_prefix'] + 'help` for more info on this command.')
                    return
            except (ValueError, IndexError):
                await message.channel.send(syntax_error_message)
                return
        else:
            await message.channel.send(web_disabled_message)
            return

    # Weather
    if message.content.lower().startswith(read_config()['command_prefix'] + 'weather'):
        if read_config()['web_commands'] or str(message.author) == read_config()['admin_user']:
            try:
                city = message.content.split(read_config()['argument_separator'], 1)[1]
                if city != '':
                    weather = web.current_weather(city)
                    if type(weather) == str:
                        await message.channel.send(weather)
                        return
                    else:
                        await message.channel.send(embed=weather)
                        return
                else:
                    await message.channel.send('Please enter the city you want the weather for after `' +
                                               read_config()['command_prefix'] + 'weather' +
                                               read_config()['argument_separator'] + '`, type `' +
                                               read_config()['command_prefix'] + 'help` for more info on this command.')
                    return
            except (ValueError, IndexError):
                await message.channel.send(syntax_error_message)
                return
        else:
            await message.channel.send(web_disabled_message)
            return

    # News
    if message.content.lower().startswith(read_config()['command_prefix'] + 'news'):
        if read_config()['web_commands'] or str(message.author) == read_config()['admin_user']:
            try:
                topic = message.content.split(read_config()['argument_separator'], 1)[1]
                if topic != '':
                    news = web.news(topic)
                    if type(news) == str:
                        await message.channel.send(news)
                        return
                    else:
                        await message.channel.send(embed=news)
                        return
                else:
                    await message.channel.send('Please enter the topic you want news for after `' +
                                               read_config()['command_prefix'] + 'news' +
                                               read_config()['argument_separator'] + '`, type `' +
                                               read_config()['command_prefix'] + 'help` for more info on this command.')
                    return
            except (ValueError, IndexError):
                await message.channel.send(syntax_error_message)
                return
        else:
            await message.channel.send(web_disabled_message)
            return

    # ADMIN COMMANDS

    # Shutdown
    if message.content.lower() == read_config()['command_prefix'] + 'shutdown':
        if str(message.author) == read_config()['admin_user']:
            await client.change_presence(activity=discord.Game(name='Shutting down...'))
            print(str(time.ctime()) + ' Shutdown')
            quit()
        else:
            await message.channel.send(access_denied_message)
            return

    # Restart
    if message.content.lower() == read_config()['command_prefix'] + 'restart':
        if str(message.author) == read_config()['admin_user']:
            await client.change_presence(activity=discord.Game(name='Restarting...'))
            print(str(time.ctime()) + ' Restart')
            os.execv(sys.executable, ['python'] + sys.argv)
        else:
            await message.channel.send(access_denied_message)
            return

    # Send file
    if message.content.lower().startswith(read_config()['command_prefix'] + 'sendfile'):
        if str(message.author) == read_config()['admin_user']:
            try:
                file_name = message.content.split(read_config()['argument_separator'], 1)[1]
                try:
                    await message.channel.send(file=discord.File(file_name))
                    return
                except FileNotFoundError:
                    await message.channel.send('Please enter the name of one of the bot\'s files after `' +
                                               read_config()['command_prefix'] + 'sendfile' +
                                               read_config()['argument_separator'] + '`')
                    return
            except (ValueError, IndexError):
                await message.channel.send(syntax_error_message)
                return
        else:
            await message.channel.send(access_denied_message)
            return

    # Update
    if message.content.lower() == read_config()['command_prefix'] + 'update':
        if str(message.author) == read_config()['admin_user']:
            if message.attachments:
                await client.change_presence(activity=discord.Game(name='Updating...'))
                for file in message.attachments:
                    await file.save(file.filename)
                    print(str(time.ctime()) + ' Update: ' + file.filename)
                os.execv(sys.executable, ['python'] + sys.argv)
            else:
                await message.channel.send('Please attach the file to update.')
                return
        else:
            await message.channel.send(access_denied_message)
            return

    # Edit config
    if message.content.lower().startswith(read_config()['command_prefix'] + 'editconfig'):
        if str(message.author) == read_config()['admin_user']:
            try:
                value_to_edit = message.content.split(read_config()['argument_separator'], 2)[1]
                if value_to_edit in read_config():
                    try:
                        new_value = message.content.split(read_config()['argument_separator'], 2)[2]
                        config = read_config()
                        if new_value == 'true':
                            config[value_to_edit] = True
                        elif new_value == 'false':
                            config[value_to_edit] = False
                        else:
                            config[value_to_edit] = new_value
                        write_config(config)
                        print(str(time.ctime()) + ' Config edit')
                        await message.channel.send('Edit successful!\n' + json.dumps(read_config(), indent=2))
                        await client.change_presence(
                            activity=discord.Game(name='type ' + read_config()['command_prefix'] + 'help'))
                        return
                    except (ValueError, IndexError):
                        await message.channel.send('Please enter the value you wish to change the setting to after `' +
                                                   read_config()['command_prefix'] + 'editconfig' +
                                                   read_config()['argument_separator'] + 'setting' +
                                                   read_config()['argument_separator'] + '`')
                        return
                else:
                    await message.channel.send('Please enter a setting in the config file after `' +
                                               read_config()['command_prefix'] + 'editconfig' +
                                               read_config()['argument_separator'] + '`, type `' +
                                               read_config()['command_prefix'] + 'config` to view the config file.')
                    return
            except (ValueError, IndexError):
                await message.channel.send(syntax_error_message)
                return
        else:
            await message.channel.send(access_denied_message)
            return


# Reads base64 encoded token from config.json and connects to Discord
client.run(base64.b64decode(read_config()['token_base64']).decode('ascii'))
