#ifndef KING_H
#define KING_H

#include "chesspiece.h"

class King : public ChessPiece {
public:
    std::vector<std::pair<int, int>> getValidMoves(const ChessBoard* board, int row, int col) const override;
    char getSymbol() const override { return 'K'; } // Symbol for King
};

#endif // KING_H
