#include <iostream>
#include <vector>

void printSolution(const std::vector<int>& board) {
    int n = board.size();
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            if (board[i] == j) {
                std::cout << " Q ";
            } else {
                std::cout << " . ";
            }
        }
        std::cout << std::endl;
    }
    std::cout << std::endl;
}

bool isSafe(const std::vector<int>& board, int row, int col) {
    for (int i = 0; i < row; ++i) {
        // Check column and diagonal attacks
        if (board[i] == col || board[i] - i == col - row || board[i] + i == col + row) {
            return false;
        }
    }
    return true;
}

void solveNQueens(int row, std::vector<int>& board, std::vector<std::vector<int>>& solutions) {
    int n = board.size();
    if (row == n) {
        solutions.push_back(board); // Found a valid solution
        return;
    }

    for (int col = 0; col < n; ++col) {
        if (isSafe(board, row, col)) {
            board[row] = col; // Place queen
            solveNQueens(row + 1, board, solutions); // Recur to place next queen
            // Backtrack: no need to explicitly remove the queen as we overwrite in the next iteration
        }
    }
}

int main() {
    int n = 4; // Size of the chessboard
    std::vector<int> board(n, -1); // Board representation (column index for each row)
    std::vector<std::vector<int>> solutions;

    solveNQueens(0, board, solutions);

    std::cout << "Solutions for " << n << "-Queens:" << std::endl;
    for (const auto& solution : solutions) {
        printSolution(solution);
    }

    return 0;
}
