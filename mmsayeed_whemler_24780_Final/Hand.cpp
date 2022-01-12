#include "Hand.h"

using namespace std;

Hand::Hand(int cash) {
	bet = cash;
}

void Hand::calcPoints() {
	int p = 0;
	bool oneAce = false;								
	for (card* nextCard : playerHand) {
		if (!nextCard->hidden) {							// Don't calculate hidden cards points
			// check if need to use alternate scoring
			if (nextCard->value == 1) {						// If an Ace is present
				oneAce = true;
				p += 1;
			}
			// face cards each worth 10
			else if (nextCard->value > 10)
				p += 10;
			else
				p += nextCard->value;
		}
	}
	altPoints = p;
	points = p;
	if (oneAce) altPoints += 10;
}

int Hand::getPoints() {			// Function that checks hand points and which value of "Ace" should be used
	calcPoints();
	if (altPoints > 21) {
		return points;
	}
	else {
		return altPoints;
	}
}

void Hand::addCardToHand(card* newCard) {
	if (playerHand.size()>0)
		newCard->angOff = playerHand[0]->angOff;
	playerHand.push_back(newCard); // PROBLEM HERE SOLVED
	
}

void Hand::clearHand() {
	playerHand.resize(0);
}

bool Hand::splittable() {							// Checks if hand is splittable
	if ((playerHand.size() == 2) && (playerHand.at(0)->value == playerHand.at(1)->value)) {
		return true;
	}
	else {
		return false;
	}
}

bool Hand::isBlackjack() {							// Checks if there is a blackjack
	if (playerHand.size() != 2) return false;
	else if (getPoints() == 21) return true;
	else return false;
}

bool Hand::canDoubleDown() {						// Checks if player can double down
	if (playerHand.size() != 2) return false;
	if (getPoints() >= 9 && getPoints() <= 11) return true;
	else return false;
}

bool Hand::isSoftHand() {
	if (playerHand.size() != 2) return false;
	else if ((playerHand.at(0)->value == 1) && (playerHand.at(1)->value != 10)) return true;
	else if ((playerHand.at(1)->value == 1) && (playerHand.at(0)->value != 10)) return true;
	else return false;
}

bool Hand::busted() {							// Checks if hand has lost
	if (getPoints() > 21) return true;
	else return false;
}

bool Hand::at21() {
	if (getPoints() == 21) return true;
	else return false;
}



// THis function calls on print card for each card in a given hand
void Hand::drawHandOnScreen(int playerN, GLuint textures[13][4], GLuint shadeTexture, YsRawPngDecoder png[13][4], bool dealer, bool split) {
	int n = 0;
	
	for (card* currCard : playerHand) {
		if (!currCard->hidden) {
			if (split) currCard->printAltOnScreen(playerN, n, cardScale, textures, shadeTexture, png, dealer);
			else currCard->printOnScreen(playerN, n, cardScale, textures, shadeTexture, png, dealer);
			n++;
		}
	}
}

// This function allows cards to rotate in the arc as the next players turn arrives
void Hand::changeTurn(int playerNumber, bool immediate) {
	for (card* currCard : playerHand) {
		if(immediate)
			currCard->angOff = (-playerNumber) * currCard->phi;
		else {
			if (currCard->angOff > (-playerNumber) * currCard->phi) {				// increment angle by 0.02 until it gets to the desired spot
				currCard->angOff -= 0.02;
			}
			else if (currCard->angOff < (-playerNumber) * currCard->phi) {
				currCard->angOff += 0.02;
			}
			if (abs(currCard->angOff + playerNumber * currCard->phi) <= 0.02) {
				currCard->angOff = (-playerNumber) * currCard->phi;
			}
		}
	}
}

void Hand::shadeHand() {										// Turn hand shaded if it is lost
	for (card* currCard : playerHand)
		currCard->lost = true;
}
