#ifndef GAME_H
#define GAME_H

#include "chessboard.h"
#include "player.h"
#include "ai.h"
#include "movevalidator.h"
#include "gamelog.h"

class Game {
    public:
        Game();
        void start();
        void makeMove(int fromRow, int fromCol,int toRow,
                        int toCol);
        void undoMove();
        void displayStatus() const;
    
    private:
        ChessBoard board;
        AI ai;
        MoveValidator validator;
        GameLog log;
        Player currentPlayer;
};

#endif // GAME_H