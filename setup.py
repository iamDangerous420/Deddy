import os
import sys
import json
import pip

h = "info.json"
if not os.path.exists(h):
    with open(h, "w") as f:
        writeJ = '{"PREFIX": "None", "TOKEN": "None", "GAME": "None", "DEV_MODE": "False", "FIRST_SETUP": "True", "OWNER": "None"}'
        parse = json.loads(writeJ)
        f.write(json.dumps(parse, indent=4, sort_keys=True))
        f.truncate()
else:
    print("Starting with current info.json")

with open("info.json") as f:
    config = json.load(f)

INTERACTIVE_MODE = not len(sys.argv) > 1


win = os.name == "nt"

def wait():
    if INTERACTIVE_MODE:
        input("Press enter to continue.")


def user_choice():
    return input("> ").lower().strip()


def menu():
    while True:
        print("Options :\nType a # and i will guide you through it!")
        print("1. Set Bot Token")
        print("2. Set The Bots Global Prefix")
        print("3. Set Bot Owner ID")
        print("4. Install Requirements")
        print("5. Login game.")
        print("6. Developer mode.")
        print("7. Run Bot")

        choice = user_choice()
        if choice == "1":
            with open(h, "r+"   ) as f:
                configg = json.load(f)
                token = input("Please paste your application token here: ")
                configg["TOKEN"] = token
                f.seek(0)
                f.write(json.dumps(configg, indent=4, sort_keys=True))
                f.truncate()
                print("Successfully set the token.")
                wait()
        elif choice == "2":
            with open(h, "r+") as f:
                configg = json.load(f)
                prefix = input("Type your prefered prefix for your bot: ")
                configg["PREFIX"] = prefix
                f.seek(0)
                f.write(json.dumps(configg, indent=4, sort_keys=True))
                f.truncate()
                print("Global Prefix Set!")
                wait()
        elif choice == "3":
            with open(h, "r+") as f:
                configg = json.load(f)
                id = input("Paste The Owner ID: ")
                configg["OWNER"] = id
                f.seek(0)
                f.write(json.dumps(configg, indent=4, sort_keys=True))
                f.truncate()
                print("Owner Id set!")
                wait()
        elif choice == "4":
            pip.main(['install', '-r', "req.txt"])
            wait()
        elif choice == "5":
            with open(h, "r+") as f:
                configg = json.load(f)
                g = input("Paste The playing stats ypu would like to view as so as i login: ")
                configg["GAME"] = g
                f.seek(0)
                f.write(json.dumps(configg, indent=4, sort_keys=True))
                f.truncate()
                print("Playing status set!")
                wait()
        elif choice == "6":
            with open(h, "r+") as f:
                configg = json.load(f)
                d = input("Type True to enable or False to disable dév mode.: ")
                configg["DEV_MODE"] = d
                f.seek(0)
                f.write(json.dumps(configg, indent=4, sort_keys=True))
                f.truncate()
                print("Developer status set!")
                wait()
        elif choice == "7":
            #python bot.py
            print("WP")
        elif choice == "0":
            break
        if win:
            os.system("cls")
        else:
            os.system("clear")


if __name__ == '__main__':
    menu()
#brooklyn.1.1 ref