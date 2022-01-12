#pragma once
#include "fssimplewindow.h"
#include "ysglfontdata.h"
#include "Deck.h"
#include "Hand.h"
#include "Player.h"
#include "Game.h"

#include <string>
#include <iostream>


class gameManager {
private:
	int key;
public:
	gameManager();
	void manage();
};