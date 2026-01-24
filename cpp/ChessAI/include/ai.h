#ifndef AI_H
#define AI_H

#include "chessboard.h"
#include "player.h"
#include "movevalidator.h"
#include "move.h"

class AI{
public:
    AI(ChessBoard* board, int searchDepth = 3);
    Move getBestMove();

private:
    ChessBoard* board;
    int searchDepth;

    int evaluateBoard() const;
    int minimax(int depth, bool maximizingPlayer, int alpha, 
                int beta);
    std::vector<Move> getAllValidMoves(Player player);

};

#endif // AI_H