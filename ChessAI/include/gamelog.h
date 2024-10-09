#ifndef GAMELOG_H
#define GAMELOG_H

#include <stack>
#include "move.h"

class GameLog{
public:
    void recordMove(const Move& move);
    Move undoMove();
    bool hasMoves() const;

private:  
    std::stack<Move> moveHistory;
};

#endif //GAMELOOG_H