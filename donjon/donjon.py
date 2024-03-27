from gpiozero import RGBLED, Button, TonalBuzzer
from time import sleep
from flask import Flask, render_template, request
import pygame, random
import math
from json import dumps



# D'abord on crée notre application Flask 
app = Flask(__name__)
data = [["nathan",32.9], ["PA", 32]]
haut = Button(20)
bas = Button(26)
gauche = Button(16)
droite = Button(21)
buzzer = TonalBuzzer(13)
enter = Button(19)
ledRGB = RGBLED(2,3,4)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':  #envoie du formulaire
        name = request.form.get('jouer')
        color = request.form.get('head')
        difficulte = request.form.get('difficulty')
        jeu(color, name, difficulte)
        return render_template("index.html", tableau=data)      
    else:
        return render_template("index.html")



@app.route('/tableau', methods=['GET'])
def get_data_tab():
    return dumps(data)
######################## pygame setup #####################

def init_jeu(hexColor):
    IMAGE = pygame.image.load("static/EPHEC.jpeg")
    TAILLE_ECRAN = IMAGE.get_size()
    TAILLE_BOULE = 10
    COULEUR_PION = (hexColor)
    COULEUR_TEXTE = (255, 255, 255)
    COULEUR_FOND = (211, 211, 211)
    MID_X = TAILLE_ECRAN[0]//2
    MID_Y = TAILLE_ECRAN[1]//2
    LARGEUR_MSG = TAILLE_ECRAN[0]//3
    HAUTEUR_MSG = TAILLE_ECRAN[1]//5
    return IMAGE,TAILLE_ECRAN,TAILLE_BOULE,COULEUR_FOND,COULEUR_PION,COULEUR_TEXTE,MID_X,MID_Y,LARGEUR_MSG,HAUTEUR_MSG

###########################################################


def jeu(couleur, nom, difficulte):
    pygame.init()
    IMAGE,TAILLE_ECRAN,TAILLE_BOULE,COULEUR_FOND,COULEUR_PION,COULEUR_TEXTE,MID_X,MID_Y,LARGEUR_MSG,HAUTEUR_MSG = init_jeu(couleur) 
    DEPLACEMENT = 150 * int(difficulte)
    set_led_color(ledRGB, couleur)
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("jeu du point")
    temps = pygame.time
    running = True
    dt = 0
    screen.blit(IMAGE, (0, 0))
    police = pygame.font.Font("font/junegull.ttf", TAILLE_ECRAN[0]//40)
    msg_debut = police.render("Essayez de placer le point rouge en plein centre de l'ecran", True, COULEUR_PION, COULEUR_FOND)
    clock = temps.Clock()

    player_pos = pygame.Vector2(random.randint(TAILLE_BOULE, (MID_X-TAILLE_BOULE)), random.randint(TAILLE_BOULE, (MID_Y-TAILLE_BOULE)))

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(IMAGE, (0, 0))
        pygame.display.update()
        
        if dt == 0:
            screen.blit(msg_debut, (LARGEUR_MSG//2, HAUTEUR_MSG//6))
            pygame.display.update()
            temps.delay(2000)

        
        pygame.draw.circle(screen, COULEUR_PION, player_pos, TAILLE_BOULE)

        if haut.is_pressed():
            player_pos.y -= DEPLACEMENT * dt
        if bas.is_pressed():
            player_pos.y += DEPLACEMENT * dt
        if gauche.is_pressed():
            player_pos.x -= DEPLACEMENT * dt
        if droite.is_pressed():
            player_pos.x += DEPLACEMENT * dt
        if enter.is_pressed():
            pos_finale = (player_pos.x, player_pos.y)
            diff = (MID_X - pos_finale[0], MID_Y - pos_finale[1])
            string_l1 = f"Horizontalement, vous êtes à  {round(abs(diff[0]))} pixels du centre"
            string_l2 = f"Verticalement, vous êtes à {round(abs(diff[1]))} pixels du centre"
            string_l3 = f"SCORE = {hypothenuse(diff[0],diff[1])}"
            msg_fin_l1 = police.render(string_l1, True, COULEUR_TEXTE, COULEUR_FOND)
            msg_fin_l2 = police.render(string_l2, True, COULEUR_TEXTE, COULEUR_FOND)
            msg_fin_l3 = police.render(string_l3, True, COULEUR_TEXTE, COULEUR_FOND)
            screen.blit(msg_fin_l1, (LARGEUR_MSG//2, HAUTEUR_MSG//6))
            screen.blit(msg_fin_l2, (LARGEUR_MSG//2, HAUTEUR_MSG//3))
            screen.blit(msg_fin_l3, (LARGEUR_MSG//2, 1.5*HAUTEUR_MSG//3))
            pygame.display.update()
            temps.delay(3000)
            
            score = hypothenuse(diff[0],diff[1])
            nom_deja_present(data, nom=nom, score=score)

            pygame.quit()
            return tableau_html()


        # flip() the display to put your work on screen
        pygame.display.update()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000
    

def hypothenuse(x,y):
    return round(math.sqrt(x*x + y*y),2)
  

def mkTab(raws):
    return f"""
        <table>
            <thead>
                <tr>
                    <th> tag </th>
                    <th> score </th>
                </tr>
            </thead>
            
            <tbody>
                {raws}
            </tbody>
        </table>
"""

def mkTr(tag, score):
    return f"""
        <tr>
            <td> {tag} </td>
            <td> {score} </td>
        </tr>
        """
def nom_deja_present(liste, nom, score):
    # Parcourir la liste
    for element in liste:
        # Vérifier si le nom est déjà présent dans la liste
        if element[0] == nom:
            if score > element[1]:
                element[1] = score  
    liste.append([nom, score])

def tableau_html():
    body = ""
    for donnee in data:
        body += mkTr(donnee[0],donnee[1])
    return mkTab(body)

def hex_to_rgb(hex_string):
    # Assurez-vous que la chaîne hexadécimale est correctement formatée
    hex_string = hex_string.strip('#')
    
    # Séparez les composantes R, G et B
    red = int(hex_string[0:2], 16) / 255.0
    green = int(hex_string[2:4], 16) / 255.0
    blue = int(hex_string[4:6], 16) / 255.0
    
    return red, green, blue



def set_led_color(led, hex_color):
    rgb_color = hex_to_rgb(hex_color)
    led.color = rgb_color
    
    
app.run(host='0.0.0.0', port=8000)