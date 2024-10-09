#ifndef MOVEVALIDATOR_H
#define MOVEVALIDATOR_H

#include <utility>
#include "chessboard.h"
#include "chesspiece.h"
#include "player.h"

class MoveValidator{
public:
    bool isMoreValid(const ChessBoard* board, int fromRow, int fromCol,
                    int toRow, int toCol) const;
    bool isCheck(const ChessBoard* board, Player player) const;
    bool isCheckMate(const ChessBoard* board, Player player) const;

};

#endif // MOVEvALIDATOR_H