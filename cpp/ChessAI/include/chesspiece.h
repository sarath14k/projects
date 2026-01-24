#ifndef CHESSPIECE_H
#define CHESSPIECE_H

#include <vector>
#include <utility> // for std::pair

class ChessBoard; // Forward declaration

class ChessPiece {

    public:
        virtual ~ChessPiece() = default; // Virtual destructor for proper cleanup
        virtual std::vector<std::pair<int, int>> getValidMoves(const ChessBoard* board, int row, int col) const = 0; // Pure virtual function
        virtual char getSymbol() const = 0; // Function to get the symbol representing the piece
};

#endif // CHESSPIECE_H
