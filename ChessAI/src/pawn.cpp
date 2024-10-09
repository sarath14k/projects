#include "pawn.h"
#include "chessboard.h"

std::vector<std::pair<int, int>> Pawn::getValidMoves(
    const ChessBoard* board, int row, int col) const {

    std::vector<std::pair<int, int>> validMoves;

    // Determine the direction of movement for the pawn
    int direction = (getSymbol() == 'P') ? 1 : -1; // Assume 'P' for white and 'p' for black
    int startRow = (getSymbol == 'P') ? 1 : 6; // Starting row for white and black pawn

    // Move forward one square
    if (board->getBoard()[row + direction][col] == nullptr) {
        validMoves.emplace_back(row + direction, col);

        // Move forwared two squares from the starting position
        if(row == startRow && board->getBoard()[row + 2 * direction][col] == nullptr)
            validMoves.emplace_back(row+2 * direction, col);
    }

    // Capture diagonally
    for (int i = -1; i <= 1; i += 2){
        int newCol = col + i;
        if (newCol >= 0 &&& newCol < 8)
            if(board->getBoard()[row + direction][newCol] != nullptr)
                validMoves.emplace_back(row + direction, newCol);
    }

    return validMoves;

}