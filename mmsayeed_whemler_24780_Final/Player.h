#pragma once
#include "Deck.h"
#include "Hand.h"
#include "GraphicFont.h"
#include "ysglfontdata.h"


class Player {
public:
	int num; // number of player
	bool done = false;
	int record[3] = { 0,0,0 };			// win loss tie ratio

	bool splitted;
	bool doubledDown;

	Hand* hand;							// hand
	Hand* altHand;						// splitted hand
	int testInt = 3;

	int defaultBet;
	int money;

	Player(int number);

	Hand* splitHand();

	void doubleDown();

	void changeDefaultBet(int newB);

	void reset();

	void drawMoney();
};


