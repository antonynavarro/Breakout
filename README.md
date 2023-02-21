# Breakout, un jeu de réaction

L'objectif de ce problème est de programmer en Python le jeu classique de
[Breakout](https://fr.wikipedia.org/wiki/Breakout_(jeu_vid%C3%A9o,_1976)), où le
but du joueur est d'éliminer toutes les briques alignées dans le haut de la
fenêtre en lançant et en faisant rebondir une balle par une raquette, qui peut
être déplacée horizontalement. Une balle est perdue quand la raquette n'arrive
pas à la faire rebondir. Le joueur possède d'un nombre fini de balles, et la
partie est perdue s'il y a des briques restantes quand toutes les balles sont
perdues. Une version en ligne est disponible [ici](https://elgoog.im/breakout/).

| ![Capture d'écran de LBreakout sur Wikipedia](breakout.jpg) |
|:--:| 
| *Capture d'écran de LBreakout sur [Wikipedia](https://fr.wikipedia.org/wiki/Fichier:Screenshot-LBreakout2.jpg)* |

Attention, il y a *énormément* de possibilités d'amélioration. Il est
impossible de toutes les implémenter. Soignez bien la version de base du jeu
avant de vous lancer dans de nouvelles fonctionnalités, et choisissez bien
lesquelles vous souhaitez implémenter !


## Mécanisme général

Au lancement, le jeu affiche une raquette en bas et des lignes de briques en 
haut, avec une balle prête à être lancée dessus. Le jeu commence dès que le 
joueur clique sur la fenêtre, qui entraîne le lancement de la balle dans une 
direction oblique. La balle peut rebondir sur les bords en haut, à gauche et à 
droite de la fenêtre, et aussi sur les briques. Après le rebondissement sur une
brique, cette brique disparaît tout de suite. Quand la balle touche le bord en
bas de la fenêtre, elle est perdu, et on recommence par le lancement. Le seul
moyen à éviter cette situation est de contrôler la raquette (par souris ou par
clavier) pour faire rebondir la balle en bloquant sa descente. Quand la balle
est perdue malgré tout, on recommence par le lancement avec une nouvelle balle.
Le jeu se termine si une des conditions suivantes sont remplies

- Si le nombre de balles perdues atteint un nombre fixé en avance (souvent 3),
  avant l'élimination de tous les briques. Dans ce cas là, la partie est perdue.
- Si tous les briques sont éliminées, alors la partie est gagnée.

Quand le jeu termine, le résultat (nombre de briques éliminées, temps écoulé,
nombre de lancements restant) est affiché. L'utilisateur peut recommencer une
autre partie en cliquant sur la fenêtre.

Pour l'affichage, pour assurer une visualisation fluide, il faut bien
contrôler le nombre d'images par seconde. Une valeur souvent utilisée est de
mettre à jour les positions de la balle **60** fois par seconde (autrement dit
une mise à jour toutes les 1/60 s précisément). Entre chaque mise à jour, il
faut calculer les nouvelles positions de la balle, qui peuvent être modifiées
pour deux raisons : le mouvement rectiligne dû à la vitesse de la balle, qui
est facile à calculer, et la collision avec un mur ou une brique (qui peut aussi
changer sa direction et sa vitesse), qui demande un effort. Il faut aussi
mettre à jour les briques restantes.

Pour détecter les collisions, à chaque mise à jour on vérifie si la balle rentre
en collision avec un bord ou une des briques. Si le centre de la balle rentre à
une distance inférieur au rayon de la balle avec un bord de la fenêtre, un côté
d'une brique ou le bord supérieur de la raquette, alors il y a une
collision.

Pour calculer les changements suite à la collision, il y a deux façons de
faire :

- Façon facile mais imprécise : calculer la nouvelle vitesse à partir de la
  position courante, même si la distance est strictement inférieure à la vraie
  distance de collision (ce qui signifie que la collision aurait du déjà se
  passer entre deux mises à jour).
- Façon plus difficile mais précise (optionnelle) : calculer la nouvelle
  vitesse **et** la nouvelle position de manière plus réaliste, en tenant
  compte de la proportion du déplacement normal qui peut s'effectuer avant
  collision, et de la proportion restante après collision. Avec un peu de
  réflexion, ce n'est pas trop difficile à faire pour les rebonds sur un bord
  rectiligne.

Il est conseillé d'écrire une fonction qui vérifie si la balle est en collision
avec un segment rectiligne donnée.


## Bonus et malus (optionnel)

Dans certaines versions de Breakout, quand une brique est éliminée, il pourrait
y avoir un bonus ou un malus qui tombe et qui peut être capturé par la raquette
pour prendre effet. Pour une brique contenant un bonus ou un malus, il est
conseillé d'y afficher un symbole pour donner une indication au joueur.

Voici quelques bonus et malus possibles:

- Ajouter un lancement restant
- Faire perdre immédiatement la balle courante, et forcer un nouveau lancement
- Faire scinder toute balle dans la fenêtre en deux
- Rendre la balle "invincible" pour quelques secondes, pendant lesquelles la
  balle traverse les briques et les élimine sans rebondissement
- Rendre la balle plus grande ou plus petite pour quelques secondes
- Rallonger ou raccourcir la raquette pour quelques secondes
- Rendre la raquette à la longueur maximale pour quelques secondes
- Ralentir ou accélérer la balle
- Faire réapparaître quelques briques déjà éliminées


## Autres extensions optionnelles possibles (liste non exhaustive)

- Ajustement de difficulté du jeu en réglant la vitesse initiale, le nombre de 
  briques et la configuations des briques, choix parmi plusieurs difficultés
  possibles.
- Enregistrement des meilleurs résultats, catégorisé par mode et par difficulté.
- Cocotte minute : accélération progressive de la balle.
- Briques renforcées : certaines briques nécessitent plusieures collisions pour
  être éliminées
- Angle variant : l'angle de réflection sur la raquette dépend de la position de
  contact
- Calcul précis des collisions.
- Génération aléatoire de la configuration initiale des briques.


## Récapitulatif (partie obligatoire)

Dans la version de base du problème, il vous est donc demandé d'implémenter :

- Les collisions de la balle avec les briques et les bords ;
- La bonne implantation du mécanisme du jeu.

Par ailleurs le jeu doit être stable et agréable à jouer, et l'animation
fluide.
