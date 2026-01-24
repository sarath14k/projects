#include "ai.h"
#include <algorithm>
#include "move.h"

AI::AI(ChessBoard* board, int searchDepth) 
    : board(board), searchDepth(searchDepth) {}

Move AI::getBestMove(){
    int bestValue = -10000; // Initialize to a very low value
    Move bestMove;

    // Iterate through all possible moves for the AI player
    for (const Move& move : getAllValidMoves(Player::AI)) {
        // Make the move
        int startRow = move.startRow;
        int startCol = move.startCol;
        int endRow = move.endRow;
        int endCol = move.endCol;
    }

}

