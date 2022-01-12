#pragma once
#include "Deck.h"

using namespace std;

class Hand {
	
public:
	const double PI = 3.1415927;

	int cardScale = 10;
	vector<card*> playerHand;				// player hand
	int points;								// hand score
	int altPoints;							// alternate score if there is an ace
	int bet;								// ammount of money betted
	bool lost = false;

	float angOff = 0;						// angle for turning hand about arc


	Hand(int bet = 10);					// constructor

	void calcPoints();

	int getPoints();

	void addCardToHand(card* newCard);

	void clearHand();

	bool splittable();

	bool isBlackjack();

	bool canDoubleDown();

	bool isSoftHand();

	bool busted();

	bool at21();
	\




	// OPENGL DRAW HAND FUNCTIONS //

	void drawHandOnScreen(int playerN, GLuint textures[13][4], GLuint shadeTexture, YsRawPngDecoder png[13][4], bool dealer = false, bool split = false);


	void changeTurn(int playerNumber, bool immediate = false);

	void shadeHand();




	////////////////////////////////////////// CARD COUNTING ////////////////////////////////////////////////////////

};