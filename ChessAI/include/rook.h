#ifndef ROOK_H
#define ROOK_H

#include "chesspiece.h"

class Rook : public ChessPiece{
    public:
        std::vector<std::pair<int, int>> getValidMoves(const ChessBoard* board,
            int row, int col) const override;
        char getSymbol() const override {return 'R';}// Symbol fo Rook
};

#endif // ROOK_H
