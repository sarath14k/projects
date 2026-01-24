#ifndef KNIGHT_H
#define KNIGHT_H

#include "chesspiece.h"

class Knight : public ChessPiece {
public:
    std::vector<std::pair<int, int>> getValidMoves(const ChessBoard* board, int row, int col) const override;
    char getSymbol() const override { return 'N'; } // Symbol for Knight
};

#endif // KNIGHT_H
