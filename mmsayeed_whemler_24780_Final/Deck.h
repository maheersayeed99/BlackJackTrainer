#pragma once
#include <vector>
#include <iostream>
#include "yspng.h"
#include <stdio.h>
#include <math.h>
#include <ctype.h>
#include "fssimplewindow.h"
#include "yssimplesound.h"

using namespace std;

class card {
public:
	const double PI = 3.1415927;
	// value: 1 = Ace, 11 = Jack, 12 = Queen, 13 = King
	int value;

	// suit: 0 = spade, 1 = hearts, 2 = clubs, 3 = diamonds
	int suit;

	bool hidden;
	bool lost;

	float xloc, yloc, theta, cardHei, cardWid;			// Card coordinates for absolute position
	float dealerYLoc = 150;
	float dealerXloc;

	float topLeftx, topLefty;							// Card coordinates for printing
	float topRightx, topRighty;
	float botLeftx, botLefty;
	float botRightx, botRighty;

	float phi = -22*PI/180;		// Card Rotation Angle
	float roty = 100;			 //Height of center of rotation
	float rotx = 530;
	float angOff = 0;

	
	card(int v, int s, bool h = false);	// card constructor

	void printCard();					// print card to console


	// OPENGL CARD DRAWING FUNCTIONS
	void printOnScreen(int player, int cardNumber, int scale, GLuint textures[13][4], GLuint shadeTexture, YsRawPngDecoder png[13][4], bool dealer = false);
	void rotateCard(float& xval, float& yval, int player);
	void printAltOnScreen(int player, int cardNumber, int scale, GLuint textures[13][4], GLuint shadeTexture, YsRawPngDecoder png[13][4], bool dealer = false);
};

class Deck {
private:
	int numDecks;
	int nextCard;

	vector<card*> deckStatic;
	vector<int> deckOrder;
	vector<int> cardOrder;
	

public:
	YsSoundPlayer theSoundPlayer;
	YsSoundPlayer::SoundData Shuffle;
	YsSoundPlayer::SoundData Deal;
	YsSoundPlayer::SoundData Chips;

	// counting cards
	int count;
	int trueCount;

	// construct deck static with n decks of cards
	Deck(int n);

	void shuffle();						//shuffle entire deck
	card* draw(bool hide = false);		// pick a new card
	void printDeckStatic();
	void printDeckOrder();
	void playChips();

	// DRAW ON SCREEN FUNCTIONS

	

	
};