from fltk import *
import time
import random
import sys


class Ball():
    def __init__(self, x, y, r, vitesse):
        self.x = x
        self.y = y
        self.r = r
        self.vec= [1, 1]
        self.vitesse = vitesse
    
    def somme_vecteurs(self, v1, v2):
        x1, y1 = v1
        x2, y2 = v2
        x = x1 + x2
        y = y1 + y2
        return (x, y)

    def dessine(self,ball,color):
        """
        affiche la balle avec la nouvelle position pour la deplacer
        """
        x, y, r = self.x, self.y,self.r
        efface(ball)
        cercle(x, y, r, couleur = color, remplissage = color, tag=ball)

    def deplace(self):
        """
        effectue les rebonds sur les bords de la fenêtre
        """ 
        pos = (self.x,self.y)

        if pos[0] >= largeur -self.r:
            self.vec[0]*=-1
        if pos[0] <= self.r:
            self.vec[0]*=-1
        if pos[1] >= hauteur -self.r:
            self.vec[1]*=-1
        if pos[1] <= self.r + 70:
            self.vec[1]*=-1

        pos = self.somme_vecteurs(pos, [self.vec[0]*self.vitesse,self.vec[1]*self.vitesse])

        self.x = pos[0]
        self.y = pos[1]
    
    def collision(self):
        """
        effectue les rebonds avec la plateforme
        """
        pos_ball = (self.x,self.y)
        pos_plat = ( plat.x1 , plat.y1, plat.x2) 
        bout = (pos_plat[2] - pos_plat[0]) /6
         
        if pos_ball[1]+self.r >= pos_plat[1] :

            if pos_plat[0] <= pos_ball[0] <= pos_plat[0]+bout :
                self.vec = [-1.5,-0.5]
            if pos_plat[0]+bout <= pos_ball[0] <= pos_plat[0]+bout*2 :
                self.vec = [-1,-1]
            if pos_plat[0]+bout*2 <= pos_ball[0] <= pos_plat[0]+bout*3 :
                self.vec = [-0.5,-1.5]
            if pos_plat[0]+bout*3 <= pos_ball[0] <= pos_plat[0]+bout*4 :
                self.vec = [0.5,-1.5]
            if pos_plat[0]+bout*4 <= pos_ball[0] <= pos_plat[0]+bout*5 :
                self.vec = [1,-1]
            if pos_plat[0]+bout*5 <= pos_ball[0] <= pos_plat[0]+bout*6 :
                self.vec = [1.5,-0.5]

        pos_ball = self.somme_vecteurs(pos_ball, [self.vec[0]*self.vitesse,self.vec[1]*self.vitesse])  
        self.x = pos_ball[0]
        self.y = pos_ball[1]


class Bonus():
    def __init__(self,x1,y1,nom,color):
        self.color=color
        self.nom=nom
        self.future = None
        self.x1 = x1
        self.y1 = y1
        self.go = True
        
    def big(self):
        """
        Augmente la taille de la plateforme
        """
        plat.x1 -= 50
        plat.x2 +=50
        self.future = time.time() + 3
        plat.stack +=1
        
    def move(self):
        """
        fait aparaitre un bonus
        """
        if self.go:
            y1 = self.y1+5 
            y2 = self.y1+25
            efface(self.nom)
            rectangle(self.x1+60, y1, self.x1 + 100 , y2, remplissage=self.color, epaisseur=3, tag=self.nom)
            self.y1 = y1

    def touche(self):
        """
        Verifie si on obtient le bonus ou pas avec la plateforme
        """
        x2 = self.x1 + 95
        y2 = self.y1+25
        pos = (x2,y2)
        pos_plat = (plat.x1, plat.y1, plat.x2) 

        if self.go:
            if pos[1] >= pos_plat[1] :

                if pos[0]>=pos_plat[0] and pos[0]-100 <= pos_plat[2]: 
                    self.big()
                    efface(self.nom)
                    self.go = False
                    efface(self.nom)
                    br.active = False
                    
            if pos[1] > hauteur:
                br.active = False
                self.go = False
                efface(self.nom)
                
    def add_ball(self):
        ball_1 = Ball(plat.x1,plat.y1-20,10,2)


class Brick():
    def __init__(self,colonnes,lignes,haut,diff):
        self.colonnes = colonnes
        self.lignes = lignes
        self.haut = haut
        self.larg = int((largeur-50)/colonnes)
        self.sizeX = int((largeur-50)/colonnes)
        self.sizeY = haut
        self.max_Y = 140
        self.list_coord = []
        self.touched = 0
        self.bonus_coo = None
        self.active = False
        self.pv =  5
        self.color = [None,'jaune','orange','rouge']
        self.diff = diff

    def cree_brick(self):
        """
        dessine toutes les briques et stockes leurs positions dans un liste
        chaque brique a son propre identitiant et une couleur qui correspond
        à son nombre de point de vie
        """
        id = 0
        for j in range(self.lignes):
            self.max_Y += self.haut
            self.max_X = 25
            self.pv -=1
            for i in range(self.colonnes):
                color = ['violet','rouge','orange','jaune']
                image(self.max_X, self.max_Y, 'images\image_'+self.diff+'_'+color[j]+'.png',
                    ancrage='nw', tag='b'+str(id))
                self.list_coord.append([self.max_X,self.max_Y,'b'+str(id),self.pv])
                self.max_X += self.larg
                id += 1

    def check_collision(self, nbBriques,ball):
        """
        Verifie si la balle est en collision avec une brique
        """
        for brick in self.list_coord:

            if ball.y-ball.r <= brick[1]+self.haut and ball.y > brick[1]+(self.haut - 10): #bas
                if ball.x >= brick[0] and ball.x <= brick[0]+self.larg:
                    
                    brick[3]-=1  # diminue de 1 les pv de la brique
                    if brick[3] <= 0:                 
                        efface(brick[2])
                        self.list_coord.remove(brick)
                        self.touched += 1
                    else:
                        efface(brick[2])
                        image(brick[0], brick[1], 'images\image_'+self.diff+'_'+self.color[brick[3]]+'.png',
                            ancrage='nw', tag=brick[2])
                    
                    ball.vec[1]*=-1 # rebond de la balle
                    
                    if self.active == False : # fait spawn un bonus
                        if random.random() < percentage_chance:
                            self.bonus_coo = (int(brick[0]),int(brick[1]))
                            self.active = True
            
            elif ball.y+ball.r >= brick[1] and ball.y < brick[1]+ 10: #haut
                if ball.x >= brick[0] and ball.x <= brick[0]+self.larg:

                    brick[3]-=1  # diminue de 1 les pv de la brique
                    if brick[3] <= 0:                 
                        efface(brick[2])
                        self.list_coord.remove(brick)
                        self.touched += 1
                    else:
                        efface(brick[2])
                        image(brick[0], brick[1], 'images\image_'+self.diff+'_'+self.color[brick[3]]+'.png',
                            ancrage='nw', tag=brick[2])

                    ball.vec[1]*=-1 # rebond de la balle
            
            elif ball.x-ball.r <= brick[0]+self.larg and ball.x > brick[0]: # droite
                if ball.y >= brick[1] and ball.y <= brick[1]+self.haut:

                    brick[3]-=1  # diminue de 1 les pv de la brique
                    if brick[3] <= 0:                 
                        efface(brick[2])
                        self.list_coord.remove(brick)
                        self.touched += 1
                    else:
                        efface(brick[2])
                        image(brick[0], brick[1], 'images\image_'+self.diff+'_'+self.color[brick[3]]+'.png',
                            ancrage='nw', tag=brick[2])

                    ball.vec[0]*=-1 # rebond de la balle
            
            elif ball.x + ball.r >= brick[0] and ball.x < brick[0]+ self.larg: #gauche
                if ball.y >= brick[1] and ball.y <= brick[1]+self.haut:

                    brick[3]-=1  # diminue de 1 les pv de la brique
                    if brick[3] <= 0:                 
                        efface(brick[2])
                        self.list_coord.remove(brick)
                        self.touched += 1
                    else:
                        efface(brick[2])
                        image(brick[0], brick[1], 'images\image_'+self.diff+'_'+self.color[brick[3]]+'.png',
                            ancrage='nw', tag=brick[2])

                    ball.vec[0]*=-1 # rebond de la balle
        
        efface('bricks_count')
        texte(18, 37, 'Briques détruites: '+str(self.touched)+'/'+str(nbBriques), couleur='red',
            ancrage='w', tag='bricks_count')
        return self.touched

    def remove_bricks(self):
        id = 0
        for i in range(self.lignes):
            for j in range(self.colonnes):
                efface('b'+str(id))
                id += 1


class Platform():
    def __init__ (self,x1,y1,x2,y2):
        self.x1 = x1
        self.x2 = x2
        self.y1= y1
        self.y2 = y2

        self.dep = 10 # déplacement en pixels à chaque flèche pressée
        self.dx = 0 # dernier déplacement du rectangle
        self.last_dx = 0
        self.stack = 0

    def boost (self):
        """
        Fait déplacer la plateforme plus vite
        """
        if self.last_dx < 0:
                if self.x1 - self.dep * 10 > 0:
                    self.dx = - self.dep * 10
                else:
                    self.dx = - self.x1
        elif self.last_dx > 0:
                if self.x2 + self.dep * 10 < largeur:
                    self.dx = self.dep * 10
                else:
                    self.dx = largeur - self.x2
    
    def gauche(self):
        self.dx = - self.dep
    
    def droite(self):
        self.dx = self.dep
    
    def pas_depasser(self):
        """
        Pour que la plateforme ne dépasse pas des bordures de la fenetre
        """
        if self.dx != 0 and (self.x1 > 0 or self.dx > 0) and (self.x2 < largeur or self.dx < 0):
            efface('platform')
            self.x1 += self.dx
            self.x2 += self.dx
            rectangle(self.x1, self.y1, self.x2, self.y2,couleur='white',
                remplissage='white',tag='platform')
    
    def update(self):
        self.last_dx = self.dx



# fonctions relatives au fonctionnement d'une partie
def demande_action(key):
    """
    Attend qu'une touche donnée soit pressée ou que l'utilisateur veuille quitter la fenêtre
    """
    while True:
        ev = donne_ev()
        if touche_pressee(key) or type_ev(ev) == key:
            return ev
        elif type_ev(ev) == 'Quitte':
            ferme_fenetre()
            sys.exit()
        mise_a_jour()

def info():
    texte(10, 8, 'Lancer une balle: Enter', taille=13, couleur="white",
        ancrage='nw', tag = 'info')
    texte(10, 28, 'Déplacer la plateforme: Flèche Droite/Gauche', taille=13, couleur="white",
        ancrage='nw', tag = 'info')
    texte(10, 48, 'Booster la plateforme: Clic Gauche', taille=13, couleur="white",
        ancrage='nw', tag = 'info')



largeur = 1000
hauteur = 700

cree_fenetre(largeur, hauteur)
image(largeur, hauteur, 'bg_breakout.gif', ancrage = 'se', tag = 'background')
rectangle(0, 0, largeur-1, 70, couleur='white', remplissage='black', tag='bar')


percentage_chance = 0.25 # probabilité d'apparition d'un bonus de plateforme
cur_frames = 0
cur_second = 0
running_game = False
bestTime = False

while True: # le jeu se lance

    # initialisation de la partie
    if not running_game:
        texte(18, 37, 'Difficulté:', couleur='white', ancrage='w', tag='diff')
        texte(350, 37, 'Facile', couleur='light blue', ancrage = 'center', tag='diff')
        texte(500, 37, 'Moyen', couleur='light blue', ancrage = 'center', tag='diff')
        texte(650, 37, 'Difficile', couleur='light blue', ancrage = 'center', tag='diff')

        event = demande_action('ClicGauche') # on doit appuyer sur Espace ou Quitter
        while not (ordonnee(event) < 70 and 305 < abscisse(event) < 400 or 450 < abscisse(event) < 555
                or 595 < abscisse(event) < 710): # on doit appuyer sur un des trois boutons
            event = demande_action('ClicGauche')
        efface('diff')

        if 305 < abscisse(event) < 400:
            diff = 'facile'
            ballSpeed = 1.5
            largBrick = 60
            nbCol = 3
            nbLine = 3
        elif 450 < abscisse(event) < 555:
            diff = 'moyen'
            ballSpeed = 2.25
            largBrick = 50
            nbCol = 4
            nbLine = 4
        elif 595 < abscisse(event) < 710:
            diff = 'difficile'
            ballSpeed = 3
            largBrick = 40
            nbCol = 6
            nbLine = 4

        br = Brick(nbCol,nbLine,largBrick,diff)
        br.cree_brick()

        # timer
        totalTime = 0
        efface('timer')
        
        cree=True
        ballon = False
        loot=False

        used_balls = 1
        texte(largeur-18, 37, 'Vies restantes: 3', couleur='red', ancrage='e', tag='balls_count')
        info()
        mise_a_jour()
        demande_action('Return') # on doit appuyer sur Espace ou Quitter
        

    rectangle(largeur/2-70, hauteur-25, largeur/2+70, hauteur-10, couleur='white', remplissage='white',
        tag='platform')
    plat = Platform(largeur/2-70, hauteur-25, largeur/2+70, hauteur-10)
    ball = Ball(370,490,10,ballSpeed)
    mv = False
    efface('info')

    startTime = time.time()


    # la balle se lance
    while True:
        ev = donne_ev()
        tev = type_ev(ev)


        # timer
        roundTime = float('%.1f' % (time.time() - startTime + totalTime))
        efface('timer')
        texte(largeur/2, 37, 'Temps: '+str(roundTime)+'s', couleur='white', ancrage='center', tag='timer')


        # déplacement de la plateforme
        plat.dx = 0

        if tev:
            if tev == 'Quitte':
                ferme_fenetre()
                sys.exit()
            if tev == 'ClicGauche':
                plat.boost()
            elif touche(ev) == 'Left':
                plat.gauche()
            elif touche(ev) == 'Right':
                plat.droite()

            plat.pas_depasser()
            plat.update()
        

        # bonus plateforme et bonus balle bleue
        if br.active:
            if random.randint(0,100) < 60:
                loot = True
                br.active = False
                bonus_x=br.bonus_coo[0]
                bonus_y=br.bonus_coo[1]
            else :
                bonus = Bonus(br.bonus_coo[0],br.bonus_coo[1],"big","green")
                mv = True
                br.active = False
            
        if loot == True:
            efface("ball_extra")
            rectangle(int(bonus_x), int(bonus_y), int(bonus_x)+40, int(bonus_y)+10, remplissage="blue",
                tag="ball_extra")
            
            bonus_y += 3
            if bonus_y >= hauteur-10:
                    efface("ball_extra")
                    loot=False
            if bonus_y>= plat.y1 and bonus_y<=plat.y2 and bonus_x>plat.x1 and bonus_x <= plat.x2 :
                efface("ball_extra")
                loot = False
                if cree==True or ballon == False:
                    ball_1 = Ball(plat.x1+70,plat.y1-20,10,2)
                    ballon = True
                    cree=False
        
        if ballon == True:
            nbBriques_1 = br.check_collision(nbCol*nbLine,ball_1)
            ball_1.dessine("ball_1","blue")
            ball_1.deplace() 
            ball_1.collision()
            if ball_1.y>= hauteur-30:
                efface("ball_1")
                ballon=False

        if mv:     
            bonus.move()
            bonus.touche()
              
            if bonus.future is not None:
                if time.time() > bonus.future:
                    bonus.future = None
                    plat.x1 = plat.x1 + 50*plat.stack
                    plat.x2 = plat.x2 - 50*plat.stack
                    plat.stack=0
        

        # actualisation du jeu
        touched = br.check_collision(nbCol*nbLine,ball)
        ball.dessine("ball","white")
        ball.deplace() 
        ball.collision()

        mise_a_jour()


        #compteur de fps
        if int(time.perf_counter())==cur_second: 
            cur_frames +=1 
        
        else: 
            efface('fps')
            texte(largeur-18, 90, 'fps: '+str(cur_frames),taille ='15',couleur="white",
                ancrage='e', tag = 'fps')
            cur_frames=0
            cur_second=int(time.perf_counter())
        
        clock = time.perf_counter() * 60  # measer time in 1/60 seconds
        sleep = int(clock) + 1 - clock # time till the next 1/60 
        time.sleep(sleep/60)


        # la balle touche le bas ou toutes les briques ont été touchées
        if ball.y >= hauteur - 30 or touched >= nbCol*nbLine:
            totalTime = roundTime
            efface('ball_1')
            ballon = False
            efface('ball')
            efface('bricks_count')
            efface('balls_count')
            efface('big')
            efface("ball_extra")

            # toutes les briques ont été touchées ou les 3 balles ont toutes été utilisées
            if touched >= nbCol*nbLine or used_balls == 3:

                if touched >= nbCol*nbLine: # toutes les briques ont été touchées (victoire)
                    texte(18, 37, 'VICTORY!', taille = 30, couleur="red", ancrage='w', tag = 'game')
                    if totalTime < bestTime or not bestTime:
                        bestTime = totalTime
                        efface('timer')
                        attente(0.5)
                        texte(largeur/2-50, 37, 'Nouveau Record! '+str(bestTime)+'s', couleur='yellow',
                            ancrage='center', tag='timer')

                else: # toutes les briques n'ont pas été touchées (défaite)
                    texte(18, 37, 'GAME OVER...', taille = 30, couleur="red", ancrage='w', tag = 'game')

                running_game = False #la partie est terminée
                attente(1)
                texte(largeur-18, 37, 'Clique sur Espace!', couleur="red", ancrage='e', tag='game')
                demande_action('space') # on doit appuyer sur Espace ou Quitter
                br.remove_bricks()

            else: # les 3 balles n'ont pas toutes été utilisées
                texte(largeur-18, 37, 'Vies restantes: '+str(3 - used_balls), couleur="red",
                    ancrage='e', tag = 'balls_count')
                info()
                used_balls += 1
                running_game = True # la partie est en cours, on lance juste une nouvelle manche
                demande_action('Return') # on doit appuyer sur Enter ou Quitter
            
            efface('game')
            efface('platform')
            efface('timer')
            break