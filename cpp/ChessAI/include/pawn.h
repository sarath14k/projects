#ifndef PAWN_H
#define PAWN_H

#include "chesspiece.h"

class Pawn : public ChessPiece{
    public:
        std::vector<std::pair<int, int>> getValidMoves(const ChessBoard* board,
            int row, int col) const override;
        char getSymbol() const override {return 'P';} // Symbol for pawn;
};

#endif // PAWN_H