#include "Player.h"

using namespace std;

Player::Player(int number) {
	splitted = false;
	doubledDown = false;
	done = false;
	defaultBet = 10;
	num = number;
	money = 100;
	hand = new Hand(defaultBet);
}

Hand* Player::splitHand() {				// Split a hand if both cards are initially the same
	if (hand->playerHand.size() == 2 && (hand->playerHand.at(0)->value == hand->playerHand.at(1)->value)) {
		// split is allowed
		altHand = new Hand(hand->bet);
		(altHand->playerHand).push_back(hand->playerHand.back());
		hand->playerHand.pop_back();
		splitted = true;

		return altHand;
	}
	else {
		return nullptr;
	}
}

void Player::doubleDown() {
	if (hand->canDoubleDown()) {
		int newB = (hand->bet * 2);
		hand->bet = newB;
		doubledDown = true;
	}
}

void Player::changeDefaultBet(int newB) {
	defaultBet = newB;
}

void Player::reset() {						// reset player stats
	money = 100;
	defaultBet = 10;
}

void Player::drawMoney() {

}