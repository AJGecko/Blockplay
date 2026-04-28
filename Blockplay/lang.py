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
                "highscore": "Highscore",
                "new_highscore": "New Highscore!",
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
                    "es": "Español",
                    "fr": "Français",
                    "de": "Deutsch",
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
                "volume": "Volume",
                "placeholder": "placeholder",
                "yes": "Yes",
                "no": "No",
        }

    elif selectedlang == "de":
        currentlang = {
            #main menu:
                "start": "Start",
                "exit": "Beenden",
                "info": "Info",
                "settings": "Einstellungen",
                "main_menu": "Hauptmenü",
            #pause menu:
                "resume": "Fortsetzen",
                "restart": "Neustart",
                "pause": "Pause",
            #win/lose screen:
                "your_time": "Deine Zeit",
                "highscore": "Highscore",
                "new_highscore": "Neuer Highscore!",
                "game_over": "Game Over",
                "you_won": "Gewonnen!",
            #Settings menu:
                #general
                "language": "Sprache",
                "skin": "Skin",

                #ingame
                "number_platforms": "Anzahl Plattformen",
                "difficulty": "Schwierigkeit",
                "music": "Musik",
                "test": "Test",
                
                #dropdown menu:
                    #difficulty
                    "normal": "Normal",
                    "hard": "Schwer",
                    "easy": "Leicht",
                    #language
                    "en": "English",
                    "es": "Español",
                    "fr": "Français",
                    "de": "Deutsch",
                    #skin
                    "green": "Grün",
                    "blue": "Blau",
                    "red": "Rot",
                    #color scheme
                    "color_scheme": "Farbschema",
                    "color_scheme_1": "Hellgrün",
                    "color_scheme_2": "Grün",
                    "color_scheme_3": "Blau",
                    "color_scheme_4": "Rot",
                    "color_scheme_5": "Lila",
                #debug
                "fly": "Fliegen (Debug; mit u)",
                #other
                "volume": "Lautstärke",
                "placeholder": "Platzhalter",
                "yes": "Ja",
                "no": "Nein",
        }
    elif selectedlang == "fr":
        currentlang = {
            #main menu:
                "start": "Démarrer",
                "exit": "Quitter",
                "info": "Info",
                "settings": "Paramètres",
                "main_menu": "Menu principal",
            #pause menu:
                "resume": "Reprendre",
                "restart": "Redémarrer",
                "pause": "Pause",
            #win/lose screen:
                "your_time": "Votre temps",
                "highscore": "Meilleur score",
                "new_highscore": "Nouveau record !",
                "game_over": "Game Over",
                "you_won": "You Won!",
            #Settings menu:
                #general
                "language": "Langue",
                "skin": "Skin",

                #ingame
                "number_platforms": "Nombre de plateformes",
                "difficulty": "Difficulté",
                "music": "Musique",
                "test": "Test",
                
                #dropdown menu:
                    #difficulty
                    "normal": "Normal",
                    "hard": "Difficile",
                    "easy": "Facile",
                    #language
                    "en": "English",
                    "es": "Español",
                    "fr": "Français",
                    "de": "Deutsch",
                    #skin
                    "green": "Vert",
                    "blue": "Bleu",
                    "red": "Rouge",
                    #color scheme
                    "color_scheme": "Schéma de couleurs",
                    "color_scheme_1": "Vert clair",
                    "color_scheme_2": "Vert",
                    "color_scheme_3": "Bleu",
                    "color_scheme_4": "Rouge",
                    "color_scheme_5": "Violet",
                #debug
                "fly": "Voler (Debug; avec u)",
                #other
                "volume": "Volume",
                "placeholder": "Espace réservé",
                "yes": "Oui",
                "no": "Non",
        }
    elif selectedlang == "es":
        currentlang = {
            #main menu:
                "start": "Iniciar",
                "exit": "Salir",
                "info": "Info",
                "settings": "Ajustes",
                "main_menu": "Menú principal",
            #pause menu:
                "resume": "Continuar",
                "restart": "Reiniciar",
                "pause": "Pausa",
            #win/lose screen:
                "your_time": "Tu tiempo",
                "highscore": "Puntuación más alta",
                "new_highscore": "¡Nuevo récord!",
                "game_over": "Game Over",
                "you_won": "¡Ganaste!",
            #Settings menu:
                #general
                "language": "Idioma",
                "skin": "Skin",

                #ingame
                "number_platforms": "Número de plataformas",
                "difficulty": "Dificultad",
                "music": "Música",
                "test": "Prueba",
                
                #dropdown menu:
                    #difficulty
                    "normal": "Normal",
                    "hard": "Difícil",
                    "easy": "Fácil",
                    #language
                    "en": "English",
                    "es": "Español",
                    "fr": "Français",
                    "de": "Deutsch",
                    #skin
                    "green": "Verde",
                    "blue": "Azul",
                    "red": "Rojo",
                    #color scheme
                    "color_scheme": "Esquema de color",
                    "color_scheme_1": "Verde claro",
                    "color_scheme_2": "Verde",
                    "color_scheme_3": "Azul",
                    "color_scheme_4": "Rojo",
                    "color_scheme_5": "Púrpura",
                #debug
                "fly": "Volar (Debug; con u)",
                #other
                "volume": "Volumen",
                "placeholder": "Marcador de posición",
                "yes": "Sí",
                "no": "No",
        }

updatelang()