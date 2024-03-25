# from gpiozero import LED, Button, TonalBuzzer
# from time import sleep
from flask import Flask, render_template, request
import pygame, random
import math

# D'abord on crée notre application Flask 
app = Flask(__name__)
pygame.init()
# avancer = Button(26)
# reculer = Button(20)
# gauche = Button(21)
# droite = Button(16)
# buzzer = TonalBuzzer(19)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        color = request.form.get('head')
        image = request.form.get('imageSelect')
        if image is not None:
            image = image.value
        score = jeu(color,image)
        return f"Score: {score}"
    else:
        jeu('#e66465', 'static/img1.png')
        return render_template("index.html")




######################## pygame setup #####################

def init_jeu(hexColor,background):
    IMAGE = pygame.image.load(background)
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


def jeu(couleur, image):
    IMAGE,TAILLE_ECRAN,TAILLE_BOULE,COULEUR_FOND,COULEUR_PION,COULEUR_TEXTE,MID_X,MID_Y,LARGEUR_MSG,HAUTEUR_MSG = init_jeu(couleur,image) 
    screen = pygame.display.set_mode(TAILLE_ECRAN)
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
            temps.delay(4000)

        
        pygame.draw.circle(screen, COULEUR_PION, player_pos, TAILLE_BOULE)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player_pos.y -= 150 * dt
        if keys[pygame.K_DOWN]:
            player_pos.y += 150 * dt
        if keys[pygame.K_LEFT]:
            player_pos.x -= 150 * dt
        if keys[pygame.K_RIGHT]:
            player_pos.x += 150 * dt
        if keys[pygame.K_RETURN]:
            pos_finale = (player_pos.x, player_pos.y)
            diff = (MID_X - pos_finale[0], MID_Y - pos_finale[1])
            string_l1 = f"Horizontalement, vous êtes à {round(abs(diff[0]))} pixels du centre"
            string_l2 = f"Verticalement, vous êtes à {round(abs(diff[1]))} pixels du centre"
            msg_fin_l1 = police.render(string_l1, True, COULEUR_PION, COULEUR_FOND)
            msg_fin_l2 = police.render(string_l2, True, COULEUR_PION, COULEUR_FOND)
            screen.blit(msg_fin_l1, (LARGEUR_MSG//2, HAUTEUR_MSG//6))
            screen.blit(msg_fin_l2, (LARGEUR_MSG//2, HAUTEUR_MSG//6 + HAUTEUR_MSG//6))
            pygame.display.update()
            temps.delay(3000)
            pygame.quit()


        # flip() the display to put your work on screen
        pygame.display.update()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000
    
    pygame.quit()
    return hypothenuse(diff[0],diff[1])



def hypothenuse(x,y):
    return math.sqrt(x*x + y*y)


def mktr(td):
    return f"<tr>{td}</tr>"

def mktd(txt):
    return f"<td>{txt}</td>"







app.run(host='0.0.0.0', port=8000)