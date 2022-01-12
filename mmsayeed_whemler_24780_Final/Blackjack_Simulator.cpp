#include "Game.h"
#include "Player.h"
#include "Deck.h"
#include "Hand.h"
#include "iostream"
#include <string.h>
#include <ctype.h>
#include <stdio.h>
#include <math.h>
#include "yspng.h"
#include "fssimplewindow.h"


using namespace std;
int WIN_WIDTH = 1060, WIN_HEIGHT = 650, WIN_X = 5, WIN_Y = 10;				// Define window size
int numPLayers = 5;
int numDecks = 6;


int main(void)
{
	srand(unsigned(time(0)));												// random seed
	FsOpenWindow(WIN_X, WIN_Y, WIN_WIDTH, WIN_HEIGHT, 1);					// opengl open window

	
	cout << "Creating game..." << endl;

	Game Simulator = Game(numDecks, numPLayers);							// Begin game with 5 players and 6 decks

	while (true) {
		glClear(GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT);					// clear screen
		Simulator.manage();													// run game loop
		
	}
	
	return 0;

}
