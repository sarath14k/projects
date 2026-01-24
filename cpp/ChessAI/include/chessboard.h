#ifndef CHESSBOARD_H
#define CHESSBOARD_H

#include <vector>
#include <memory>
#include "chesspiece.h"
#include "movevalidator.h"
#include "gamelog.h"

class ChessBoard {
private:
    std::vector<std::vector<std::unique_ptr<ChessPiece>>> board; // 2D vector to hold chess pieces
    MoveValidator moveValidator; // Object for validating moves
    GameLog gameLog; // Object for logging game actions

public:
    ChessBoard(); // Constructor to initialize the board
    void initializeBoard(); // Method to set up the board with pieces
    void printBoard() const; // Method to print the board state
    bool makeMove(int startRow, int startCol, int endRow, int endCol); // Method to make a move
    bool isInCheck(bool isWhite) const; // Check if the current player is in check
    bool isCheckmate(bool isWhite) const; // Check if the current player is in checkmate

    // Getters for the board and game log
    const std::vector<std::vector<std::unique_ptr<ChessPiece>>>& getBoard() const { return board; }
    const GameLog& getGameLog() const { return gameLog; }

    // Additional utility methods can be added as needed
};

#endif// CHESSBOARD_H