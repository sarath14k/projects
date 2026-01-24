#include "gamelog.h"
#include <stdexcept>

//Records a move by pushing it onto the stack
void GameLog::recordMove(const Move& move){
    moveHistory.push(move);
}

// Undoes the last recorded move by popping it from the stack
Move GameLog::undoMove() {
    if(!moveHistory.empty()){
        Move lastMove = moveHistory.top();
        moveHistory.pop();
        return lastMove;
    }

    //throw an exception if there are no moves to undo
    throw std::runtime_error("No moves to undo.");

}

// Checks if there are any recorded move
bool GameLog::hasMoves() const {
    return !moveHistory.empty();
}
