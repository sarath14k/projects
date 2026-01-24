#ifndef QUEEN_H
#define QUEEN_H

#include "chesspiece.h"

class Queen : public ChessPiece {
public:
    std::vector<std::pair<int, int>> getValidMoves(const ChessBoard* board, int row, int col) const override;
    char getSymbol() const override { return 'Q'; } // Symbol for Queen
};

#endif // QUEEN_H
