#ifndef MOVE_H
#define MOVE_H

#include <utility>
#include "chesspiece.h"

struct Move
{
    std::pair <int, int> from; // Starting position (row,column)
    std::pair <int, int> to; //Ending position (row, column)
    ChessPiece* movedPiece; // Pointer to the moved piece
    ChessPiece* capturedPiece; // Pointer to any captured piece (nullptr if no capture)

    Move(int fromRow, int fromCol, int toRow, int toCol, ChessPiece* moved, 
            ChessPiece* captured = nullptr) : from({fromRow, fromCol}),
            to({toRow, toCol}), movedPiece(moved), capturedPiece(captured) {}

    bool isCapture() const { return capturedPiece != nullptr;}

};

#endif // MOVE_H
