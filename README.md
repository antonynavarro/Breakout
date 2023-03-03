# Breakout, un jeu de réaction

Classic Breakout game made in python

| ![Capture d'écran de LBreakout sur Wikipedia](breakout.jpg) |
|:--:| 
| *Capture d'écran de LBreakout sur [Wikipedia](https://fr.wikipedia.org/wiki/Fichier:Screenshot-LBreakout2.jpg)* |


## Mécanisme général

On launch, the game displays a racket at the bottom and rows of bricks at the
high, with a ball ready to be thrown at it. The game starts as soon as the
player clicks on the window, which causes the ball to be thrown into a
oblique direction. The ball can bounce off the top, left and right edges.
right of the window, and also on the bricks. After the twist on a
brick, this brick disappears immediately. When the ball hits the edge
bottom of the window, it is lost, and we start again with the launch. The only
way to avoid this situation is to control the racket (by mouse or by
keyboard) to bounce the ball blocking its descent. When the ball
is lost despite everything, we start again by throwing with a new ball.
The game ends if one of the following conditions are met :

- If the number of lost balls reaches a number fixed in advance (often 3),
  before all bricks are removed. In this case, the game is lost.
- If all the bricks are eliminated, then the game is won.

When the game ends, the result (number of bricks eliminated, time elapsed,
number of launches remaining) is displayed. The user can restart a
another part by clicking on the window.


## Bonus 

Red Bonus : adds an additional ball

Green Bonus : Makes the plateform bigger during 5 seconds 

