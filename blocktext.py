import string


# Converts text into Discord regional character emojis
def blocktext(text):
    block_text = []
    for z in text:
        if z == '0':
            block_text.append(':zero:')
        elif z == '1':
            block_text.append(':one:')
        elif z == '2':
            block_text.append(':two:')
        elif z == '3':
            block_text.append(':three:')
        elif z == '4':
            block_text.append(':four:')
        elif z == '5':
            block_text.append(':five:')
        elif z == '6':
            block_text.append(':six:')
        elif z == '7':
            block_text.append(':seven:')
        elif z == '8':
            block_text.append(':eight:')
        elif z == '9':
            block_text.append(':nine:')
        elif z == '#':
            block_text.append(':hash:')
        elif z == '*':
            block_text.append(':asterisk:')
        elif z == '.':
            block_text.append(':record_button:')
        elif z == '<':
            block_text.append(':arrow_backward:')
        elif z == '>':
            block_text.append(':arrow_forward:')
        elif z == '?':
            block_text.append(':grey_question:')
        elif z == '!':
            block_text.append(':grey_exclamation:')
        elif z == '+':
            block_text.append(':heavy_plus_sign:')
        elif z == '-':
            block_text.append(':heavy_minus_sign:')
        elif z == '$':
            block_text.append(':heavy_dollar_sign:')
        elif z == ' ':
            block_text.append(':blue_square:')
        elif z in string.ascii_letters:
            block_text.append(':regional_indicator_' + z.lower() + ':')
    return ''.join(block_text)
