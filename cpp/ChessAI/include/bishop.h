#ifndef BISHOP_H
#define BISHOP_H

#include "chesspiece.h"

class Bishop : public ChessPiece {
public:
    std::vector<std::pair<int, int>> getValidMoves(const ChessBoard* board, int row, int col) const override;
    char getSymbol() const override { return 'B'; } // Symbol for Bishop
};

#endif // BISHOP_H
