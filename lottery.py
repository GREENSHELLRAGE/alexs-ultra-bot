import json
import random
import time


# Read from the lotterydata.json file
def read_lotterydata():
    file = open('lotterydata.json', 'r')
    lotterydata = json.loads(file.read())
    file.close()
    return lotterydata


# Write to the lotterydata.json file
def write_lotterydata(lotterydata):
    file = open('lotterydata.json', 'w')
    lotterydata['last_updated'] = str(time.ctime())
    json_lotterydata = json.dumps(lotterydata, indent=4)
    file.write(json_lotterydata)
    file.close()


# Generates numbers for each ticket
def generate_numbers():
    num_list = []
    for x in range(5):
        while True:
            rand_num = random.randint(1, 69)
            if num_list.count(rand_num) == 0:
                num_list.append(rand_num)
                break
    num_list.sort()
    num_list.append(random.randint(1, 26))
    return num_list


# Compares two sets of lottery numbers and calculates money
def get_money(drawn, ticket):
    matching_numbers = 0
    matching_powerballs = 0
    for x in range(5):
        if drawn[x] == ticket[x]:
            matching_numbers += 1
    if drawn[5] == ticket[5]:
        matching_powerballs += 1
    if matching_numbers == 0 and matching_powerballs == 1 or matching_numbers == 1 and matching_powerballs == 1:
        return [matching_numbers, matching_powerballs, 4]
    elif matching_numbers + matching_powerballs == 3:
        return [matching_numbers, matching_powerballs, 7]
    elif matching_numbers + matching_powerballs == 4:
        return [matching_numbers, matching_powerballs, 100]
    elif matching_numbers == 4 and matching_powerballs == 1:
        return [matching_numbers, matching_powerballs, 50000]
    elif matching_numbers == 5 and matching_powerballs == 0:
        return [matching_numbers, matching_powerballs, 1000000]
    elif matching_numbers + matching_powerballs == 6:
        return [matching_numbers, matching_powerballs, 768400000]
    else:
        return [matching_numbers, matching_powerballs, 0]


# Runs the lottery simulation, returns the result and the money won, and saves the current game to lotterydata.json
def lottery(user):
    # Picks ticket and lottery numbers and calculates money won
    drawn_numbers = generate_numbers()
    ticket_numbers = generate_numbers()
    results = get_money(drawn_numbers, ticket_numbers)
    matching_numbers = results[0]
    matching_powerballs = results[1]
    money = results[2]

    # Loads the lottery data
    lottery_data = read_lotterydata()
    # Saves the current game to user's data
    try:
        lottery_data[str(user)]['money_won'] += money
        lottery_data[str(user)]['times_played'] += 1
    except KeyError:
        lottery_data.update({str(user): {'money_won': money, 'times_played': 1}})
    # Saves the new data
    write_lotterydata(lottery_data)
    # Returns the reply text
    return '**' + user.display_name + '**\nYour ticket numbers: ' + str(drawn_numbers) + \
           '\nThe lottery numbers: ' + str(ticket_numbers) + '\nMatching numbers: ' + str(matching_numbers) + \
           '\nMatching Powerballs: ' + str(matching_powerballs) + '\nMoney won: $' + str(money) + \
           '\n**Your Data:**\nTotal money won: $' + str(lottery_data[str(user)]['money_won']) + \
           '\nTotal times played: ' + str(lottery_data[str(user)]['times_played'])


# Shows the user's data
def my_data(user):
    # Loads the lottery data
    lottery_data = read_lotterydata()

    # Returns the user's data
    try:
        return 'Lottery data for **' + user.display_name + ':**\nTotal money won: $' + \
               str(lottery_data[str(user)]['money_won']) + '\nTotal times played: ' + \
               str(lottery_data[str(user)]['times_played'])
    except KeyError:
        return 'There is no lottery data for **' + user.display_name + '**.'


# Deletes the user's data
def delete_data(user):
    # Loads the lottery data
    lottery_data = read_lotterydata()

    # Deletes the user's data
    try:
        lottery_data.pop(str(user))
        write_lotterydata(lottery_data)
        return 'The lottery data for **' + user.display_name + '** has been deleted.'
    except KeyError:
        return 'There is no lottery data for **' + user.display_name + '**.'
