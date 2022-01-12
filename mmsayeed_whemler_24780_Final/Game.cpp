#include "Game.h"
#include "DrawingUtilNG.h"
#include "yssimplesound.h"
using namespace std;


Game::Game(int n, int p) {

	glClear(GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT);
	loadHelper("loading.png", miscPng[3], miscTexture[3]);
	drawBackground(3);
	Fonts.init();
	Fonts.setColorRGB(250, 0, 0);
	
	deck = new Deck(n);							// make new deck
	
	numPlayers = p;								// specify how many players in game

	for (int i = 0; i < numPlayers; i++) {	
		Player* newPlayer = new Player(i+1);		// make new players
		players.push_back(newPlayer);			
	}

	dealer = new Player(0);						// make dealer
	insurance = false;

	gameRunning = true;							// Start game loop
	gameMode = 0;								// Set game mode to menu

	/////// SOUND ////////
	
	
	FsSwapBuffers();
	loadTextures();								// Load Textures
	printMenu();
}

void Game::dealRound(int mode) {
	// make sure all hands cleared 
	clearHand();

	// players place bets

	// initial 2 cards
	for (int i = 0; i < 2; i++) {
		// deal two cards;

		for (Player* nextPlayer : players) {
			card* nextCard = deck->draw();					// pick new card
			nextPlayer->hand->addCardToHand(nextCard);		// add card to hand of current player
			int playerCount = 0;							// current player number

			glClear(GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT);				// clear screen
			drawBackground(mode);										
			for (Player* printPlayer : players) {

				FsPollDevice();
				key = FsInkey();

				if (key == FSKEY_M) {
					gameMode = 0;
					goto endFunc;
				}
				printPlayer->hand->changeTurn((players.size()) / 2, true);
				printPlayer->hand->drawHandOnScreen(playerCount, textures, miscTexture[2], png);			// draw all hands
				playerCount++;
			}
			
			FsSwapBuffers();
			FsSleep(gameSpeed);								// wait before next card is drawn before printing
			
			
		}
	
		
	}
endFunc: {}

	// dealers 2 cards
	card* nextCard = deck->draw();
	dealer->hand->addCardToHand(nextCard);
	//cout << "Current CArd Count is " << deck->count << endl;
	nextCard = deck->draw(true);								// Second Dealer Card is hidden
	dealer->hand->addCardToHand(nextCard);
	//cout << "Current CArd Count is " << deck->count << endl;

	//printGameState();											// Print Game state and Score So Far

	// INSURANCE BETS
	if (dealer->hand->getPoints() == 11) {
		// insert insurance betting here
		// dealer peaks if other card is a 10
	}

}

void Game::printGameState(bool countHidden) {
	cout << endl;
	cout << "Dealer Hand:" << endl;
	for (card* nextCard : (dealer->hand->playerHand)) {
		//s =
			nextCard->printCard();
	}
	cout << "Dealer total: " << dealer->hand->getPoints() << endl;
	// if card up is an Ace, allow insurance
	if (dealer->hand->getPoints() == 11) {
		insurance = true;
		cout << "Dealer Ace: allowing insurance" << endl;
	}
	
	int n = 1;													// iterate Number of Players
	for (Player* nextPlayer : players) {
		cout << "Player " << n << " Hand:" << endl;
		for (card* nextCard : (nextPlayer->hand->playerHand)) { 
			nextCard->printCard();
		}

		// Print if hand is splittable
		if (nextPlayer->hand->splittable() == true) { cout << "Hand is splittable!" << endl; }

		// Print if player can Double Down  
		// NOTE: cannot double down AND split
		if (nextPlayer->hand->canDoubleDown() == true) { cout << "You can double down!" << endl; }

		// Print if hand is Blackjack
		if (nextPlayer->hand->isBlackjack() == true) { 
			cout << "BlackJack!" << endl;
			int newB = nextPlayer->hand->bet * (3 / 2);
			nextPlayer->hand->bet = newB;
		}
		else if (nextPlayer->hand->isSoftHand() == true) { cout << "Soft " << nextPlayer->hand->getPoints() << endl; }

		// alternate hand (splitted)
		if (nextPlayer->splitted) {
			cout << "Player " << n << " SPLIT Hand:" << endl;
			for (card* nextCardA : (nextPlayer->altHand->playerHand)) {
				//s = 
				nextCardA->printCard();
				//cout << "\t" << s << endl;
			}
		}
		cout <<"Player "<< n << " total: " << nextPlayer->hand->getPoints() << endl << endl;
		n++;
	}
	cout << endl << endl;

	if (!countHidden)
		cout << "COUNT: " << deck->count << endl;
}

void Game::printMenu() {															// Console function

	cout << "Press M to Open Main Menu" << endl;
	cout << "Press B to Start BlackJack Game" << endl;
	cout << "Press C to Practice Running Count" << endl;
	cout << "Press S to Simulate Strategy" << endl;
	cout << endl << endl;
}

void Game::printPlayerPrompt(int n, Player* P) {									// Console function
	printGameState();
	cout << "Player " << P->num << " What would you like to do?"<< endl;
	cout << "Press 1 to hit" << endl;
	cout << "Press 2 to stand" << endl;
	if (P->hand->splittable()) cout << "Press 3 to split your hand" << endl;
	if (P->hand->canDoubleDown()) cout << "Press 4 to double down" << endl;
	if (insurance) cout << "Press 5 to input Insurance bet" << endl;
	cout << endl;
}



void Game::checkGameState(bool finalCheck) {
	for (Player* currPlayer : players) {
		

		if (currPlayer->hand->busted()) {
			currPlayer->hand->lost = true;
			currPlayer->hand->shadeHand();
		}
			

	}
	if (finalCheck) {
		dealer->hand->playerHand[1]->hidden = false;
		
		while (dealer->hand->getPoints() < 17) {
			dealer->hand->addCardToHand(deck->draw());
			//printGameState();
			//FsSleep(1500);
		}
		printGameState();

		deck->playChips(); // play chips sound effect

		// DEALER BUSTED //
		if (dealer->hand->getPoints() > 21) {
			for (Player* currPlayer : players) {

				if (currPlayer->doubledDown)
					currPlayer->hand->playerHand[2]->hidden = false;

				currPlayer->record[0]++;
				if (!currPlayer->hand->busted()) {
					currPlayer->money += currPlayer->hand->bet;
					currPlayer->record[0]++;
				}
				else if (currPlayer->hand->busted()) {
					currPlayer->money -= currPlayer->hand->bet;
					currPlayer->record[1]++;
				}

				if (currPlayer->splitted) {
					if (!currPlayer->altHand->busted()) {
						currPlayer->money += currPlayer->hand->bet;
						currPlayer->record[0]++;
					}
					else if (currPlayer->altHand->busted()) {
						currPlayer->money -= currPlayer->hand->bet;
						currPlayer->record[1]++;
					}
				}
			}
		}
		// DEALER NOT BUSSIN //
		else {
			for (Player* currPlayer : players) {
				if (currPlayer->doubledDown)
					currPlayer->hand->playerHand[2]->hidden = false;

				if (currPlayer->hand->busted()) {
					currPlayer->money -= currPlayer->hand->bet;
					currPlayer->record[1]++;
				}
				else if (currPlayer->hand->getPoints() > dealer->hand->getPoints()) {
					currPlayer->money += currPlayer->hand->bet;
					currPlayer->record[0]++;
				}
				else if (currPlayer->hand->getPoints() < dealer->hand->getPoints()) {
					currPlayer->money -= currPlayer->hand->bet;
					currPlayer->record[1]++;
					currPlayer->hand->shadeHand();
				}
				else currPlayer->record[2]++;

				if (currPlayer->splitted) {
					if (currPlayer->altHand->busted()) {
						currPlayer->money -= currPlayer->hand->bet;
						currPlayer->record[1]++;
					}
					else if (currPlayer->altHand->getPoints() > dealer->hand->getPoints()) {
						currPlayer->money += currPlayer->hand->bet;
						currPlayer->record[0]++;
					}
					else if (currPlayer->altHand->getPoints() < dealer->hand->getPoints()) {
						currPlayer->money -= currPlayer->hand->bet;
						currPlayer->record[1]++;
						currPlayer->hand->shadeHand();
					}
					else
						currPlayer->record[2]++;
				}
			}
		}
		// HANDLED IN CLEARHAND() //
		//for (Player* currPlayer : players) {
		//	currPlayer->done = false;
		//}
		printRecord();
	}
}

void Game::printRecord() {
	cout << endl;
	cout << "W  L  T" << endl;
	for (Player* currPlayer : players)
		cout << currPlayer->record[0] << "  " << currPlayer->record[1] << "  " << currPlayer->record[2] << endl;
	cout << endl;
	cout << endl;
	cout << "Chip totals:" << endl;
	for (Player* currPlayer : players)
		cout << "Player " << currPlayer->num << ": " << currPlayer->money << endl;
	cout << endl;
}

void Game::clearHand() {
	for (Player* currPlayer : players) {
		currPlayer->hand->clearHand();
		if (currPlayer->splitted) currPlayer->altHand->clearHand();
		currPlayer->splitted = false;
		currPlayer->doubledDown = false;
		currPlayer->done = false;
	}
	dealer->hand->clearHand();
}









// GRAPHICS FUNCTIONS

void Game::loadHelper(string fileName, YsRawPngDecoder& decodeFile, GLuint& textureFile) {
	const char* c = fileName.c_str();
	decodeFile.Decode(c);
	glGenTextures(1, &textureFile);
	glBindTexture(GL_TEXTURE_2D, textureFile);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, decodeFile.wid,
		decodeFile.hei, 0, GL_RGBA, GL_UNSIGNED_BYTE, decodeFile.rgba);
}

void Game::loadTextures() {
	// Read Table PNG
	loadHelper("table.png", miscPng[1], miscTexture[1]);
	loadHelper("shade.png", miscPng[4], miscTexture[4]);
	loadHelper("menu.png", miscPng[0], miscTexture[0]);
	loadHelper("blueTable.png", miscPng[2], miscTexture[2]);
	// Read Card pngs
	for (int i = 0; i <= 12; i++) {
		for (int j = 0; j <= 3; j++) {
			string str = to_string(i) + to_string(j) + ".png";
			loadHelper(str, png[i][j], textures[i][j]);
		}
	}
}

void Game::drawBackground(int version) {
	int wid, hei;
	FsGetWindowSize(wid, hei);

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
	glBindTexture(GL_TEXTURE_2D, miscTexture[version]); // Current texture from reserved ids
	glBegin(GL_QUADS);

	glTexCoord2d(1.0, 1.0);
	glVertex2d(wid, hei);

	glTexCoord2d(0.0, 1.0);
	glVertex2d(0, hei);

	glTexCoord2d(0.0, 0.0);
	glVertex2d(0, 0);

	glTexCoord2d(1.0, 0.0);
	glVertex2d(wid, 0);

	glEnd();
}



int Game::getIntFromScreen() {
	string tempString = getStringFromScreen();
	int result = stoi(tempString);
	result += 3;
	return result;
}

string Game::getStringFromScreen()
{
	int adjustLetter;
	int key;
	string fileName = "";

	FsPollDevice();
	key = FsInkey();
	while (key != FSKEY_ESC && key != FSKEY_ENTER) {
		glClear(GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT);

		// build filename from keyboard entry, letter by letter
		DrawingUtilNG::buildStringFromFsInkey(key, fileName);
		cout << fileName << endl;

		FsSwapBuffers();
		FsSleep(25);

		FsPollDevice();
		key = FsInkey();
	}

	if (key == FSKEY_ENTER) {
		return fileName;
	}
	else
		return "";

}


void Game::drawCardsAuto(Player* player) {

	if (player->hand->getPoints() < 17) {
		//if (timeElapsed > 1
		player->hand->addCardToHand(deck->draw());
		// get ready for next cycle
	}

	if (player->hand->getPoints() > 21) {
		player->hand->lost = true;
		player->hand->shadeHand();
		player->done = true;
	}
	else if (player->hand->getPoints() >= 17) {
		player->done = true;
	}

	printGameState();
}

void Game::printMoney() {
	int n = 0;
	for (Player* currPlayer : players) {
		glColor3f(0, 0, 0);
		glRasterPos2d(0, 500);
		string line = "Player " + to_string(currPlayer->num) + ": $" + to_string(currPlayer->money);
		//YsGlDrawFontBitmap20x28(line);

		//FsSwapBuffers();
		n++;
	}
}


int Game::promptCount() {
	string fileName = "";
	string prompt = "Input Count . . .";
	//FsSwapBuffers();

	while (key != FSKEY_ESC && key != FSKEY_ENTER) {
		//glClear(GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT);

		// ask for file name from the graphics window
		glColor3f(1, 0, 0);
		glRasterPos2d(340, 25);
		YsGlDrawFontBitmap16x20(prompt.c_str());
		//glRasterPos2d(360, 50);
		//YsGlDrawFontBitmap12x16("Press ENTER when done, ESC to cancel.");
		glColor3ub(255, 0, 255);
		DrawingUtilNG::drawRectangle(340, 35, 350, 50, false);

		// build filename from keyboard entry, letter by letter
		DrawingUtilNG::buildStringFromFsInkey(key, fileName);

		fileName += "_"; // add an underscore as prompt
		glRasterPos2i(365, 75);  // sets position
		YsGlDrawFontBitmap16x24(fileName.c_str());
		fileName = fileName.substr(0, fileName.length() - 1); // remove underscore

		FsSwapBuffers();
		FsSleep(25);

		FsPollDevice();
		key = FsInkey();
	}

	if (key == FSKEY_ENTER) {
		//glColor3f(1, 0, 0);
		//glRasterPos2d(140, 400);
		//YsGlDrawFontBitmap16x20("Loading . . .");

		//FsSwapBuffers(); // this keeps the other stuff on because the previous buffer had it too
		return stoi(fileName);
	}
	else
		return 0;
}


void Game::manage() {	
	FsPollDevice();
	key = FsInkey();


	/////////////////////////////////////	MAIN MENU	/////////////////////////////////////////////////////
	
	if (gameMode == 0) {			// If the screen is on menu

		drawBackground(gameMode);

		switch (key) {
		case FSKEY_M:				// Pressing M opens the menu
			gameMode = 0;
			break;
		case FSKEY_B:				// Pressing B starts Blackjack Game
			gameMode = 1;
			break;
		case FSKEY_C:				// Pressing C starts Counting Cards Game
			gameMode = 2;
			break;
		case FSKEY_S:				// Pressing S starts Simulation Mode
			gameMode = 3;
			break;
		case FSKEY_X:				// Pressing X closes the Menu
			gameRunning = false;
			break;
		}
	}

	////////////////////////////////////////////// BLACKJACK REGULAR ///////////////////////////////////////////////

	else if (gameMode == 1) {			// If BlackJack Mode							
		
		cout << "NOW PLAYING BLACKJACK" << endl << endl;
		
		dealRound(gameMode);					// Deal Cards Initially
		if (gameMode == 0) { goto backMenu; }
		
		printGameState();				// Print the dealt cards

		
		playerTurn = 1;						// Player number
		for (Player* currPlayer : players) {
			
			key = FSKEY_NULL;

			if (currPlayer->hand->isBlackjack()) {
				int newB = (currPlayer->hand->bet * 3) / 2;
				currPlayer->hand->bet = newB;
				currPlayer->done = true;
				goto playerDone;
				//continue;
			}

			//if (currPlayer->done) break;
			
			printPlayerPrompt(playerTurn, currPlayer);			// Print player menu
			while (key != FSKEY_2) {		// move to next player if 2 is inputted (STAND)

				// double down check //
				if (currPlayer->doubledDown) {
					currPlayer->hand->addCardToHand(deck->draw()); // Draw Card ONCE (HIT)
					currPlayer->done = true;
					goto playerDone;
				}
				
				FsPollDevice();
				key = FsInkey();
				
				switch (key) {

				case FSKEY_1:
					currPlayer->hand->addCardToHand(deck->draw()); // Draw Card (HIT)
					printGameState();							   // Show game state
					if (currPlayer->hand->getPoints() >= 21) {
						currPlayer->done = true;
						if (currPlayer->splitted) {
							///////////// ALTERNATE HAND CHECK INTERIOR ////////////
							if (currPlayer->splitted && currPlayer->done) {
								printPlayerPrompt(playerTurn, currPlayer);			// Print player menu
								while (key != FSKEY_2) {		// move to next player if 2 is inputted (STAND)

									FsPollDevice();
									key = FsInkey();

									switch (key) {

									case FSKEY_1:
										currPlayer->altHand->addCardToHand(deck->draw()); // Draw Card (HIT)
										printGameState();							   // Show game state
										if (currPlayer->altHand->getPoints() >= 21) {
											currPlayer->done = true;
											goto playerDone;
										}
										printPlayerPrompt(playerTurn, currPlayer);							// Print player menu
										break;


									case FSKEY_2:							// Move on (STAND)
										break;

									case FSKEY_M:							// Pressing M opens the menu
										printMenu();
										gameMode = 0;
										goto backMenu;						// Break out of loop
									}
								}
							}
						}
						else {
							goto playerDone;
						}
					}
					printPlayerPrompt(playerTurn, currPlayer);							// Print player menu
					break;

				case FSKEY_2:							// Move on (STAND)
					break;

				case FSKEY_3:
					if (currPlayer->hand->splittable()) currPlayer->splitHand();
					break;
				
				case FSKEY_4:
					if (currPlayer->hand->canDoubleDown()) currPlayer->doubleDown();
					break;

				case FSKEY_M:							// Pressing M opens the menu
					printMenu();
					gameMode = 0;
					goto backMenu;						// Break out of loop

				
					
				}

				/////////////// DRAW ////////////////////
				int playerNumber = 0;									// iterate player number
				glClear(GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT);		// clear screen
				
				drawBackground(gameMode);										// draw background

				dealer->hand->drawHandOnScreen(playerNumber, textures, miscTexture[4],png, true);	// draw dealer hand

				for (Player* currPlayer: players){										// draw players hand
					currPlayer->hand->changeTurn(playerTurn - 1);

					currPlayer->hand->drawHandOnScreen(playerNumber, textures, miscTexture[4], png);
					if (currPlayer->splitted) 
						currPlayer->altHand->drawHandOnScreen(playerNumber, textures, miscTexture[4], png, false, true);
					playerNumber++;										// iterate player number

				}
				//////////// END DRAW ///////////////

				if (currPlayer->hand->getPoints() == 21) {
					currPlayer->done = true;
					goto playerDone;
				}

				FsSwapBuffers();										// get ready for next cycle
				FsSleep(25);
			}

		playerDone:
			cout << endl;

			checkGameState();					// Check if anybody has lost
			playerTurn++;								// Move on to next player
		}
		checkGameState(true);					// Check if dealer wins
		
		
		//printRecord();							// Print win loss tie record for each player
		while (key != FSKEY_N) {
			FsPollDevice();
			key = FsInkey();
			int playerNumber = 0;
			glClear(GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT);
			  
			drawBackground(gameMode);

			
			dealer->hand->drawHandOnScreen(playerNumber, textures, miscTexture[4], png, true);

			for (Player* currPlayer : players) {
				currPlayer->hand->changeTurn((players.size())/2);
				currPlayer->hand->drawHandOnScreen(playerNumber, textures, miscTexture[4], png);
				if (currPlayer->splitted)
					currPlayer->altHand->drawHandOnScreen(playerNumber, textures, miscTexture[4], png, false, true);
				playerNumber++;
			}
			switch (key) {
			case FSKEY_M:							// Pressing M opens the menu
				printMenu();
				gameMode = 0;
				goto backMenu;
			}

			FsSwapBuffers();
			FsSleep(25);
		}
		
		clearHand();							// Clear Hand
	backMenu:
		cout << "done" << endl;
	}



	/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


	else if (gameMode == 2) {												// If Counting Mode							
	cout << "NOW PLAYING COUNTING GAME" << endl << endl;
	int correct = 0;
	int outOf = 0;
	auto begin = std::chrono::high_resolution_clock::now();	
	int guess;
		// begin clock

	dealRound(gameMode);															// Deal Cards Initially
	if (gameMode == 0) { goto backMenu; }

	playerTurn = 1;																// Player number
	for (Player* currPlayer : players) {
		key = FSKEY_NULL;
		printPlayerPrompt(playerTurn, currPlayer);			// Print player menu
		
		while (!currPlayer->done) {											// player n's turn
			timeElapsed = chrono::duration_cast<chrono::milliseconds>
				(chrono::high_resolution_clock::now() - begin).count();

			if (timeElapsed > gameSpeed) {
				drawCardsAuto(currPlayer);
				begin = std::chrono::high_resolution_clock::now();
			}
			
			//cout << timeElapsed << "     time" << endl;

			int playerNumber = 0;									// iterate player number
			glClear(GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT);		// clear screen

			drawBackground(gameMode);										// draw background

			dealer->hand->drawHandOnScreen(playerNumber, textures, miscTexture[2], png, true);	// draw dealer hand

			for (Player* newPlayer : players) {										// draw players hand

				newPlayer->hand->drawHandOnScreen(playerNumber, textures, miscTexture[4], png);
				playerNumber++;										// iterate player number
			}

			
			printGameState(true);

			FsSwapBuffers();
			FsSleep(25);
		}

		checkGameState();					// Check if anybody has lost
		playerTurn++;								// Move on to next player
	}

	checkGameState(true);					// Check if dealer wins
											// Print win loss tie record for each player

	//while (key != FSKEY_3) {
		FsPollDevice();
		key = FsInkey();
		int playerNumber = 0;
		glClear(GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT);

		drawBackground(gameMode);

		dealer->hand->drawHandOnScreen(playerNumber, textures, miscTexture[4], png, true);

		for (Player* currPlayer : players) {
			currPlayer->hand->changeTurn((players.size()) / 2, true);
			currPlayer->hand->drawHandOnScreen(playerNumber, textures, miscTexture[4], png);
			playerNumber++;
		}
		switch (key) {
		case FSKEY_M:							// Pressing M opens the menu
			printMenu();
			gameMode = 0;
			goto backMenu2;
		}
		 
		FsSwapBuffers();
		FsSleep(25);
	//}
		FsSwapBuffers();

	guess = promptCount();
	outOf++;
	if (guess == deck->count) {
		correct++;
		glColor3f(1, 1, 1);
		glRasterPos2d(140, 400);
		YsGlDrawFontBitmap16x20("Correct!");
		FsSleep(1000);
		FsSwapBuffers(); // this keeps the other stuff on because the previous buffer had it too
	}
	else {
		glColor3f(1, 0, 0);
		glRasterPos2d(140, 400);
		YsGlDrawFontBitmap16x20("Incorrect. Correct count:");
		Fonts.drawText(to_string(deck->count), 650, 250, 10);
		FsSleep(1000);
		/////////// OUTPUT CORRECT COUNT //////////

		FsSwapBuffers(); // this keeps the other stuff on because the previous buffer had it too
	}

	cout << "RECORD: " << endl;
	cout << "\t" << correct << " out of " << outOf << " correct" << endl;

	clearHand();							// Clear Hand
backMenu2:
	cout << "done" << endl;
	}

	FsSwapBuffers();
	FsSleep(25);

}



