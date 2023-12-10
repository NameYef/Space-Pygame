# Space-Pygame
2D Top-down rogue-lite space shooter with progressive difficulty built using pygame and OOP.

Can be played using one hand only

![game screenshot](./textures/space%20pygame.png)

## Requirements
* Python 3.10 or above recommended
* have pygame installed (run `pip install pygame` in terminal)
* run game.py

## How to play
- WASD to move
- Spacebar to shoot
- LShift to fire missile
- ESC to pause
- B to toggle autofire (only when autofire is activated)

## Items
* +HP
  
![heart](./textures/heartitem.png)

+10 HP when picked up

* +ATK

![attack](./textures/attackitem.png)

Each laser deducts one more enemy hp when picked up

* +SPD

![speed](./textures/speeditem.png)

Player moves slightly faster after pick up

* +LSPD

![laser speed](./textures/lspeeditem.png)

Player laser speed increases slightly after pick up

* AUTO

![auto](./textures/autoitem.png)

Enables auto firing, increases auto firing speed if auto firing is enabled already

* WEAPONUP

![upgrade](./textures/weaponupitem.png)

Increases weapon tier

* MISSILE

![missile](./textures/missileitem.png)

Increases amount of missiles in reserve

## Enemies
There are 4 types of enemies
### Fighter
![missile](./textures/enemy_basic.png)

Very fragile, and have a weak attack, but they come in a bunch

### Elite
![missile](./textures/enemy_elite.png)

Stronger than fighter, shoots more lasers and has thicker armor

### Kamikaze
![missile](./textures/kamikaze.png)

Shoots no lasers, its only goal is to die with you

### Big Boy
![missile](./textures/enemy_big.png)

The chunky one, shoots many lasers, many hp, but very slow
