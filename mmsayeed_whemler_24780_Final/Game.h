#pragma once
#include "Deck.h"
#include "Hand.h"
#include "Player.h"
#include <string>
#include"fssimplewindow.h"
#include <iostream>
#include <chrono>
#include "DrawingUtilNG.h"
#include "StringPlus.h"

using namespace std;

class Game {
private:

	// constants
	const double PI = 3.1415927;

	// User Inputs

	int trueCount;

	Deck* deck;
	int numPlayers;
	int gameSpeed = 100;						// This sets how fast the cards are drawn

	vector<Player*> players;
	Player* dealer;
	double timeElapsed;
	int gameMode;
	int playerIndex;

	bool insurance;

	GraphicFont Fonts;
	
	// In Game Tools

	int playerTurn;
	
public:
	// Textures for pngs

	GLuint textures[13][4], miscTexture[10]; // misc1 is background, misc2 is shade
	YsRawPngDecoder png[13][4], miscPng[10];

	
	// User Input Logic
	int key;
	bool gameRunning;
	

	Game(int n, int p);

	// Console Functions
	
	void printMenu();

	void printPlayerPrompt(int n, Player* P);

	void printGameState(bool countHidden = false);

	void printRecord();
	
	void printMoney();
	
	
	// Game Functions
	
	void dealRound(int gameMode);

	void checkGameState(bool finalCheck = false);
	
	void clearHand();

	void manage();					// Main Function


	// Graphics

	void loadHelper(string fileName, YsRawPngDecoder& decodeFile, GLuint& textureFile);

	void loadTextures();

	void drawBackground(int version);

	void drawCardsAuto(Player* player);			// Used for card Counting Practice
	

	// Misc

	string getStringFromScreen();

	int getIntFromScreen();

	int promptCount();
	
};
