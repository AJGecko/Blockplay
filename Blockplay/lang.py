selectedlang = "en"
currentlang = {}

#set current language to a language
def setlang(lang):
    global selectedlang
    selectedlang = lang

#get current language
def getlang():
    global selectedlang
    return selectedlang

#update currentlang based on selectedlang
def updatelang():
    global currentlang, selectedlang
    if selectedlang == "en":
        currentlang = {

            #main menu:
                "start": "Start",
                "exit": "Exit",
                "info": "Info",
                "settings": "Settings",
                "main_menu": "Main Menu",
            #pause menu:
                "resume": "Resume",
                "restart": "Restart",
                "pause": "Pause",
            #win/lose screen:
                "your_time": "Your Time",
                "game_over": "Game Over",
                "you_won": "You Won",
            #Settings menu:
                #general
                "language": "Language",
                "skin": "Skin",

                #ingame
                "number_platforms": "Number of platforms",
                "difficulty": "Difficulty",
                "music": "Music",
                "test": "Test",
                
                #dropdown menu:
                    #difficulty
                    "normal": "Normal",
                    "hard": "Hard",
                    "easy": "Easy",
                    #language
                    "en": "English",
                    "es": "Spanish",
                    "fr": "French",
                    "de": "German",
                    #skin
                    "green": "Green",
                    "blue": "Blue",
                    "red": "Red",
                    #color scheme
                    "color_scheme": "Color Scheme",
                    "color_scheme_1": "Light Green",
                    "color_scheme_2": "Green",
                    "color_scheme_3": "Blue",
                    "color_scheme_4": "Red",
                    "color_scheme_5": "Purple",
                
                #debug
                "fly": "Fly (Debug; with u)",
                #other
                "placeholder": "placeholder",
                "yes": "Yes",
                "no": "No",
        }

updatelang()