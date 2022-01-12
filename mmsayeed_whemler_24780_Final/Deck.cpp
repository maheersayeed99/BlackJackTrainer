#include "Deck.h"
#include <iostream>
#include <random>
#include <string>

using namespace std;

card::card(int v, int s, bool h) {
	value = v;
	suit = s;
	hidden = h;				// Used with first deaker card to hide it
	lost = false;			// Used to shade card if the hand is lost
}

Deck::Deck(int n) {
	// load sounds and start player
	if (YSOK != Shuffle.LoadWav("shuffle.wav"))
		cout << "   ERROR: Unable to load shuffle.wav " << endl;

	if (YSOK != Deal.LoadWav("deal.wav"))
		cout << "   ERROR: Unable to load deal.wav " << endl;

	if (YSOK != Chips.LoadWav("Chips.wav"))
		cout << "   ERROR: Unable to load chips.wav " << endl;

	theSoundPlayer.Start();

	int count = 0;
	for (int iteration = 0; iteration < n; iteration++) {					// Build the deck
		for (int value = 1; value <= 13; value++) {
			for (int s = 0; s <= 3; s++) {
				cardOrder.push_back(count);
				card* newCard = new card(value, s);
				deckStatic.push_back(newCard);
				count++;
			}
		}
	}
	numDecks = n;
	nextCard = 0;

	count = 0;
	trueCount = 0;
	
	cout << "Shuffling..." << endl;
	shuffle();
	cout << "Done shuffling..." << endl;
}

void Deck::shuffle() {
	
	random_shuffle(cardOrder.begin(), cardOrder.end());					// random library used
	nextCard = 0;														// shuffles cardOrder which is a list of indexes the size of the deck
	theSoundPlayer.PlayOneShot(Shuffle);
}

card* Deck::draw(bool hide) {
	card* next = deckStatic.at(cardOrder.at(nextCard));				// pick next card
	nextCard++;

	theSoundPlayer.PlayOneShot(Deal);

	next->hidden = hide;

	// update count
	if (!hide) {
		if (next->value > 1 && next->value <= 6) count--;
		else if (next->value >= 10 || next->value == 1) count++;
	}

	trueCount = count / 6;

	// if less than half of cards remaining in deck, shuffle
	if (nextCard >= 52 * numDecks / 2) shuffle();

	return next;
}

void card::printCard() {									// Prints card to command console
	if (hidden) {
		cout << "\t*HIDDEN*" << endl;
		return;
	}

	string v;
	string s;
	switch (value) {
	case 1:
		v = "A";
		break;
	case 2:
		v = "2";
		break;
	case 3:
		v = "3";
		break;
	case 4:
		v = "4";
		break;
	case 5:
		v = "5";
		break;
	case 6:
		v = "6";
		break;
	case 7:
		v = "7";
		break;
	case 8:
		v = "8";
		break;
	case 9:
		v = "9";
		break;
	case 10:
		v = "10";
		break;
	case 11:
		v = "J";
		break;
	case 12:
		v = "Q";
		break;
	case 13:
		v = "K";
		break;
	}

	switch (suit) {
	case 0:
		s = "S";
		break;
	case 1:
		s = "H";
		break;
	case 2:
		s = "C";
		break;
	case 3:
		s = "D";
		break;
	}

	cout << "\t" << v << s << endl;
}



void Deck::playChips() {
	theSoundPlayer.PlayOneShot(Chips);
}


void card::rotateCard(float& xval, float& yval, int player) {			// Rotates card coordinates to make them spin around the table
	float angVal = angOff + (player * phi);

	float xvalNew = xval;
	xvalNew -= rotx;							// move center of rotation to the origin
	yval -= roty;
	xval = (xvalNew * cos(angVal)) - (yval * sin(angVal));		// rotate about origin
	yval = (xvalNew * sin(angVal)) + (yval * cos(angVal));
	xval += rotx;								// translate cards back 
	yval += roty;
}


void card::printOnScreen(int player, int cardNumber, int scale, 
	GLuint textures[13][4], GLuint shadeTexture, YsRawPngDecoder png[13][4], bool dealer) {
	
	int wid, hei;								// Get window dimensions
	FsGetWindowSize(wid, hei);

	theta = -PI / 4;							// position cards upright initially
	cardHei = png[value - 1][suit].hei / scale;		// get scaled card dimensions
	cardWid = png[value - 1][suit].wid / scale;

	if (dealer) {									// place dealer at dealer location
		yloc = dealerYLoc;
		xloc = (wid/2) + (40* cardNumber-1);
	}
	else {											// place cards initially at the bottom of the arc
		yloc = 475 + (25 * cardNumber);
		xloc = (wid / 2) + (20 * cardNumber);
	}

	topLeftx = xloc + cardWid * cos(theta);					// get coordinates of 4 points of card to draw on screen
	topLefty = yloc - cardHei * sin(theta);
	

	topRightx = xloc + cardWid * cos(theta - PI / 2.0);
	topRighty = yloc - cardHei * sin(theta - PI / 2.0);
	

	botLeftx = xloc + cardWid * cos(theta + PI / 2.0);
	botLefty = yloc - cardHei * sin(theta + PI / 2.0);
	

	botRightx = xloc + cardWid * cos(theta + PI);
	botRighty = yloc - cardHei * sin(theta + PI);
	

	if (!dealer) {												// arrange cards in an arc (THIS DOES NOT CHANGE XLOC/YLOC)
		rotateCard(topLeftx, topLefty, player);
		rotateCard(topRightx, topRighty, player);
		rotateCard(botLeftx, botLefty, player);
		rotateCard(botRightx, botRighty, player);
	}
	
	//cout << "working" << endl;

	glViewport(0, 0, wid, hei);
	glMatrixMode(GL_PROJECTION);
	glLoadIdentity();
	glOrtho(0, (float)wid - 1, (float)hei - 1, 0, -1, 1);

	glMatrixMode(GL_MODELVIEW);
	glLoadIdentity();

	glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE);
	glColor4d(1.0, 1.0, 1.0, 1.0);         // Current color is solid white

	glEnable(GL_TEXTURE_2D);
	glBindTexture(GL_TEXTURE_2D, textures[(value) - 1][suit]); // Current texture from reserved ids
	glBegin(GL_QUADS);


	glTexCoord2d(1.0, 1.0);																						// Draw at coordinates
	//glVertex2d(xloc + cardWid * cos(theta + PI), yloc - cardHei * sin(theta + PI));
	glVertex2d(botRightx, botRighty);

	glTexCoord2d(0.0, 1.0);
	//glVertex2d(xloc + cardWid * cos(theta + PI / 2.0), yloc - cardHei * sin(theta + PI / 2.0));
	glVertex2d(botLeftx, botLefty);

	glTexCoord2d(0.0, 0.0);
	//glVertex2d(xloc + cardWid * cos(theta), yloc - cardHei * sin(theta));
	glVertex2d(topLeftx, topLefty);

	glTexCoord2d(1.0, 0.0);
	//glVertex2d(xloc + cardWid * cos(theta - PI / 2.0), yloc - cardHei * sin(theta - PI / 2.0));
	glVertex2d(topRightx,topRighty);

	glEnd();

	if (lost) {						// If card is lost, print shade png on top of it

		glEnable(GL_BLEND);
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

		glViewport(0, 0, wid, hei);
		glMatrixMode(GL_PROJECTION);
		glLoadIdentity();
		glOrtho(0, (float)wid - 1, (float)hei - 1, 0, -1, 1);

		glMatrixMode(GL_MODELVIEW);
		glLoadIdentity();

		glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE);
		glColor4d(1.0, 1.0, 1.0, 1.0);         // Current color is solid white

		glEnable(GL_TEXTURE_2D);
		glBindTexture(GL_TEXTURE_2D, shadeTexture); // Current texture from reserved ids
		glBegin(GL_QUADS);


		glTexCoord2d(1.0, 1.0);								// Draw at coordinates
		glVertex2d(botRightx, botRighty);

		glTexCoord2d(0.0, 1.0);
		glVertex2d(botLeftx, botLefty);

		glTexCoord2d(0.0, 0.0);
		glVertex2d(topLeftx, topLefty);

		glTexCoord2d(1.0, 0.0);
		glVertex2d(topRightx, topRighty);

		glEnd();

		glDisable(GL_BLEND);

	}

	
}

void card::printAltOnScreen(int player, int cardNumber, int scale,
	GLuint textures[13][4], GLuint shadeTexture, YsRawPngDecoder png[13][4], bool dealer) {

	int wid, hei;								// Get window dimensions
	FsGetWindowSize(wid, hei);

	theta = -PI / 4;							// position cards upright initially
	cardHei = png[value - 1][suit].hei / scale;		// get scaled card dimensions
	cardWid = png[value - 1][suit].wid / scale;

	if (dealer) {									// place dealer at dealer location
		yloc = dealerYLoc;
		xloc = (wid / 2) + (40 * cardNumber - 1);
	}
	else {											// place cards initially at the bottom of the arc
		yloc = 575 + (25 * cardNumber);
		xloc = (wid / 2) + (20 * cardNumber);
	}

	topLeftx = xloc + cardWid * cos(theta);					// get coordinates of 4 points of card to draw on screen
	topLefty = yloc - cardHei * sin(theta);


	topRightx = xloc + cardWid * cos(theta - PI / 2.0);
	topRighty = yloc - cardHei * sin(theta - PI / 2.0);


	botLeftx = xloc + cardWid * cos(theta + PI / 2.0);
	botLefty = yloc - cardHei * sin(theta + PI / 2.0);


	botRightx = xloc + cardWid * cos(theta + PI);
	botRighty = yloc - cardHei * sin(theta + PI);


	if (!dealer) {												// arrange cards in an arc (THIS DOES NOT CHANGE XLOC/YLOC)
		rotateCard(topLeftx, topLefty, player);
		rotateCard(topRightx, topRighty, player);
		rotateCard(botLeftx, botLefty, player);
		rotateCard(botRightx, botRighty, player);
	}

	//cout << "working" << endl;

	glViewport(0, 0, wid, hei);
	glMatrixMode(GL_PROJECTION);
	glLoadIdentity();
	glOrtho(0, (float)wid - 1, (float)hei - 1, 0, -1, 1);

	glMatrixMode(GL_MODELVIEW);
	glLoadIdentity();

	glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE);
	glColor4d(1.0, 1.0, 1.0, 1.0);         // Current color is solid white

	glEnable(GL_TEXTURE_2D);
	glBindTexture(GL_TEXTURE_2D, textures[(value)-1][suit]); // Current texture from reserved ids
	glBegin(GL_QUADS);


	glTexCoord2d(1.0, 1.0);																						// Draw at coordinates
	//glVertex2d(xloc + cardWid * cos(theta + PI), yloc - cardHei * sin(theta + PI));
	glVertex2d(botRightx, botRighty);

	glTexCoord2d(0.0, 1.0);
	//glVertex2d(xloc + cardWid * cos(theta + PI / 2.0), yloc - cardHei * sin(theta + PI / 2.0));
	glVertex2d(botLeftx, botLefty);

	glTexCoord2d(0.0, 0.0);
	//glVertex2d(xloc + cardWid * cos(theta), yloc - cardHei * sin(theta));
	glVertex2d(topLeftx, topLefty);

	glTexCoord2d(1.0, 0.0);
	//glVertex2d(xloc + cardWid * cos(theta - PI / 2.0), yloc - cardHei * sin(theta - PI / 2.0));
	glVertex2d(topRightx, topRighty);

	glEnd();

	if (lost) {

		glEnable(GL_BLEND);
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

		glViewport(0, 0, wid, hei);
		glMatrixMode(GL_PROJECTION);
		glLoadIdentity();
		glOrtho(0, (float)wid - 1, (float)hei - 1, 0, -1, 1);

		glMatrixMode(GL_MODELVIEW);
		glLoadIdentity();

		glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE);
		glColor4d(1.0, 1.0, 1.0, 1.0);         // Current color is solid white

		glEnable(GL_TEXTURE_2D);
		glBindTexture(GL_TEXTURE_2D, shadeTexture); // Current texture from reserved ids
		glBegin(GL_QUADS);


		glTexCoord2d(1.0, 1.0);								// Draw at coordinates
		glVertex2d(botRightx, botRighty);

		glTexCoord2d(0.0, 1.0);
		glVertex2d(botLeftx, botLefty);

		glTexCoord2d(0.0, 0.0);
		glVertex2d(topLeftx, topLefty);

		glTexCoord2d(1.0, 0.0);
		glVertex2d(topRightx, topRighty);

		glEnd();

		glDisable(GL_BLEND);

	}


}

void Deck::printDeckStatic() {										// USED FOR TESTING
	cout << "\nDeck in static order" << endl;
	for (card* nextCard : deckStatic) {
		nextCard->printCard();
	}
}


void Deck::printDeckOrder() {										// USED FOR TESTING
	cout << "\nDeck in shuffled order" << endl;
	for (int nextIndex : cardOrder) {
		deckStatic[nextIndex]->printCard();
		//deckStatic.at(deckOrder.at(nextIndex))->printCard();
	}
}