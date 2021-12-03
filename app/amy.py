import re
import random

#Je kan de namen niet opvragen in de Telegram API :(((
names = ["Joost", "Yoni", "Rutger", "AmyO", "AmyL", "Thijs", "Joshiwa","Lenne"]

def get_rng(input):
    if input == "rng":
        output = "please use this function as follows: /rng@{number}, for the random number generator"
    elif "rng@" in input:
        try:
            new = re.findall(r'rng@(\w+)', input)[0]
            print(new)
            components = re.split('(\d+)',new)
            print([int(word) for word in components if word.isdigit()][0])
            output = "The magic number is :", random.randint(1,[int(word) for word in components if word.isdigit()][0])
        except:
            output = "You are probably doing something wrong, you fool. Format: /rng@{number}"
    else:
        output = "yeeez, just use it the way you is supposed to, idiot. Format: /rng@{number}"
    return output

def get_name():
    return random.choice(names)

def get_manly():
    nmb = random.randint(1,30)
    return ("8"+nmb*'='+"D")
