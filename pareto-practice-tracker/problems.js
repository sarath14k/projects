// problems.js - Database of all 49 Pareto Problem Set questions with FULL RUNNABLE C++ and PYTHON codes
const PROBLEMS = [
  // ==================== ARRAYS & HASHING ====================
  {
    id: 1,
    name: "Contains Duplicate",
    category: "Arrays & Hashing",
    difficulty: "Easy",
    leetCodeUrl: "https://leetcode.com/problems/contains-duplicate/",
    description: "Given an integer array `nums`, return `true` if any value appears **at least twice** in the array, and return `false` if every element is distinct.",
    examples: [
      { input: "nums = [1,2,3,1]", output: "true", explanation: "The element 1 occurs at index 0 and 3." },
      { input: "nums = [1,2,3,4]", output: "false", explanation: "All elements are unique." }
    ],
    constraints: ["`1 <= nums.length <= 10^5`", "`-10^9 <= nums[i] <= 10^9`"],
    starterCode: {
      cpp: `#include <iostream>\n#include <vector>\n#include <unordered_set>\n\nusing namespace std;\n\nclass Solution {\npublic:\n    bool containsDuplicate(vector<int>& nums) {\n        // Write code here\n        return false;\n    }\n};\n\nint main() {\n    Solution sol;\n    vector<int> nums = {1, 2, 3, 1};\n    cout << (sol.containsDuplicate(nums) ? "True" : "False") << endl;\n    return 0;\n}`,
      python: `from typing import List\n\nclass Solution:\n    def containsDuplicate(self, nums: List[int]) -> bool:\n        # Write code here\n        return False\n\nif __name__ == "__main__":\n    sol = Solution()\n    print(sol.containsDuplicate([1, 2, 3, 1]))`
    },
    solutions: {
      cpp: `#include <iostream>\n#include <vector>\n#include <unordered_set>\n\nusing namespace std;\n\nclass Solution {\npublic:\n    bool containsDuplicate(vector<int>& nums) {\n        unordered_set<int> seen;\n        for (int num : nums) {\n            if (seen.count(num)) return true;\n            seen.insert(num);\n        }\n        return false;\n    }\n};\n\nint main() {\n    Solution sol;\n    vector<int> test1 = {1, 2, 3, 1};\n    vector<int> test2 = {1, 2, 3, 4};\n    \n    cout << "Test 1 [1,2,3,1]: " << (sol.containsDuplicate(test1) ? "True" : "False") << " (Expected: True)" << endl;\n    cout << "Test 2 [1,2,3,4]: " << (sol.containsDuplicate(test2) ? "True" : "False") << " (Expected: False)" << endl;\n    return 0;\n}`,
      python: `from typing import List\n\nclass Solution:\n    def containsDuplicate(self, nums: List[int]) -> bool:\n        seen = set()\n        for num in nums:\n            if num in seen:\n                return True\n            seen.add(num)\n        return False\n\nif __name__ == "__main__":\n    sol = Solution()\n    test1 = [1, 2, 3, 1]\n    test2 = [1, 2, 3, 4]\n    print(f"Test 1 [1,2,3,1]: {sol.containsDuplicate(test1)} (Expected: True)")\n    print(f"Test 2 [1,2,3,4]: {sol.containsDuplicate(test2)} (Expected: False)")`
    },
    complexity: { time: "O(n)", space: "O(n)" },
    explanation: "We utilize a Hash Set to track elements we have already encountered. As we traverse the array, we check if the current element exists in the set. If it does, a duplicate exists. Otherwise, we add the element to the set. If the loop completes, all elements are unique."
  },
  {
    id: 2,
    name: "Valid Anagram",
    category: "Arrays & Hashing",
    difficulty: "Easy",
    leetCodeUrl: "https://leetcode.com/problems/valid-anagram/",
    description: "Given two strings `s` and `t`, return `true` if `t` is an anagram of `s`, and `false` otherwise.\n\nAn **Anagram** is a word or phrase formed by rearranging the letters of a different word or phrase, typically using all the original letters exactly once.",
    examples: [
      { input: "s = \"anagram\", t = \"nagaram\"", output: "true" },
      { input: "s = \"rat\", t = \"car\"", output: "false" }
    ],
    constraints: ["`1 <= s.length, t.length <= 5 * 10^4`", "`s` and `t` consist of lowercase English letters."],
    starterCode: {
      cpp: `#include <iostream>\n#include <string>\n\nusing namespace std;\n\nclass Solution {\npublic:\n    bool isAnagram(string s, string t) {\n        // Write code here\n        return false;\n    }\n};\n\nint main() {\n    Solution sol;\n    cout << (sol.isAnagram("anagram", "nagaram") ? "True" : "False") << endl;\n    return 0;\n}`,
      python: `class Solution:\n    def isAnagram(self, s: str, t: str) -> bool:\n        # Write code here\n        return False\n\nif __name__ == "__main__":\n    sol = Solution()\n    print(sol.isAnagram("anagram", "nagaram"))`
    },
    solutions: {
      cpp: `#include <iostream>\n#include <string>\n\nusing namespace std;\n\nclass Solution {\npublic:\n    bool isAnagram(string s, string t) {\n        if (s.length() != t.length()) return false;\n        int counts[26] = {0};\n        for (int i = 0; i < s.length(); ++i) {\n            counts[s[i] - 'a']++;\n            counts[t[i] - 'a']--;\n        }\n        for (int count : counts) {\n            if (count != 0) return false;\n        }\n        return true;\n    }\n};\n\nint main() {\n    Solution sol;\n    string s1 = "anagram", t1 = "nagaram";\n    string s2 = "rat", t2 = "car";\n    \n    cout << "Test 1: " << (sol.isAnagram(s1, t1) ? "True" : "False") << " (Expected: True)" << endl;\n    cout << "Test 2: " << (sol.isAnagram(s2, t2) ? "True" : "False") << " (Expected: False)" << endl;\n    return 0;\n}`,
      python: `class Solution:\n    def isAnagram(self, s: str, t: str) -> bool:\n        if len(s) != len(t):\n            return False\n        count = {}\n        for char in s:\n            count[char] = count.get(char, 0) + 1\n        for char in t:\n            if char not in count or count[char] == 0:\n                return False\n            count[char] -= 1\n        return True\n\nif __name__ == "__main__":\n    sol = Solution()\n    print(f"Test 1: {sol.isAnagram('anagram', 'nagaram')} (Expected: True)")\n    print(f"Test 2: {sol.isAnagram('rat', 'car')} (Expected: False)")`
    },
    complexity: { time: "O(n)", space: "O(1)" },
    explanation: "Two strings are anagrams if they have the exact same character frequencies. First, check if lengths match. Then, count character occurrences. We can use a frequency array of size 26 for lowercase letters. Increment for string `s` and decrement for string `t`. If all slots return to zero, it is a valid anagram."
  },
  {
    id: 3,
    name: "Two Sum",
    category: "Arrays & Hashing",
    difficulty: "Easy",
    leetCodeUrl: "https://leetcode.com/problems/two-sum/",
    description: "Given an array of integers `nums` and an integer `target`, return *indices of the two numbers such that they add up to `target`*.\n\nYou may assume that each input would have ***exactly* one solution**, and you may not use the *same* element twice.\n\nYou can return the answer in any order.",
    examples: [
      { input: "nums = [2,7,11,15], target = 9", output: "[0,1]", explanation: "Because nums[0] + nums[1] == 9, we return [0, 1]." }
    ],
    constraints: ["`2 <= nums.length <= 10^4`", "`-10^9 <= nums[i] <= 10^9`", "`-10^9 <= target <= 10^9`", "Only one valid answer exists."],
    starterCode: {
      cpp: `#include <iostream>\n#include <vector>\n#include <unordered_map>\n\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> twoSum(vector<int>& nums, int target) {\n        // Write code here\n        return {};\n    }\n};\n\nint main() {\n    Solution sol;\n    vector<int> nums = {2, 7, 11, 15};\n    vector<int> res = sol.twoSum(nums, 9);\n    cout << "[" << res[0] << ", " << res[1] << "]" << endl;\n    return 0;\n}`,
      python: `from typing import List\n\nclass Solution:\n    def twoSum(self, nums: List[int], target: int) -> List[int]:\n        # Write code here\n        return []\n\nif __name__ == "__main__":\n    sol = Solution()\n    print(sol.twoSum([2, 7, 11, 15], 9))`
    },
    solutions: {
      cpp: `#include <iostream>\n#include <vector>\n#include <unordered_map>\n\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> twoSum(vector<int>& nums, int target) {\n        unordered_map<int, int> num_to_idx;\n        for (int i = 0; i < nums.size(); ++i) {\n            int complement = target - nums[i];\n            if (num_to_idx.count(complement)) {\n                return {num_to_idx[complement], i};\n            }\n            num_to_idx[nums[i]] = i;\n        }\n        return {};\n    }\n};\n\nint main() {\n    Solution sol;\n    vector<int> nums = {2, 7, 11, 15};\n    int target = 9;\n    vector<int> res = sol.twoSum(nums, target);\n    cout << "Indices: [" << res[0] << ", " << res[1] << "] (Expected: [0, 1])" << endl;\n    return 0;\n}`,
      python: `from typing import List\n\nclass Solution:\n    def twoSum(self, nums: List[int], target: int) -> List[int]:\n        prevMap = {} # val -> index\n        for i, n in enumerate(nums):\n            diff = target - n\n            if diff in prevMap:\n                return [prevMap[diff], i]\n            prevMap[n] = i\n        return []\n\nif __name__ == "__main__":\n    sol = Solution()\n    print(f"Indices: {sol.twoSum([2, 7, 11, 15], 9)} (Expected: [0, 1])")`
    },
    complexity: { time: "O(n)", space: "O(n)" },
    explanation: "Instead of searching for pairs using a nested loop ($O(n^2)$), we utilize a hash map to save values we have scanned and their corresponding index. For each number, we compute its complement (`target - num`). If the complement is present in the hash map, we return its index along with the current index."
  },
  {
    id: 4,
    name: "Group Anagrams",
    category: "Arrays & Hashing",
    difficulty: "Medium",
    leetCodeUrl: "https://leetcode.com/problems/group-anagrams/",
    description: "Given an array of strings `strs`, group the **anagrams** together. You can return the answer in **any order**.",
    examples: [
      { input: "strs = [\"eat\",\"tea\",\"tan\",\"ate\",\"nat\",\"bat\"]", output: "[[\"bat\"],[\"nat\",\"tan\"],[\"ate\",\"eat\",\"tea\"]]" }
    ],
    constraints: ["`1 <= strs.length <= 10^4`", "`0 <= strs[i].length <= 100`", "`strs[i]` consists of lowercase English letters."],
    starterCode: {
      cpp: `#include <iostream>\n#include <vector>\n#include <string>\n#include <unordered_map>\n#include <algorithm>\n\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<vector<string>> groupAnagrams(vector<string>& strs) {\n        // Write code here\n        return {};\n    }\n};\n\nint main() {\n    Solution sol;\n    vector<string> strs = {"eat","tea","tan","ate","nat","bat"};\n    vector<vector<string>> res = sol.groupAnagrams(strs);\n    for (auto& row : res) {\n        for (auto& s : row) cout << s << " ";\n        cout << "| ";\n    }\n    cout << endl;\n    return 0;\n}`,
      python: `from typing import List\nimport collections\n\nclass Solution:\n    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:\n        # Write code here\n        return []\n\nif __name__ == "__main__":\n    sol = Solution()\n    print(sol.groupAnagrams(["eat","tea","tan","ate","nat","bat"]))`
    },
    solutions: {
      cpp: `#include <iostream>\n#include <vector>\n#include <string>\n#include <unordered_map>\n#include <algorithm>\n\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<vector<string>> groupAnagrams(vector<string>& strs) {\n        unordered_map<string, vector<string>> groups;\n        for (const string& s : strs) {\n            string key = s;\n            sort(key.begin(), key.end());\n            groups[key].push_back(s);\n        }\n        vector<vector<string>> result;\n        for (auto& pair : groups) {\n            result.push_back(move(pair.second));\n        }\n        return result;\n    }\n};\n\nint main() {\n    Solution sol;\n    vector<string> strs = {"eat","tea","tan","ate","nat","bat"};\n    vector<vector<string>> res = sol.groupAnagrams(strs);\n    cout << "Grouped Anagrams:\\n";\n    for (const auto& group : res) {\n        cout << "[ ";\n        for (const string& s : group) cout << s << " ";\n        cout << "] ";\n    }\n    cout << endl;\n    return 0;\n}`,
      python: `from typing import List\nimport collections\n\nclass Solution:\n    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:\n        ans = collections.defaultdict(list)\n        for s in strs:\n            count = [0] * 26\n            for c in s:\n                count[ord(c) - ord('a')] += 1\n            ans[tuple(count)].append(s)\n        return list(ans.values())\n\nif __name__ == "__main__":\n    sol = Solution()\n    print(f"Grouped Anagrams: {sol.groupAnagrams(['eat','tea','tan','ate','nat','bat'])}")`
    },
    complexity: { time: "O(n * k log k)", space: "O(n * k)" },
    explanation: "Two strings are anagrams if their sorted forms are identical. We loop through the array of strings and use the sorted string as a unique identifier ('key') for a hash map. The key maps to a list of its anagrams. In Python, we can also use a character count tuple as the key, running in $O(n \\cdot k)$ where $k$ is maximum string length."
  },
  {
    id: 5,
    name: "Top K Frequent Elements",
    category: "Arrays & Hashing",
    difficulty: "Medium",
    leetCodeUrl: "https://leetcode.com/problems/top-k-frequent-elements/",
    description: "Given an integer array `nums` and an integer `k`, return *the* `k` *most frequent elements*. You may return the answer in **any order**.",
    examples: [
      { input: "nums = [1,1,1,2,2,3], k = 2", output: "[1,2]" }
    ],
    constraints: ["`1 <= nums.length <= 10^5`", "`-10^4 <= nums[i] <= 10^4`", "`k` is in the range `[1, the number of unique elements in the array]`", "The answer is **guaranteed** to be unique."],
    starterCode: {
      cpp: `#include <iostream>\n#include <vector>\n#include <unordered_map>\n\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> topKFrequent(vector<int>& nums, int k) {\n        // Write code here\n        return {};\n    }\n};\n\nint main() {\n    Solution sol;\n    vector<int> nums = {1, 1, 1, 2, 2, 3};\n    vector<int> res = sol.topKFrequent(nums, 2);\n    for (int x : res) cout << x << " ";\n    cout << endl;\n    return 0;\n}`,
      python: `from typing import List\n\nclass Solution:\n    def topKFrequent(self, nums: List[int], k: int) -> List[int]:\n        # Write code here\n        return []\n\nif __name__ == "__main__":\n    sol = Solution()\n    print(sol.topKFrequent([1, 1, 1, 2, 2, 3], 2))`
    },
    solutions: {
      cpp: `#include <iostream>\n#include <vector>\n#include <unordered_map>\n\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> topKFrequent(vector<int>& nums, int k) {\n        unordered_map<int, int> counts;\n        for (int num : nums) counts[num]++;\n        \n        int n = nums.size();\n        vector<vector<int>> buckets(n + 1);\n        for (auto& pair : counts) {\n            buckets[pair.second].push_back(pair.first);\n        }\n        \n        vector<int> res;\n        for (int i = n; i >= 0 && res.size() < k; --i) {\n            for (int num : buckets[i]) {\n                res.push_back(num);\n                if (res.size() == k) break;\n            }\n        }\n        return res;\n    }\n};\n\nint main() {\n    Solution sol;\n    vector<int> nums = {1, 1, 1, 2, 2, 3};\n    vector<int> res = sol.topKFrequent(nums, 2);\n    cout << "Top 2 Frequent: ";\n    for (int x : res) cout << x << " ";\n    cout << " (Expected: 1 2)" << endl;\n    return 0;\n}`,
      python: `from typing import List\n\nclass Solution:\n    def topKFrequent(self, nums: List[int], k: int) -> List[int]:\n        count = {}\n        freq = [[] for i in range(len(nums) + 1)]\n        \n        for n in nums:\n            count[n] = 1 + count.get(n, 0)\n        for n, c in count.items():\n            freq[c].append(n)\n            \n        res = []\n        for i in range(len(freq) - 1, 0, -1):\n            for n in freq[i]:\n                res.append(n)\n                if len(res) == k:\n                    return res\n\nif __name__ == "__main__":\n    sol = Solution()\n    print(f"Top 2 Frequent: {sol.topKFrequent([1, 1, 1, 2, 2, 3], 2)} (Expected: [1, 2])")`
    },
    complexity: { time: "O(n)", space: "O(n)" },
    explanation: "We count the frequencies of each element using a hash map. Instead of sorting by frequency in $O(n \\log n)$, we can use Bucket Sort. The buckets are indexed by frequency (from 0 to `nums.length`). We place each element in the bucket corresponding to its count. Finally, we iterate backward from the largest frequency to collect the top `k` elements."
  },
  {
    id: 6,
    name: "Valid Sudoku",
    category: "Arrays & Hashing",
    difficulty: "Medium",
    leetCodeUrl: "https://leetcode.com/problems/valid-sudoku/",
    description: "Determine if a `9 x 9` Sudoku board is valid. Only the filled cells need to be validated according to the following rules:\n\n1. Each row must contain the digits `1-9` without repetition.\n2. Each column must contain the digits `1-9` without repetition.\n3. Each of the nine `3 x 3` sub-boxes of the grid must contain the digits `1-9` without repetition.\n\nNote: A Sudoku board (partially filled) could be valid but is not necessarily solvable. Only the filled cells need to be validated.",
    examples: [
      { input: "board = [[\"5\",\"3\",\".\",\".\",\"7\",\".\",\".\",\".\",\".\"], ...]", output: "true" }
    ],
    constraints: ["`board.length == 9`", "`board[i].length == 9`", "`board[i][j]` is a digit `1-9` or `'.'`."],
    starterCode: {
      cpp: `#include <iostream>\n#include <vector>\n#include <unordered_set>\n#include <string>\n\nusing namespace std;\n\nclass Solution {\npublic:\n    bool isValidSudoku(vector<vector<char>>& board) {\n        // Write code here\n        return false;\n    }\n};\n\nint main() {\n    Solution sol;\n    vector<vector<char>> board = {\n        {'5','3','.','.','7','.','.','.','.'},\n        {'6','.','.','1','9','5','.','.','.'},\n        {'.','9','8','.','.','.','.','6','.'},\n        {'8','.','.','.','6','.','.','.','3'},\n        {'4','.','.','8','.','3','.','.','1'},\n        {'7','.','.','.','2','.','.','.','6'},\n        {'.','6','.','.','.','.','2','8','.'},\n        {'.','.','.','4','1','9','.','.','5'},\n        {'.','.','.','.','8','.','.','7','9'}\n    };\n    cout << (sol.isValidSudoku(board) ? "True" : "False") << endl;\n    return 0;\n}`,
      python: `from typing import List\nimport collections\n\nclass Solution:\n    def isValidSudoku(self, board: List[List[str]]) -> bool:\n        # Write code here\n        return False\n\nif __name__ == "__main__":\n    sol = Solution()\n    board = [\n        ["5","3",".",".","7",".",".",".","."],\n        ["6",".",".","1","9","5",".",".","."],\n        [".","9","8",".",".",".",".","6","."],\n        ["8",".",".",".","6",".",".",".","3"],\n        ["4",".",".","8",".","3",".",".","1"],\n        ["7",".",".",".","2",".",".",".","6"],\n        [".","6",".",".",".",".","2","8","."],\n        [".",".",".","4","1","9",".",".","5"],\n        [".",".",".",".","8",".",".","7","9"]\n    ]\n    print(sol.isValidSudoku(board))`
    },
    solutions: {
      cpp: `#include <iostream>\n#include <vector>\n#include <unordered_set>\n#include <string>\n\nusing namespace std;\n\nclass Solution {\npublic:\n    bool isValidSudoku(vector<vector<char>>& board) {\n        unordered_set<string> seen;\n        for (int r = 0; r < 9; ++r) {\n            for (int c = 0; c < 9; ++c) {\n                if (board[r][c] != '.') {\n                    char val = board[r][c];\n                    string row_key = to_string(val) + " found in row " + to_string(r);\n                    string col_key = to_string(val) + " found in col " + to_string(c);\n                    string box_key = to_string(val) + " found in box " + to_string(r/3) + "-" + to_string(c/3);\n                    if (seen.count(row_key) || seen.count(col_key) || seen.count(box_key)) {\n                        return false;\n                    }\n                    seen.insert(row_key);\n                    seen.insert(col_key);\n                    seen.insert(box_key);\n                }\n            }\n        }\n        return true;\n    }\n};\n\nint main() {\n    Solution sol;\n    vector<vector<char>> board = {\n        {'5','3','.','.','7','.','.','.','.'},\n        {'6','.','.','1','9','5','.','.','.'},\n        {'.','9','8','.','.','.','.','6','.'},\n        {'8','.','.','.','6','.','.','.','3'},\n        {'4','.','.','8','.','3','.','.','1'},\n        {'7','.','.','.','2','.','.','.','6'},\n        {'.','6','.','.','.','.','2','8','.'},\n        {'.','.','.','4','1','9','.','.','5'},\n        {'.','.','.','.','8','.','.','7','9'}\n    };\n    cout << "Is Valid Sudoku: " << (sol.isValidSudoku(board) ? "True" : "False") << " (Expected: True)" << endl;\n    return 0;\n}`,
      python: `from typing import List\nimport collections\n\nclass Solution:\n    def isValidSudoku(self, board: List[List[str]]) -> bool:\n        cols = collections.defaultdict(set)\n        rows = collections.defaultdict(set)\n        squares = collections.defaultdict(set)\n        \n        for r in range(9):\n            for c in range(9):\n                if board[r][c] == ".":\n                    continue\n                val = board[r][c]\n                if (val in rows[r] or\n                    val in cols[c] or\n                    val in squares[(r // 3, c // 3)]):\n                    return False\n                cols[c].add(val)\n                rows[r].add(val)\n                squares[(r // 3, c // 3)].add(val)\n        return True\n\nif __name__ == "__main__":\n    sol = Solution()\n    board = [\n        ["5","3",".",".","7",".",".",".","."],\n        ["6",".",".","1","9","5",".",".","."],\n        [".","9","8",".",".",".",".","6","."],\n        ["8",".",".",".","6",".",".",".","3"],\n        ["4",".",".","8",".","3",".",".","1"],\n        ["7",".",".",".","2",".",".",".","6"],\n        [".","6",".",".",".",".","2","8","."],\n        [".",".",".","4","1","9",".",".","5"],\n        [".",".",".",".","8",".",".","7","9"]\n    ]\n    print(f"Is Valid Sudoku: {sol.isValidSudoku(board)} (Expected: True)")`
    },
    complexity: { time: "O(1)", space: "O(1)" },
    explanation: "We scan the $9 \\times 9$ board exactly once. To track visited numbers, we save their presence in sets. For each cell `(r, c)`, if it contains a digit, we verify if it violates the row constraint, column constraint, or the sub-grid block. The block ID can be represented as `(r/3, c/3)`."
  },
  {
    id: 7,
    name: "Product of Array Except Self",
    category: "Arrays & Hashing",
    difficulty: "Medium",
    leetCodeUrl: "https://leetcode.com/problems/product-of-array-except-self/",
    description: "Given an integer array `nums`, return *an array* `answer` *such that* `answer[i]` *is equal to the product of all the elements of* `nums` *except* `nums[i]`.\n\nThe product of any prefix or suffix of `nums` is **guaranteed** to fit in a **32-bit** integer.\n\nYou must write an algorithm that runs in `O(n)` time and without using the division operation.",
    examples: [
      { input: "nums = [1,2,3,4]", output: "[24,12,8,6]" }
    ],
    constraints: ["`2 <= nums.length <= 10^5`", "`-30 <= nums[i] <= 30`", "The product fits in a 32-bit signed integer.", "Follow up: Can you solve the problem in `O(1)` extra space complexity? (The output array does not count as extra space)."],
    starterCode: {
      cpp: `#include <iostream>\n#include <vector>\n\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> productExceptSelf(vector<int>& nums) {\n        // Write code here\n        return {};\n    }\n};\n\nint main() {\n    Solution sol;\n    vector<int> nums = {1, 2, 3, 4};\n    vector<int> res = sol.productExceptSelf(nums);\n    for (int x : res) cout << x << " ";\n    cout << endl;\n    return 0;\n}`,
      python: `from typing import List\n\nclass Solution:\n    def productExceptSelf(self, nums: List[int]) -> List[int]:\n        # Write code here\n        return []\n\nif __name__ == "__main__":\n    sol = Solution()\n    print(sol.productExceptSelf([1, 2, 3, 4]))`
    },
    solutions: {
      cpp: `#include <iostream>\n#include <vector>\n\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> productExceptSelf(vector<int>& nums) {\n        int n = nums.size();\n        vector<int> res(n, 1);\n        \n        int prefix = 1;\n        for (int i = 0; i < n; ++i) {\n            res[i] = prefix;\n            prefix *= nums[i];\n        }\n        \n        int suffix = 1;\n        for (int i = n - 1; i >= 0; --i) {\n            res[i] *= suffix;\n            suffix *= nums[i];\n        }\n        \n        return res;\n    }\n};\n\nint main() {\n    Solution sol;\n    vector<int> nums = {1, 2, 3, 4};\n    vector<int> res = sol.productExceptSelf(nums);\n    cout << "Products: ";\n    for (int x : res) cout << x << " ";\n    cout << " (Expected: 24 12 8 6)" << endl;\n    return 0;\n}`,
      python: `from typing import List\n\nclass Solution:\n    def productExceptSelf(self, nums: List[int]) -> List[int]:\n        res = [1] * (len(nums))\n        \n        prefix = 1\n        for i in range(len(nums)):\n            res[i] = prefix\n            prefix *= nums[i]\n            \n        postfix = 1\n        for i in range(len(nums) - 1, -1, -1):\n            res[i] *= postfix\n            postfix *= nums[i]\n            \n        return res\n\nif __name__ == "__main__":\n    sol = Solution()\n    print(f"Products: {sol.productExceptSelf([1, 2, 3, 4])} (Expected: [24, 12, 8, 6])")`
    },
    complexity: { time: "O(n)", space: "O(1)" },
    explanation: "For any index `i`, its result is `(product of prefix values before i) * (product of suffix values after i)`. We can calculate this in two linear sweeps. In the first sweep, we store prefix products directly in our output array. In the second sweep, we traverse backward, multiplying the result by a running `postfix` accumulator."
  },
  {
    id: 8,
    name: "Longest Consecutive Sequence",
    category: "Arrays & Hashing",
    difficulty: "Medium",
    leetCodeUrl: "https://leetcode.com/problems/longest-consecutive-sequence/",
    description: "Given an unsorted array of integers `nums`, return *the length of the longest consecutive elements sequence.*\n\nYou must write an algorithm that runs in `O(n)` time.",
    examples: [
      { input: "nums = [100,4,200,1,3,2]", output: "4", explanation: "The longest consecutive elements sequence is [1, 2, 3, 4]. Therefore its length is 4." }
    ],
    constraints: ["`0 <= nums.length <= 10^5`", "`-10^9 <= nums[i] <= 10^9`"],
    starterCode: {
      cpp: `#include <iostream>\n#include <vector>\n#include <unordered_set>\n#include <algorithm>\n\nusing namespace std;\n\nclass Solution {\npublic:\n    int longestConsecutive(vector<int>& nums) {\n        // Write code here\n        return 0;\n    }\n};\n\nint main() {\n    Solution sol;\n    vector<int> nums = {100, 4, 200, 1, 3, 2};\n    cout << sol.longestConsecutive(nums) << endl;\n    return 0;\n}`,
      python: `from typing import List\n\nclass Solution:\n    def longestConsecutive(self, nums: List[int]) -> int:\n        # Write code here\n        return 0\n\nif __name__ == "__main__":\n    sol = Solution()\n    print(sol.longestConsecutive([100, 4, 200, 1, 3, 2]))`
    },
    solutions: {
      cpp: `#include <iostream>\n#include <vector>\n#include <unordered_set>\n#include <algorithm>\n\nusing namespace std;\n\nclass Solution {\npublic:\n    int longestConsecutive(vector<int>& nums) {\n        unordered_set<int> num_set(nums.begin(), nums.end());\n        int longest = 0;\n        for (int num : num_set) {\n            if (!num_set.count(num - 1)) {\n                int current_num = num;\n                int current_streak = 1;\n                while (num_set.count(current_num + 1)) {\n                    current_num += 1;\n                    current_streak += 1;\n                }\n                longest = max(longest, current_streak);\n            }\n        }\n        return longest;\n    }\n};\n\nint main() {\n    Solution sol;\n    vector<int> nums = {100, 4, 200, 1, 3, 2};\n    cout << "Longest streak: " << sol.longestConsecutive(nums) << " (Expected: 4)" << endl;\n    return 0;\n}`,
      python: `from typing import List\n\nclass Solution:\n    def longestConsecutive(self, nums: List[int]) -> int:\n        numSet = set(nums)\n        longest = 0\n        \n        for n in numSet:\n            if (n - 1) not in numSet:\n                length = 1\n                while (n + length) in numSet:\n                    length += 1\n                longest = max(length, longest)\n        return longest\n\nif __name__ == "__main__":\n    sol = Solution()\n    print(f"Longest streak: {sol.longestConsecutive([100, 4, 200, 1, 3, 2])} (Expected: 4)")`
    },
    complexity: { time: "O(n)", space: "O(n)" },
    explanation: "Insert all numbers into a Hash Set to allow $O(1)$ lookups. Iterate through the set. A number `n` is the *start* of a sequence if `n - 1` is not in the set. If it is a start, we count how far the sequence goes by incrementing `n` and looking it up in our set. Each number is visited at most twice (once in the outer loop, and once during sequence builds), achieving $O(n)$ time."
  },

  // ==================== TWO POINTERS ====================
  {
    id: 9,
    name: "Valid Palindrome",
    category: "Two Pointers",
    difficulty: "Easy",
    leetCodeUrl: "https://leetcode.com/problems/valid-palindrome/",
    description: "A phrase is a **palindrome** if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward. Alphanumeric characters include letters and numbers.\n\nGiven a string `s`, return `true` *if it is a **palindrome**, or* `false` *otherwise*.",
    examples: [
      { input: "s = \"A man, a plan, a canal: Panama\"", output: "true", explanation: "\"amanaplanacanalpanama\" is a palindrome." }
    ],
    constraints: ["`1 <= s.length <= 2 * 10^5`", "`s` consists only of printable ASCII characters."],
    starterCode: {
      cpp: `#include <iostream>\n#include <string>\n#include <cctype>\n\nusing namespace std;\n\nclass Solution {\npublic:\n    bool isPalindrome(string s) {\n        // Write code here\n        return false;\n    }\n};\n\nint main() {\n    Solution sol;\n    cout << (sol.isPalindrome("A man, a plan, a canal: Panama") ? "True" : "False") << endl;\n    return 0;\n}`,
      python: `class Solution:\n    def isPalindrome(self, s: str) -> bool:\n        # Write code here\n        return False\n\nif __name__ == "__main__":\n    sol = Solution()\n    print(sol.isPalindrome("A man, a plan, a canal: Panama"))`
    },
    solutions: {
      cpp: `#include <iostream>\n#include <string>\n#include <cctype>\n\nusing namespace std;\n\nclass Solution {\npublic:\n    bool isPalindrome(string s) {\n        int l = 0, r = s.length() - 1;\n        while (l < r) {\n            while (l < r && !isalnum(s[l])) l++;\n            while (l < r && !isalnum(s[r])) r--;\n            if (tolower(s[l]) != tolower(s[r])) return false;\n            l++;\n            r--;\n        }\n        return true;\n    }\n};\n\nint main() {\n    Solution sol;\n    string s1 = "A man, a plan, a canal: Panama";\n    string s2 = "race a car";\n    cout << "Test 1: " << (sol.isPalindrome(s1) ? "True" : "False") << " (Expected: True)" << endl;\n    cout << "Test 2: " << (sol.isPalindrome(s2) ? "True" : "False") << " (Expected: False)" << endl;\n    return 0;\n}`,
      python: `class Solution:\n    def isPalindrome(self, s: str) -> bool:\n        l, r = 0, len(s) - 1\n        while l < r:\n            while l < r and not self.alphaNum(s[l]):\n                l += 1\n            while r > l and not self.alphaNum(s[r]):\n                r -= 1\n            if s[l].lower() != s[r].lower():\n                return False\n            l, r = l + 1, r - 1\n        return True\n        \n    def alphaNum(self, c):\n        return (ord('A') <= ord(c) <= ord('Z') or\n                ord('a') <= ord(c) <= ord('z') or\n                ord('0') <= ord(c) <= ord('9'))\n\nif __name__ == "__main__":\n    sol = Solution()\n    print(f"Test 1: {sol.isPalindrome('A man, a plan, a canal: Panama')} (Expected: True)")\n    print(f"Test 2: {sol.isPalindrome('race a car')} (Expected: False)")`
    },
    complexity: { time: "O(n)", space: "O(1)" },
    explanation: "We place two pointers at the start (`l`) and end (`r`) of the string. We increment `l` and decrement `r` to skip non-alphanumeric characters. Once both point to valid characters, we compare their lowercase values. If they differ, it is not a palindrome. We continue until the pointers meet."
  },
  {
    id: 10,
    name: "Two Sum II - Input Array Is Sorted",
    category: "Two Pointers",
    difficulty: "Medium",
    leetCodeUrl: "https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/",
    description: "Given a **1-indexed** array of integers `numbers` that is already ***sorted in non-decreasing order***, find two numbers such that they add up to a specific `target` number.\n\nReturn the indices of the two numbers, **index1** and **index2**, added by one as an integer array `[index1, index2]` of length 2.\n\nThe tests are generated such that there is **exactly one solution**. You **may not** use the same element twice.",
    examples: [
      { input: "numbers = [2,7,11,15], target = 9", output: "[1,2]" }
    ],
    constraints: ["`2 <= numbers.length <= 3 * 10^4`", "`-1000 <= numbers[i] <= 1000`", "`numbers` is sorted in non-decreasing order.", "Only one solution exists."],
    starterCode: {
      cpp: `#include <iostream>\n#include <vector>\n\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> twoSum(vector<int>& numbers, int target) {\n        // Write code here\n        return {};\n    }\n};\n\nint main() {\n    Solution sol;\n    vector<int> nums = {2, 7, 11, 15};\n    vector<int> res = sol.twoSum(nums, 9);\n    cout << "[" << res[0] << ", " << res[1] << "]" << endl;\n    return 0;\n}`,
      python: `from typing import List\n\nclass Solution:\n    def twoSum(self, numbers: List[int], target: int) -> List[int]:\n        # Write code here\n        return []\n\nif __name__ == "__main__":\n    sol = Solution()\n    print(sol.twoSum([2, 7, 11, 15], 9))`
    },
    solutions: {
      cpp: `#include <iostream>\n#include <vector>\n\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> twoSum(vector<int>& numbers, int target) {\n        int l = 0, r = numbers.size() - 1;\n        while (l < r) {\n            int sum = numbers[l] + numbers[r];\n            if (sum == target) return {l + 1, r + 1};\n            else if (sum < target) l++;\n            else r--;\n        }\n        return {};\n    }\n};\n\nint main() {\n    Solution sol;\n    vector<int> nums = {2, 7, 11, 15};\n    vector<int> res = sol.twoSum(nums, 9);\n    cout << "Indices: [" << res[0] << ", " << res[1] << "] (Expected: [1, 2])" << endl;\n    return 0;\n}`,
      python: `from typing import List\n\nclass Solution:\n    def twoSum(self, numbers: List[int], target: int) -> List[int]:\n        l, r = 0, len(numbers) - 1\n        while l < r:\n            curSum = numbers[l] + numbers[r]\n            if curSum > target:\n                r -= 1\n            elif curSum < target:\n                l += 1\n            else:\n                return [l + 1, r + 1]\n\nif __name__ == "__main__":\n    sol = Solution()\n    print(f"Indices: {sol.twoSum([2, 7, 11, 15], 9)} (Expected: [1, 2])")`
    },
    complexity: { time: "O(n)", space: "O(1)" },
    explanation: "Because the array is sorted, we can avoid hashing. Place a pointer at the beginning (`l`) and one at the end (`r`). Compute the sum `numbers[l] + numbers[r]`. If the sum matches the target, return 1-based indices. If the sum is too small, increase `l`. If the sum is too large, decrease `r`."
  },
  {
    id: 11,
    name: "3Sum",
    category: "Two Pointers",
    difficulty: "Medium",
    leetCodeUrl: "https://leetcode.com/problems/3sum/",
    description: "Given an integer array `nums`, return all the triplets `[nums[i], nums[j], nums[k]]` such that `i != j`, `i != k`, and `j != k`, and `nums[i] + nums[j] + nums[k] == 0`.\n\nNotice that the solution set must not contain duplicate triplets.",
    examples: [
      { input: "nums = [-1,0,1,2,-1,-4]", output: "[[-1,-1,2],[-1,0,1]]" }
    ],
    constraints: ["`3 <= nums.length <= 3000`", "`-10^5 <= nums[i] <= 10^5`"],
    starterCode: {
      cpp: `#include <iostream>\n#include <vector>\n#include <algorithm>\n\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<vector<int>> threeSum(vector<int>& nums) {\n        // Write code here\n        return {};\n    }\n};\n\nint main() {\n    Solution sol;\n    vector<int> nums = {-1, 0, 1, 2, -1, -4};\n    vector<vector<int>> res = sol.threeSum(nums);\n    for (auto& row : res) cout << "[" << row[0] << "," << row[1] << "," << row[2] << "] ";\n    cout << endl;\n    return 0;\n}`,
      python: `from typing import List\n\nclass Solution:\n    def threeSum(self, nums: List[int]) -> List[List[int]]:\n        # Write code here\n        return []\n\nif __name__ == "__main__":\n    sol = Solution()\n    print(sol.threeSum([-1, 0, 1, 2, -1, -4]))`
    },
    solutions: {
      cpp: `#include <iostream>\n#include <vector>\n#include <algorithm>\n\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<vector<int>> threeSum(vector<int>& nums) {\n        vector<vector<int>> res;\n        sort(nums.begin(), nums.end());\n        int n = nums.size();\n        for (int i = 0; i < n - 2; ++i) {\n            if (i > 0 && nums[i] == nums[i - 1]) continue;\n            int l = i + 1, r = n - 1;\n            while (l < r) {\n                int sum = nums[i] + nums[l] + nums[r];\n                if (sum == 0) {\n                    res.push_back({nums[i], nums[l], nums[r]});\n                    while (l < r && nums[l] == nums[l + 1]) l++;\n                    while (l < r && nums[r] == nums[r - 1]) r--;\n                    l++; r--;\n                } else if (sum < 0) l++;\n                else r--;\n            }\n        }\n        return res;\n    }\n};\n\nint main() {\n    Solution sol;\n    vector<int> nums = {-1, 0, 1, 2, -1, -4};\n    vector<vector<int>> res = sol.threeSum(nums);\n    cout << "Triplets:\\n";\n    for (auto& row : res) {\n        cout << "[" << row[0] << "," << row[1] << "," << row[2] << "] ";\n    }\n    cout << endl;\n    return 0;\n}`,
      python: `from typing import List\n\nclass Solution:\n    def threeSum(self, nums: List[int]) -> List[List[int]]:\n        res = []\n        nums.sort()\n        for i, a in enumerate(nums):\n            if i > 0 and a == nums[i - 1]:\n                continue\n            l, r = i + 1, len(nums) - 1\n            while l < r:\n                threeSum = a + nums[l] + nums[r]\n                if threeSum > 0:\n                    r -= 1\n                elif threeSum < 0:\n                    l += 1\n                else:\n                    res.append([a, nums[l], nums[r]])\n                    l += 1\n                    while nums[l] == nums[l - 1] and l < r:\n                        l += 1\n        return res\n\nif __name__ == "__main__":\n    sol = Solution()\n    print(f"Triplets: {sol.threeSum([-1, 0, 1, 2, -1, -4])}")`
    },
    complexity: { time: "O(n^2)", space: "O(1) (excluding sorting)" },
    explanation: "First, sort the array. This allows us to lock a first element `nums[i]` and perform a Two Sum II scan on the remainder of the array `[i+1, n-1]`. To prevent duplicates, we skip indices when they match their predecessor."
  },
  {
    id: 12,
    name: "Container With Most Water",
    category: "Two Pointers",
    difficulty: "Medium",
    leetCodeUrl: "https://leetcode.com/problems/container-with-most-water/",
    description: "You are given an integer array `height` of length `n`. There are `n` vertical lines drawn such that the two endpoints of the `i`-th line are `(i, 0)` and `(i, height[i])`.\n\nFind two lines that together with the x-axis form a container, such that the container contains the most water.\n\nReturn *the maximum amount of water a container can store*.",
    examples: [
      { input: "height = [1,8,6,2,5,4,8,3,7]", output: "49" }
    ],
    constraints: ["`n == height.length`", "`2 <= n <= 10^5`", "`0 <= height[i] <= 10^4`"],
    starterCode: {
      cpp: `#include <iostream>\n#include <vector>\n#include <algorithm>\n\nusing namespace std;\n\nclass Solution {\npublic:\n    int maxArea(vector<int>& height) {\n        // Write code here\n        return 0;\n    }\n};\n\nint main() {\n    Solution sol;\n    vector<int> heights = {1, 8, 6, 2, 5, 4, 8, 3, 7};\n    cout << sol.maxArea(heights) << endl;\n    return 0;\n}`,
      python: `from typing import List\n\nclass Solution:\n    def maxArea(self, height: List[int]) -> int:\n        # Write code here\n        return 0\n\nif __name__ == "__main__":\n    sol = Solution()\n    print(sol.maxArea([1, 8, 6, 2, 5, 4, 8, 3, 7]))`
    },
    solutions: {
      cpp: `#include <iostream>\n#include <vector>\n#include <algorithm>\n\nusing namespace std;\n\nclass Solution {\npublic:\n    int maxArea(vector<int>& height) {\n        int max_water = 0;\n        int l = 0, r = height.size() - 1;\n        while (l < r) {\n            int w = r - l;\n            int h = min(height[l], height[r]);\n            max_water = max(max_water, w * h);\n            if (height[l] < height[r]) l++;\n            else r--;\n        }\n        return max_water;\n    }\n};\n\nint main() {\n    Solution sol;\n    vector<int> heights = {1, 8, 6, 2, 5, 4, 8, 3, 7};\n    cout << "Max water: " << sol.maxArea(heights) << " (Expected: 49)" << endl;\n    return 0;\n}`,
      python: `from typing import List\n\nclass Solution:\n    def maxArea(self, height: List[int]) -> int:\n        res = 0\n        l, r = 0, len(height) - 1\n        while l < r:\n            area = (r - l) * min(height[l], height[r])\n            res = max(res, area)\n            if height[l] < height[r]:\n                l += 1\n            else:\n                r -= 1\n        return res\n\nif __name__ == "__main__":\n    sol = Solution()\n    print(f"Max Water: {sol.maxArea([1, 8, 6, 2, 5, 4, 8, 3, 7])} (Expected: 49)")`
    },
    complexity: { time: "O(n)", space: "O(1)" },
    explanation: "Place pointers at the boundaries (`l = 0` and `r = n-1`). The water volume is `(r - l) * min(height[l], height[r])`. To maximize area, we should move the pointer pointing to the shorter vertical bar inward, hoping to find a taller bar to compensate for the decreasing width."
  },

  // ==================== SLIDING WINDOW ====================
  {
    id: 13,
    name: "Best Time to Buy and Sell Stock",
    category: "Sliding Window",
    difficulty: "Easy",
    leetCodeUrl: "https://leetcode.com/problems/best-time-to-buy-and-sell-stock/",
    description: "You are given an array `prices` where `prices[i]` is the price of a given stock on the `i`-th day.\n\nYou want to maximize your profit by choosing a **single day** to buy one stock and choosing a **different day in the future** to sell that stock.\n\nReturn *the maximum profit you can achieve from this transaction*. If you cannot achieve any profit, return `0`.",
    examples: [
      { input: "prices = [7,1,5,3,6,4]", output: "5", explanation: "Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6-1 = 5." }
    ],
    constraints: ["`1 <= prices.length <= 10^5`", "`0 <= prices[i] <= 10^4`"],
    starterCode: {
      cpp: `#include <iostream>\n#include <vector>\n#include <algorithm>\n#include <climits>\n\nusing namespace std;\n\nclass Solution {\npublic:\n    int maxProfit(vector<int>& prices) {\n        // Write code here\n        return 0;\n    }\n};\n\nint main() {\n    Solution sol;\n    vector<int> prices = {7, 1, 5, 3, 6, 4};\n    cout << sol.maxProfit(prices) << endl;\n    return 0;\n}`,
      python: `from typing import List\n\nclass Solution:\n    def maxProfit(self, prices: List[int]) -> int:\n        # Write code here\n        return 0\n\nif __name__ == "__main__":\n    sol = Solution()\n    print(sol.maxProfit([7, 1, 5, 3, 6, 4]))`
    },
    solutions: {
      cpp: `#include <iostream>\n#include <vector>\n#include <algorithm>\n#include <climits>\n\nusing namespace std;\n\nclass Solution {\npublic:\n    int maxProfit(vector<int>& prices) {\n        int min_price = INT_MAX;\n        int max_prof = 0;\n        for (int p : prices) {\n            if (p < min_price) min_price = p;\n            else max_prof = max(max_prof, p - min_price);\n        }\n        return max_prof;\n    }\n};\n\nint main() {\n    Solution sol;\n    vector<int> prices = {7, 1, 5, 3, 6, 4};\n    cout << "Max Profit: " << sol.maxProfit(prices) << " (Expected: 5)" << endl;\n    return 0;\n}`,
      python: `from typing import List\n\nclass Solution:\n    def maxProfit(self, prices: List[int]) -> int:\n        l, r = 0, 1 # buy and sell\n        maxP = 0\n        while r < len(prices):\n            if prices[l] < prices[r]:\n                profit = prices[r] - prices[l]\n                maxP = max(maxP, profit)\n            else:\n                l = r\n            r += 1\n        return maxP\n\nif __name__ == "__main__":\n    sol = Solution()\n    print(f"Max Profit: {sol.maxProfit([7, 1, 5, 3, 6, 4])} (Expected: 5)")`
    },
    complexity: { time: "O(n)", space: "O(1)" },
    explanation: "Keep track of the minimum price observed so far. As we iterate through the prices day by day, we compute potential profit (`prices[i] - min_price`). If this exceeds our current maximum profit, we update our maximum. If we find a lower price than our minimum, we update the minimum."
  },
  {
    id: 14,
    name: "Longest Substring Without Repeating Characters",
    category: "Sliding Window",
    difficulty: "Medium",
    leetCodeUrl: "https://leetcode.com/problems/longest-substring-without-repeating-characters/",
    description: "Given a string `s`, find the length of the **longest substring** without repeating characters.",
    examples: [
      { input: "s = \"abcabcbb\"", output: "3", explanation: "The answer is \"abc\", with the length of 3." }
    ],
    constraints: ["`0 <= s.length <= 5 * 10^4`", "`s` consists of English letters, digits, symbols and spaces."],
    starterCode: {
      cpp: `#include <iostream>\n#include <string>\n#include <unordered_set>\n#include <algorithm>\n\nusing namespace std;\n\nclass Solution {\npublic:\n    int lengthOfLongestSubstring(string s) {\n        // Write code here\n        return 0;\n    }\n};\n\nint main() {\n    Solution sol;\n    cout << sol.lengthOfLongestSubstring("abcabcbb") << endl;\n    return 0;\n}`,
      python: `class Solution:\n    def lengthOfLongestSubstring(self, s: str) -> int:\n        # Write code here\n        return 0\n\nif __name__ == "__main__":\n    sol = Solution()\n    print(sol.lengthOfLongestSubstring("abcabcbb"))`
    },
    solutions: {
      cpp: `#include <iostream>\n#include <string>\n#include <unordered_set>\n#include <algorithm>\n\nusing namespace std;\n\nclass Solution {\npublic:\n    int lengthOfLongestSubstring(string s) {\n        unordered_set<char> chars;\n        int l = 0, max_len = 0;\n        for (int r = 0; r < s.length(); ++r) {\n            while (chars.count(s[r])) {\n                chars.erase(s[l]);\n                l++;\n            }\n            chars.insert(s[r]);\n            max_len = max(max_len, r - l + 1);\n        }\n        return max_len;\n    }\n};\n\nint main() {\n    Solution sol;\n    string s = "abcabcbb";\n    cout << "Longest Substring without repeating: " << sol.lengthOfLongestSubstring(s) << " (Expected: 3)" << endl;\n    return 0;\n}`,
      python: `class Solution:\n    def lengthOfLongestSubstring(self, s: str) -> int:\n        charSet = set()\n        l = 0\n        res = 0\n        for r in range(len(s)):\n            while s[r] in charSet:\n                charSet.remove(s[l])\n                l += 1\n            charSet.add(s[r])\n            res = max(res, r - l + 1)\n        return res\n\nif __name__ == "__main__":\n    sol = Solution()\n    print(f"Longest Substring: {sol.lengthOfLongestSubstring('abcabcbb')} (Expected: 3)")`
    },
    complexity: { time: "O(n)", space: "O(min(a, n))" },
    explanation: "We utilize a sliding window represented by pointer `l` and pointer `r`. We scan through the string with pointer `r` and record encountered characters inside a Hash Set. If `s[r]` is already in the set, we shrink the window from the left by removing `s[l]` and incrementing `l` until `s[r]` is no longer duplicated."
  },
  {
    id: 15,
    name: "Longest Repeating Character Replacement",
    category: "Sliding Window",
    difficulty: "Medium",
    leetCodeUrl: "https://leetcode.com/problems/longest-repeating-character-replacement/",
    description: "You are given a string `s` and an integer `k`. You can choose any character of the string and change it to any other uppercase English character. You can perform this operation at most `k` times.\n\nReturn *the length of the longest substring containing the same letter you can get after performing the above operations*.",
    examples: [
      { input: "s = \"ABAB\", k = 2", output: "4", explanation: "Replace the two 'A's with 'B's or vice versa." }
    ],
    constraints: ["`1 <= s.length <= 10^5`", "`s` consists of uppercase English letters.", "`0 <= k <= s.length`"],
    starterCode: {
      cpp: `#include <iostream>\n#include <string>\n#include <algorithm>\n\nusing namespace std;\n\nclass Solution {\npublic:\n    int characterReplacement(string s, int k) {\n        // Write code here\n        return 0;\n    }\n};\n\nint main() {\n    Solution sol;\n    cout << sol.characterReplacement("ABAB", 2) << endl;\n    return 0;\n}`,
      python: `class Solution:\n    def characterReplacement(self, s: str, k: int) -> int:\n        # Write code here\n        return 0\n\nif __name__ == "__main__":\n    sol = Solution()\n    print(sol.characterReplacement("ABAB", 2))`
    },
    solutions: {
      cpp: `#include <iostream>\n#include <string>\n#include <algorithm>\n\nusing namespace std;\n\nclass Solution {\npublic:\n    int characterReplacement(string s, int k) {\n        int counts[26] = {0};\n        int l = 0, max_f = 0, max_len = 0;\n        for (int r = 0; r < s.length(); ++r) {\n            counts[s[r] - 'A']++;\n            max_f = max(max_f, counts[s[r] - 'A']);\n            int window_len = r - l + 1;\n            if (window_len - max_f > k) {\n                counts[s[l] - 'A']--;\n                l++;\n            }\n            max_len = max(max_len, r - l + 1);\n        }\n        return max_len;\n    }\n};\n\nint main() {\n    Solution sol;\n    cout << "Longest Replacement length: " << sol.characterReplacement("ABAB", 2) << " (Expected: 4)" << endl;\n    return 0;\n}`,
      python: `class Solution:\n    def characterReplacement(self, s: str, k: int) -> int: \n        count = {}\n        res = 0\n        l = 0\n        maxf = 0\n        for r in range(len(s)):\n            count[s[r]] = 1 + count.get(s[r], 0)\n            maxf = max(maxf, count[s[r]])\n            if (r - l + 1) - maxf > k:\n                count[s[l]] -= 1\n                l += 1\n            res = max(res, r - l + 1)\n        return res\n\nif __name__ == "__main__":\n    sol = Solution()\n    print(f"Longest Replacement: {sol.characterReplacement('ABAB', 2)} (Expected: 4)")`
    },
    complexity: { time: "O(n)", space: "O(26) = O(1)" },
    explanation: "We utilize a sliding window. At any point, our window size is `r - l + 1`. The number of replacement operations needed to make all characters in the window equal is `window_len - max_frequency`. If this count exceeds `k`, we shrink the window by decrementing the count of `s[l]` and advancing `l`. `maxf` represents the maximum frequency of any character seen in a window."
  },

  // ==================== STACK ====================
  {
    id: 16,
    name: "Valid Parentheses",
    category: "Stack",
    difficulty: "Easy",
    leetCodeUrl: "https://leetcode.com/problems/valid-parentheses/",
    description: "Given a string `s` containing just the characters `'('`, `')'`, `'{'`, `'}'`, `'['` and `']'`, determine if the input string is valid.\n\nAn input string is valid if:\n1. Open brackets must be closed by the same type of brackets.\n2. Open brackets must be closed in the correct order.\n3. Every close bracket has a corresponding open bracket of the same type.",
    examples: [
      { input: "s = \"()[]{}\"", output: "true" },
      { input: "s = \"(]\"", output: "false" }
    ],
    constraints: ["`1 <= s.length <= 10^4`", "`s` consists of parentheses only `'()[]{}'`."],
    starterCode: {
      cpp: `#include <iostream>\n#include <string>\n#include <stack>\n\nusing namespace std;\n\nclass Solution {\npublic:\n    bool isValid(string s) {\n        // Write code here\n        return false;\n    }\n};\n\nint main() {\n    Solution sol;\n    cout << (sol.isValid("()[]{}") ? "True" : "False") << endl;\n    return 0;\n}`,
      python: `class Solution:\n    def isValid(self, s: str) -> bool:\n        # Write code here\n        return False\n\nif __name__ == "__main__":\n    sol = Solution()\n    print(sol.isValid("()[]{}"))`
    },
    solutions: {
      cpp: `#include <iostream>\n#include <string>\n#include <stack>\n\nusing namespace std;\n\nclass Solution {\npublic:\n    bool isValid(string s) {\n        stack<char> st;\n        for (char c : s) {\n            if (c == '(' || c == '[' || c == '{') {\n                st.push(c);\n            } else {\n                if (st.empty()) return false;\n                char top = st.top();\n                if ((c == ')' && top != '(') ||\n                    (c == ']' && top != '[') ||\n                    (c == '}' && top != '{')) return false;\n                st.pop();\n            }\n        }\n        return st.empty();\n    }\n};\n\nint main() {\n    Solution sol;\n    string s1 = "()[]{}";\n    string s2 = "(]";\n    cout << "Test 1: " << (sol.isValid(s1) ? "True" : "False") << " (Expected: True)" << endl;\n    cout << "Test 2: " << (sol.isValid(s2) ? "True" : "False") << " (Expected: False)" << endl;\n    return 0;\n}`,
      python: `class Solution:\n    def isValid(self, s: str) -> bool:\n        Map = {")": "(", "]": "[", "}": "{"}\n        stack = []\n        for c in s:\n            if c not in Map:\n                stack.append(c)\n                continue\n            if not stack or stack[-1] != Map[c]:\n                return False\n            stack.pop()\n        return not stack\n\nif __name__ == "__main__":\n    sol = Solution()\n    print(f"Test 1: {sol.isValid('()[]{}')} (Expected: True)")\n    print(f"Test 2: {sol.isValid('(]')} (Expected: False)")`
    },
    complexity: { time: "O(n)", space: "O(n)" },
    explanation: "We loop through the string. When we encounter an opening bracket, we push it to our stack. When we encounter a closing bracket, we check if the stack is empty or if the top of the stack does not match the closing character. If either occurs, it is invalid. Otherwise, we pop from the stack. Finally, verify the stack is empty."
  },
  {
    id: 17,
    name: "Min Stack",
    category: "Stack",
    difficulty: "Medium",
    leetCodeUrl: "https://leetcode.com/problems/min-stack/",
    description: "Design a stack that supports push, pop, top, and retrieving the minimum element in constant time.\n\nImplement the `MinStack` class:\n* `MinStack()` initializes the stack object.\n* `void push(int val)` pushes the element `val` onto the stack.\n* `void pop()` removes the element on the top of the stack.\n* `int top()` gets the top element of the stack.\n* `int getMin()` retrieves the minimum element in the stack.\n\nYou must implement a solution with `O(1)` time complexity for each function.",
    examples: [
      { input: "[\"MinStack\",\"push\",\"push\",\"push\",\"getMin\",\"pop\",\"top\",\"getMin\"]\\n[[],[-2],[0],[-3],[],[],[],[]]", output: "[null,null,null,null,-3,null,0,-2]" }
    ],
    constraints: ["`-2^31 <= val <= 2^31 - 1`", "Methods `pop`, `top` and `getMin` will always be called on **non-empty** stacks."],
    starterCode: {
      cpp: `#include <iostream>\n#include <stack>\n\nusing namespace std;\n\nclass MinStack {\npublic:\n    MinStack() {\n        \n    }\n    \n    void push(int val) {\n        \n    }\n    \n    void pop() {\n        \n    }\n    \n    int top() {\n        return 0;\n    }\n    \n    int getMin() {\n        return 0;\n    }\n};\n\nint main() {\n    MinStack* obj = new MinStack();\n    obj->push(-2);\n    obj->push(0);\n    obj->push(-3);\n    cout << obj->getMin() << endl;\n    return 0;\n}`,
      python: `class MinStack:\n    def __init__(self):\n        pass\n        \n    def push(self, val: int) -> None:\n        pass\n        \n    def pop(self) -> None:\n        pass\n        \n    def top(self) -> int:\n        return 0\n        \n    def getMin(self) -> int:\n        return 0\n\nif __name__ == "__main__":\n    obj = MinStack()\n    obj.push(-2)\n    obj.push(0)\n    obj.push(-3)\n    print(obj.getMin())`
    },
    solutions: {
      cpp: `#include <iostream>\n#include <stack>\n\nusing namespace std;\n\nclass MinStack {\nprivate:\n    stack<int> st;\n    stack<int> min_st;\npublic:\n    MinStack() {}\n    \n    void push(int val) {\n        st.push(val);\n        if (min_st.empty() || val <= min_st.top()) {\n            min_st.push(val);\n        }\n    }\n    \n    void pop() {\n        if (st.top() == min_st.top()) {\n            min_st.pop();\n        }\n        st.pop();\n    }\n    \n    int top() {\n        return st.top();\n    }\n    \n    int getMin() {\n        return min_st.top();\n    }\n};\n\nint main() {\n    MinStack minStack;\n    minStack.push(-2);\n    minStack.push(0);\n    minStack.push(-3);\n    cout << "Min element: " << minStack.getMin() << " (Expected: -3)" << endl;\n    minStack.pop();\n    cout << "Top element: " << minStack.top() << " (Expected: 0)" << endl;\n    cout << "Min element: " << minStack.getMin() << " (Expected: -2)" << endl;\n    return 0;\n}`,
      python: `class MinStack:\n    def __init__(self):\n        self.stack = []\n        self.minStack = []\n        \n    def push(self, val: int) -> None:\n        self.stack.append(val)\n        val = min(val, self.minStack[-1] if self.minStack else val)\n        self.minStack.append(val)\n        \n    def pop(self) -> None:\n        self.stack.pop()\n        self.minStack.pop()\n        \n    def top(self) -> int:\n        return self.stack[-1]\n        \n    def getMin(self) -> int:\n        return self.minStack[-1]\n\nif __name__ == "__main__":\n    obj = MinStack()\n    obj.push(-2)\n    obj.push(0)\n    obj.push(-3)\n    print(f"Min element: {obj.getMin()} (Expected: -3)")\n    obj.pop()\n    print(f"Top element: {obj.top()} (Expected: 0)")\n    print(f"Min element: {obj.getMin()} (Expected: -2)")`
    },
    complexity: { time: "O(1) per operation", space: "O(n)" },
    explanation: "To find the minimum value in $O(1)$ time, we keep a parallel stack (or stack of pairs) representing the minimum value at each depth level of our primary stack. When we push a value, we calculate the minimum between it and the top of the min-stack, and push that minimum. Popping keeps both stacks aligned."
  },
  {
    id: 18,
    name: "Daily Temperatures",
    category: "Stack",
    difficulty: "Medium",
    leetCodeUrl: "https://leetcode.com/problems/daily-temperatures/",
    description: "Given an array of integers `temperatures` represents the daily temperatures, return *an array* `answer` *such that* `answer[i]` *is the number of days you have to wait after the* `i`-th *day to get a warmer temperature*. If there is no future day for which this is possible, keep `answer[i] == 0` instead.",
    examples: [
      { input: "temperatures = [73,74,75,71,69,72,76,73]", output: "[1,1,4,2,1,1,0,0]" }
    ],
    constraints: ["`1 <= temperatures.length <= 10^5`", "`30 <= temperatures[i] <= 100`"],
    starterCode: {
      cpp: `#include <iostream>\n#include <vector>\n#include <stack>\n\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> dailyTemperatures(vector<int>& temperatures) {\n        // Write code here\n        return {};\n    }\n};\n\nint main() {\n    Solution sol;\n    vector<int> temps = {73, 74, 75, 71, 69, 72, 76, 73};\n    vector<int> res = sol.dailyTemperatures(temps);\n    for (int x : res) cout << x << " ";\n    cout << endl;\n    return 0;\n}`,
      python: `from typing import List\n\nclass Solution:\n    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:\n        # Write code here\n        return []\n\nif __name__ == "__main__":\n    sol = Solution()\n    print(sol.dailyTemperatures([73, 74, 75, 71, 69, 72, 76, 73]))`
    },
    solutions: {
      cpp: `#include <iostream>\n#include <vector>\n#include <stack>\n\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> dailyTemperatures(vector<int>& temperatures) {\n        int n = temperatures.size();\n        vector<int> res(n, 0);\n        stack<int> st;\n        for (int i = 0; i < n; ++i) {\n            while (!st.empty() && temperatures[i] > temperatures[st.top()]) {\n                int prev_idx = st.top();\n                st.pop();\n                res[prev_idx] = i - prev_idx;\n            }\n            st.push(i);\n        }\n        return res;\n    }\n};\n\nint main() {\n    Solution sol;\n    vector<int> temps = {73, 74, 75, 71, 69, 72, 76, 73};\n    vector<int> res = sol.dailyTemperatures(temps);\n    cout << "Wait Days: ";\n    for (int x : res) cout << x << " ";\n    cout << " (Expected: 1 1 4 2 1 1 0 0)" << endl;\n    return 0;\n}`,
      python: `from typing import List\n\nclass Solution:\n    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:\n        res = [0] * len(temperatures)\n        stack = [] # pair: [temp, index]\n        for i, t in enumerate(temperatures):\n            while stack and t > stack[-1][0]:\n                stackT, stackI = stack.pop()\n                res[stackI] = i - stackI\n            stack.append([t, i])\n        return res\n\nif __name__ == "__main__":\n    sol = Solution()\n    print(f"Wait Days: {sol.dailyTemperatures([73, 74, 75, 71, 69, 72, 76, 73])} (Expected: [1, 1, 4, 2, 1, 1, 0, 0])")`
    },
    complexity: { time: "O(n)", space: "O(n)" },
    explanation: "We utilize a Monotonic Decreasing Stack. As we iterate through the temperatures, we check if the current temperature is warmer than the temperature of the index sitting at the top of the stack. If it is, we pop that index, calculate the difference (`current_index - popped_index`), and store it. Then we push the current index to the stack."
  },

  // ==================== BINARY SEARCH ====================
  {
    id: 19,
    name: "Binary Search",
    category: "Binary Search",
    difficulty: "Easy",
    leetCodeUrl: "https://leetcode.com/problems/binary-search/",
    description: "Given an array of integers `nums` which is sorted in ascending order, and an integer `target`, write a function to search `target` in `nums`. If `target` exists, then return its index. Otherwise, return `-1`.\n\nYou must write an algorithm with `O(log n)` runtime complexity.",
    examples: [
      { input: "nums = [-1,0,3,5,9,12], target = 9", output: "4" }
    ],
    constraints: ["`1 <= nums.length <= 10^4`", "`-10^4 < nums[i], target < 10^4`", "All the integers in `nums` are **unique**.", "`nums` is sorted in ascending order."],
    starterCode: {
      cpp: `#include <iostream>\n#include <vector>\n\nusing namespace std;\n\nclass Solution {\npublic:\n    int search(vector<int>& nums, int target) {\n        // Write code here\n        return -1;\n    }\n};\n\nint main() {\n    Solution sol;\n    vector<int> nums = {-1, 0, 3, 5, 9, 12};\n    cout << sol.search(nums, 9) << endl;\n    return 0;\n}`,
      python: `from typing import List\n\nclass Solution:\n    def search(self, nums: List[int], target: int) -> int:\n        # Write code here\n        return -1\n\nif __name__ == "__main__":\n    sol = Solution()\n    print(sol.search([-1, 0, 3, 5, 9, 12], 9))`
    },
    solutions: {
      cpp: `#include <iostream>\n#include <vector>\n\nusing namespace std;\n\nclass Solution {\npublic:\n    int search(vector<int>& nums, int target) {\n        int l = 0, r = nums.size() - 1;\n        while (l <= r) {\n            int mid = l + (r - l) / 2;\n            if (nums[mid] == target) return mid;\n            else if (nums[mid] < target) l = mid + 1;\n            else r = mid - 1;\n        }\n        return -1;\n    }\n};\n\nint main() {\n    Solution sol;\n    vector<int> nums = {-1, 0, 3, 5, 9, 12};\n    cout << "Target index: " << sol.search(nums, 9) << " (Expected: 4)" << endl;\n    return 0;\n}`,
      python: `from typing import List\n\nclass Solution:\n    def search(self, nums: List[int], target: int) -> int:\n        l, r = 0, len(nums) - 1\n        while l <= r:\n            m = l + ((r - l) // 2)\n            if nums[m] > target:\n                r = m - 1\n            elif nums[m] < target:\n                l = m + 1\n            else:\n                return m\n        return -1\n\nif __name__ == "__main__":\n    sol = Solution()\n    print(f"Target index: {sol.search([-1, 0, 3, 5, 9, 12], 9)} (Expected: 4)")`
    },
    complexity: { time: "O(log n)", space: "O(1)" },
    explanation: "Maintain two boundary pointers: `l` at the start, `r` at the end. Compute the midpoint (`mid`). If the item at `mid` is equal to `target`, return `mid`. If the value at `mid` is less than `target`, shift `l = mid + 1` to search the right half. Otherwise, shift `r = mid - 1` to search the left half."
  },
  {
    id: 20,
    name: "Find Minimum in Rotated Sorted Array",
    category: "Binary Search",
    difficulty: "Medium",
    leetCodeUrl: "https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/",
    description: "Suppose an array of length `n` sorted in ascending order is **rotated** between `1` and `n` times.\n\nGiven the sorted rotated array `nums` of **unique** elements, return *the minimum element of this array*.\n\nYou must write an algorithm that runs in `O(log n)` time.",
    examples: [
      { input: "nums = [3,4,5,1,2]", output: "1" }
    ],
    constraints: ["`n == nums.length`", "`1 <= n <= 5000`", "`-5000 <= nums[i] <= 5000`", "All integers in `nums` are unique."],
    starterCode: {
      cpp: `#include <iostream>\n#include <vector>\n#include <algorithm>\n\nusing namespace std;\n\nclass Solution {\npublic:\n    int findMin(vector<int>& nums) {\n        // Write code here\n        return 0;\n    }\n};\n\nint main() {\n    Solution sol;\n    vector<int> nums = {3, 4, 5, 1, 2};\n    cout << sol.findMin(nums) << endl;\n    return 0;\n}`,
      python: `from typing import List\n\nclass Solution:\n    def findMin(self, nums: List[int]) -> int:\n        # Write code here\n        return 0\n\nif __name__ == "__main__":\n    sol = Solution()\n    print(sol.findMin([3, 4, 5, 1, 2]))`
    },
    solutions: {
      cpp: `#include <iostream>\n#include <vector>\n#include <algorithm>\n\nusing namespace std;\n\nclass Solution {\npublic:\n    int findMin(vector<int>& nums) {\n        int l = 0, r = nums.size() - 1;\n        while (l < r) {\n            int mid = l + (r - l) / 2;\n            if (nums[mid] > nums[r]) {\n                l = mid + 1;\n            } else {\n                r = mid;\n            }\n        }\n        return nums[l];\n    }\n};\n\nint main() {\n    Solution sol;\n    vector<int> nums = {3, 4, 5, 1, 2};\n    cout << "Minimum element: " << sol.findMin(nums) << " (Expected: 1)" << endl;\n    return 0;\n}`,
      python: `from typing import List\n\nclass Solution:\n    def findMin(self, nums: List[int]) -> int:\n        l, r = 0, len(nums) - 1\n        while l < r:\n            mid = l + (r - l) // 2\n            if nums[mid] > nums[r]:\n                l = mid + 1\n            else:\n                r = mid\n        return nums[l]\n\nif __name__ == "__main__":\n    sol = Solution()\n    print(f"Minimum element: {sol.findMin([3, 4, 5, 1, 2])} (Expected: 1)")`
    },
    complexity: { time: "O(log n)", space: "O(1)" },
    explanation: "In a rotated sorted array, the minimum element acts as an inflection point. In our binary search, if `nums[mid] > nums[r]`, it implies that the left half is fully ordered, and the inflection point (minimum) resides on the right side, so we search the right (`l = mid + 1`). Otherwise, the minimum is either at `mid` or in the left half, so we search the left (`r = mid`)."
  },
  {
    id: 21,
    name: "Search in Rotated Sorted Array",
    category: "Binary Search",
    difficulty: "Medium",
    leetCodeUrl: "https://leetcode.com/problems/search-in-rotated-sorted-array/",
    description: "There is an integer array `nums` sorted in ascending order (with **unique** values).\n\nPrior to being passed to your function, `nums` is **possibly rotated** at an unknown pivot index `k`.\n\nGiven the array `nums` **after** the rotation and an integer `target`, return *the index of* `target` *if it is in* `nums`, *or* `-1` *if it is not in* `nums`.\n\nYou must write an algorithm with `O(log n)` runtime complexity.",
    examples: [
      { input: "nums = [4,5,6,7,0,1,2], target = 0", output: "4" }
    ],
    constraints: ["`1 <= nums.length <= 5000`", "`-10^4 <= nums[i], target <= 10^4`", "All values of `nums` are **unique**."],
    starterCode: {
      cpp: `#include <iostream>\n#include <vector>\n\nusing namespace std;\n\nclass Solution {\npublic:\n    int search(vector<int>& nums, int target) {\n        // Write code here\n        return -1;\n    }\n};\n\nint main() {\n    Solution sol;\n    vector<int> nums = {4, 5, 6, 7, 0, 1, 2};\n    cout << sol.search(nums, 0) << endl;\n    return 0;\n}`,
      python: `from typing import List\n\nclass Solution:\n    def search(self, nums: List[int], target: int) -> int:\n        # Write code here\n        return -1\n\nif __name__ == "__main__":\n    sol = Solution()\n    print(sol.search([4, 5, 6, 7, 0, 1, 2], 0))`
    },
    solutions: {
      cpp: `#include <iostream>\n#include <vector>\n\nusing namespace std;\n\nclass Solution {\npublic:\n    int search(vector<int>& nums, int target) {\n        int l = 0, r = nums.size() - 1;\n        while (l <= r) {\n            int mid = l + (r - l) / 2;\n            if (nums[mid] == target) return mid;\n            \n            if (nums[l] <= nums[mid]) {\n                if (target >= nums[l] && target < nums[mid]) {\n                    r = mid - 1;\n                } else {\n                    l = mid + 1;\n                }\n            } \n            else {\n                if (target > nums[mid] && target <= nums[r]) {\n                    l = mid + 1;\n                } else {\n                    r = mid - 1;\n                }\n            }\n        }\n        return -1;\n    }\n};\n\nint main() {\n    Solution sol;\n    vector<int> nums = {4, 5, 6, 7, 0, 1, 2};\n    cout << "Index of 0: " << sol.search(nums, 0) << " (Expected: 4)" << endl;\n    return 0;\n}`,
      python: `from typing import List\n\nclass Solution:\n    def search(self, nums: List[int], target: int) -> int:\n        l, r = 0, len(nums) - 1\n        while l <= r:\n            mid = l + (r - l) // 2\n            if target == nums[mid]:\n                return mid\n            if nums[l] <= nums[mid]:\n                if target > nums[mid] or target < nums[l]:\n                    l = mid + 1\n                else:\n                    r = mid - 1\n            else:\n                if target < nums[mid] or target > nums[r]:\n                    r = mid - 1\n                else:\n                    l = mid + 1\n        return -1\n\nif __name__ == "__main__":\n    sol = Solution()\n    print(f"Index of 0: {sol.search([4, 5, 6, 7, 0, 1, 2], 0)} (Expected: 4)")`
    },
    complexity: { time: "O(log n)", space: "O(1)" },
    explanation: "At least one half of the rotated array must always be sorted. In our binary search, we first determine which half is sorted: left (`nums[l] <= nums[mid]`) or right (`nums[mid] <= nums[r]`). We then verify if the target falls within the sorted range. If it does, we search that half; otherwise, we search the opposite half."
  },

  // ==================== LINKED LIST ====================
  {
    id: 22,
    name: "Reverse Linked List",
    category: "Linked List",
    difficulty: "Easy",
    leetCodeUrl: "https://leetcode.com/problems/reverse-linked-list/",
    description: "Given the `head` of a singly linked list, reverse the list, and return *the reversed list*.",
    examples: [
      { input: "head = [1,2,3,4,5]", output: "[5,4,3,2,1]" }
    ],
    constraints: ["The number of nodes in the list is the range `[0, 5000]`.", "`-5000 <= Node.val <= 5000`"],
    starterCode: {
      cpp: `#include <iostream>\n\nusing namespace std;\n\nstruct ListNode {\n    int val;\n    ListNode *next;\n    ListNode(int x) : val(x), next(nullptr) {}\n};\n\nclass Solution {\npublic:\n    ListNode* reverseList(ListNode* head) {\n        // Write code here\n        return head;\n    }\n};\n\nint main() {\n    ListNode* head = new ListNode(1);\n    head->next = new ListNode(2);\n    Solution sol;\n    ListNode* rev = sol.reverseList(head);\n    cout << rev->val << " " << rev->next->val << endl;\n    return 0;\n}`,
      python: `from typing import Optional\n\nclass ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\nclass Solution:\n    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:\n        # Write code here\n        return head\n\nif __name__ == "__main__":\n    head = ListNode(1, ListNode(2))\n    sol = Solution()\n    rev = sol.reverseList(head)\n    print(f"{rev.val} -> {rev.next.val}")`
    },
    solutions: {
      cpp: `#include <iostream>\n\nusing namespace std;\n\nstruct ListNode {\n    int val;\n    ListNode *next;\n    ListNode(int x) : val(x), next(nullptr) {}\n};\n\nclass Solution {\npublic:\n    ListNode* reverseList(ListNode* head) {\n        ListNode* prev = nullptr;\n        ListNode* curr = head;\n        while (curr != nullptr) {\n            ListNode* nextTemp = curr->next;\n            curr->next = prev;\n            prev = curr;\n            curr = nextTemp;\n        }\n        return prev;\n    }\n};\n\nint main() {\n    ListNode* head = new ListNode(1);\n    head->next = new ListNode(2);\n    head->next->next = new ListNode(3);\n    \n    Solution sol;\n    ListNode* rev = sol.reverseList(head);\n    cout << "Reversed List: ";\n    while (rev) {\n        cout << rev->val << " ";\n        rev = rev->next;\n    }\n    cout << " (Expected: 3 2 1)" << endl;\n    return 0;\n}`,
      python: `from typing import Optional\n\nclass ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\nclass Solution:\n    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:\n        prev, curr = None, head\n        while curr:\n            nxt = curr.next\n            curr.next = prev\n            prev = curr\n            curr = nxt\n        return prev\n\nif __name__ == "__main__":\n    head = ListNode(1, ListNode(2, ListNode(3)))\n    sol = Solution()\n    rev = sol.reverseList(head)\n    print("Reversed List: ", end="")\n    while rev:\n        print(rev.val, end=" ")\n        rev = rev.next\n    print("(Expected: 3 2 1)")`
    },
    complexity: { time: "O(n)", space: "O(1)" },
    explanation: "To reverse a linked list, we maintain three pointers: `prev` (initialized to null), `curr` (initialized to head), and a temporary `nextTemp` to store the next node. While moving through the list, we point the current node's next field backwards (`curr->next = prev`). Then, move the `prev` and `curr` pointers forward."
  },
  {
    id: 23,
    name: "Merge Two Sorted Lists",
    category: "Linked List",
    difficulty: "Easy",
    leetCodeUrl: "https://leetcode.com/problems/merge-two-sorted-lists/",
    description: "You are given the heads of two sorted linked lists `list1` and `list2`.\n\nMerge the two lists in a one **sorted** list. The list should be made by splicing together the nodes of the first two lists.\n\nReturn *the head of the merged linked list*.",
    examples: [
      { input: "list1 = [1,2,4], list2 = [1,3,4]", output: "[1,1,2,3,4,4]" }
    ],
    constraints: ["The number of nodes in both lists is in the range `[0, 50]`.", "`-100 <= Node.val <= 100`", "Both `list1` and `list2` are sorted in non-decreasing order."],
    starterCode: {
      cpp: `#include <iostream>\n\nusing namespace std;\n\nstruct ListNode {\n    int val;\n    ListNode *next;\n    ListNode(int x) : val(x), next(nullptr) {}\n};\n\nclass Solution {\npublic:\n    ListNode* mergeTwoLists(ListNode* list1, ListNode* list2) {\n        // Write code here\n        return nullptr;\n    }\n};\n\nint main() {\n    ListNode* l1 = new ListNode(1);\n    ListNode* l2 = new ListNode(2);\n    Solution sol;\n    ListNode* res = sol.mergeTwoLists(l1, l2);\n    cout << res->val << endl;\n    return 0;\n}`,
      python: `from typing import Optional\n\nclass ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\nclass Solution:\n    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:\n        # Write code here\n        return None\n\nif __name__ == "__main__":\n    l1 = ListNode(1)\n    l2 = ListNode(2)\n    sol = Solution()\n    res = sol.mergeTwoLists(l1, l2)\n    print(res.val)`
    },
    solutions: {
      cpp: `#include <iostream>\n\nusing namespace std;\n\nstruct ListNode {\n    int val;\n    ListNode *next;\n    ListNode(int x) : val(x), next(nullptr) {}\n};\n\nclass Solution {\npublic:\n    ListNode* mergeTwoLists(ListNode* list1, ListNode* list2) {\n        ListNode dummy(0);\n        ListNode* tail = &dummy;\n        \n        while (list1 && list2) {\n            if (list1->val <= list2->val) {\n                tail->next = list1;\n                list1 = list1->next;\n            } else {\n                tail->next = list2;\n                list2 = list2->next;\n            }\n            tail = tail->next;\n        }\n        \n        tail->next = list1 ? list1 : list2;\n        return dummy.next;\n    }\n};\n\nint main() {\n    ListNode* l1 = new ListNode(1);\n    l1->next = new ListNode(2);\n    l1->next->next = new ListNode(4);\n    \n    ListNode* l2 = new ListNode(1);\n    l2->next = new ListNode(3);\n    l2->next->next = new ListNode(4);\n    \n    Solution sol;\n    ListNode* res = sol.mergeTwoLists(l1, l2);\n    cout << "Merged: ";\n    while (res) {\n        cout << res->val << " ";\n        res = res->next;\n    }\n    cout << " (Expected: 1 1 2 3 4 4)" << endl;\n    return 0;\n}`,
      python: `from typing import Optional\n\nclass ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\nclass Solution:\n    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:\n        dummy = ListNode()\n        tail = dummy\n        \n        while list1 and list2:\n            if list1.val < list2.val:\n                tail.next = list1\n                list1 = list1.next\n            else:\n                tail.next = list2\n                list2 = list2.next\n            tail = tail.next\n            \n        if list1:\n            tail.next = list1\n        elif list2:\n            tail.next = list2\n            \n        return dummy.next\n\nif __name__ == "__main__":\n    l1 = ListNode(1, ListNode(2, ListNode(4)))\n    l2 = ListNode(1, ListNode(3, ListNode(4)))\n    sol = Solution()\n    res = sol.mergeTwoLists(l1, l2)\n    print("Merged: ", end="")\n    while res:\n        print(res.val, end=" ")\n        res = res.next\n    print("(Expected: 1 1 2 3 4 4)")`
    },
    complexity: { time: "O(n + m)", space: "O(1)" },
    explanation: "We utilize a dummy node as the placeholder head of our merged list, with a helper pointer `tail` to track the last inserted element. We compare the values at `list1` and `list2`, appending the smaller one to `tail` and stepping its pointer forward. At the end, we append any remaining nodes."
  },
  {
    id: 24,
    name: "Reorder List",
    category: "Linked List",
    difficulty: "Medium",
    leetCodeUrl: "https://leetcode.com/problems/reorder-list/",
    description: "You are given the head of a singly linked-list. The list can be represented as:\n`L0 → L1 → … → Ln - 1 → Ln`\n\n*Reorder the list to be on the following form:*\n`L0 → Ln → L1 → Ln - 1 → L2 → Ln - 2 → …`\n\nYou may not modify the values in the list's nodes. Only nodes themselves may be changed.",
    examples: [
      { input: "head = [1,2,3,4]", output: "[1,4,2,3]" }
    ],
    constraints: ["The number of nodes in the list is in the range `[1, 5 * 10^4]`.", "`1 <= Node.val <= 1000`"],
    starterCode: {
      cpp: `#include <iostream>\n\nusing namespace std;\n\nstruct ListNode {\n    int val;\n    ListNode *next;\n    ListNode(int x) : val(x), next(nullptr) {}\n};\n\nclass Solution {\npublic:\n    void reorderList(ListNode* head) {\n        // Write code here\n    }\n};\n\nint main() {\n    ListNode* head = new ListNode(1);\n    head->next = new ListNode(2);\n    Solution sol;\n    sol.reorderList(head);\n    return 0;\n}`,
      python: `from typing import Optional\n\nclass ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\nclass Solution:\n    def reorderList(self, head: Optional[ListNode]) -> None:\n        # Write code here\n        pass\n\nif __name__ == "__main__":\n    head = ListNode(1, ListNode(2))\n    sol = Solution()\n    sol.reorderList(head)`
    },
    solutions: {
      cpp: `#include <iostream>\n\nusing namespace std;\n\nstruct ListNode {\n    int val;\n    ListNode *next;\n    ListNode(int x) : val(x), next(nullptr) {}\n};\n\nclass Solution {\npublic:\n    void reorderList(ListNode* head) {\n        if (!head || !head->next) return;\n        \n        ListNode* slow = head;\n        ListNode* fast = head->next;\n        while (fast && fast->next) {\n            slow = slow->next;\n            fast = fast->next->next;\n        }\n        \n        ListNode* second = slow->next;\n        slow->next = nullptr;\n        ListNode* prev = nullptr;\n        while (second) {\n            ListNode* temp = second->next;\n            second->next = prev;\n            prev = second;\n            second = temp;\n        }\n        \n        ListNode* first = head;\n        second = prev;\n        while (second) {\n            ListNode* temp1 = first->next;\n            ListNode* temp2 = second->next;\n            \n            first->next = second;\n            second->next = temp1;\n            \n            first = temp1;\n            second = temp2;\n        }\n    }\n};\n\nint main() {\n    ListNode* head = new ListNode(1);\n    head->next = new ListNode(2);\n    head->next->next = new ListNode(3);\n    head->next->next->next = new ListNode(4);\n    \n    Solution sol;\n    sol.reorderList(head);\n    cout << "Reordered: ";\n    while (head) {\n        cout << head->val << " ";\n        head = head->next;\n    }\n    cout << " (Expected: 1 4 2 3)" << endl;\n    return 0;\n}`,
      python: `from typing import Optional\n\nclass ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\nclass Solution:\n    def reorderList(self, head: Optional[ListNode]) -> None:\n        if not head: return\n        \n        slow, fast = head, head.next\n        while fast and fast.next:\n            slow = slow.next\n            fast = fast.next.next\n            \n        second = slow.next\n        prev = slow.next = None\n        while second:\n            tmp = second.next\n            second.next = prev\n            prev = second\n            second = tmp\n            \n        first, second = head, prev\n        while second:\n            tmp1, tmp2 = first.next, second.next\n            first.next = second\n            second.next = tmp1\n            first, second = tmp1, tmp2\n\nif __name__ == "__main__":\n    head = ListNode(1, ListNode(2, ListNode(3, ListNode(4))))\n    sol = Solution()\n    sol.reorderList(head)\n    print("Reordered: ", end="")\n    curr = head\n    while curr:\n        print(curr.val, end=" ")\n        curr = curr.next\n    print("(Expected: 1 4 2 3)")`
    },
    complexity: { time: "O(n)", space: "O(1)" },
    explanation: "This problem can be decomposed into 3 sub-problems:\n1. Find the midpoint of the linked list using slow and fast pointers ($O(n)$).\n2. Split the list and reverse the second half ($O(n)$).\n3. Merge the first half and the reversed second half in alternating order ($O(n)$)."
  },
  {
    id: 25,
    name: "Remove Nth Node From End of List",
    category: "Linked List",
    difficulty: "Medium",
    leetCodeUrl: "https://leetcode.com/problems/remove-nth-node-from-end-of-list/",
    description: "Given the `head` of a linked list, remove the `n`-th node from the end of the list and return its head.",
    examples: [
      { input: "head = [1,2,3,4,5], n = 2", output: "[1,2,3,5]" }
    ],
    constraints: ["The number of nodes in the list is `sz`.", "`1 <= sz <= 30`", "`0 <= Node.val <= 100`", "`1 <= n <= sz`"],
    starterCode: {
      cpp: `#include <iostream>\n\nusing namespace std;\n\nstruct ListNode {\n    int val;\n    ListNode *next;\n    ListNode(int x) : val(x), next(nullptr) {}\n};\n\nclass Solution {\npublic:\n    ListNode* removeNthFromEnd(ListNode* head, int n) {\n        // Write code here\n        return head;\n    }\n};\n\nint main() {\n    ListNode* head = new ListNode(1);\n    head->next = new ListNode(2);\n    Solution sol;\n    ListNode* res = sol.removeNthFromEnd(head, 1);\n    cout << res->val << endl;\n    return 0;\n}`,
      python: `from typing import Optional\n\nclass ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\nclass Solution:\n    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:\n        # Write code here\n        return head\n\nif __name__ == "__main__":\n    head = ListNode(1, ListNode(2))\n    sol = Solution()\n    res = sol.removeNthFromEnd(head, 1)\n    print(res.val)`
    },
    solutions: {
      cpp: `#include <iostream>\n\nusing namespace std;\n\nstruct ListNode {\n    int val;\n    ListNode *next;\n    ListNode(int x) : val(x), next(nullptr) {}\n};\n\nclass Solution {\npublic:\n    ListNode* removeNthFromEnd(ListNode* head, int n) {\n        ListNode dummy(0, head);\n        ListNode* left = &dummy;\n        ListNode* right = head;\n        \n        while (n > 0 && right) {\n            right = right->next;\n            n--;\n        }\n        \n        while (right) {\n            left = left->next;\n            right = right->next;\n        }\n        \n        ListNode* to_delete = left->next;\n        left->next = left->next->next;\n        delete to_delete;\n        \n        return dummy.next;\n    }\n};\n\nint main() {\n    ListNode* head = new ListNode(1);\n    head->next = new ListNode(2);\n    head->next->next = new ListNode(3);\n    head->next->next->next = new ListNode(4);\n    head->next->next->next->next = new ListNode(5);\n    \n    Solution sol;\n    ListNode* res = sol.removeNthFromEnd(head, 2);\n    cout << "Removed 2nd from end: ";\n    while (res) {\n        cout << res->val << " ";\n        res = res->next;\n    }\n    cout << " (Expected: 1 2 3 5)" << endl;\n    return 0;\n}`,
      python: `from typing import Optional\n\nclass ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\nclass Solution:\n    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:\n        dummy = ListNode(0, head)\n        left = dummy\n        right = head\n        \n        while n > 0 and right:\n            right = right.next\n            n -= 1\n            \n        while right:\n            left = left.next\n            right = right.next\n            \n        left.next = left.next.next\n        return dummy.next\n\nif __name__ == "__main__":\n    head = ListNode(1, ListNode(2, ListNode(3, ListNode(4, ListNode(5)))))\n    sol = Solution()\n    res = sol.removeNthFromEnd(head, 2)\n    print("Removed 2nd from end: ", end="")\n    while res:\n        print(res.val, end=" ")\n        res = res.next\n    print("(Expected: 1 2 3 5)")`
    },
    complexity: { time: "O(n)", space: "O(1)" },
    explanation: "We utilize two pointers: `left` and `right`. First, we advance the `right` pointer by `n` steps. Then, we place a `left` pointer at a dummy node preceeding `head`, and step both `left` and `right` forward in unison. When `right` hits `nullptr`, `left` will sit exactly before the target node, allowing an easy deletion."
  },
  {
    id: 26,
    name: "Linked List Cycle",
    category: "Linked List",
    difficulty: "Easy",
    leetCodeUrl: "https://leetcode.com/problems/linked-list-cycle/",
    description: "Given `head`, the head of a linked list, determine if the linked list has a cycle in it.\n\nThere is a cycle in a linked list if there is some node in the list that can be reached again by continuously following the `next` pointer.\n\nReturn `true` *if there is a cycle in the linked list*. Otherwise, return `false`.",
    examples: [
      { input: "head = [3,2,0,-4], pos = 1", output: "true" }
    ],
    constraints: ["The number of nodes in the list is in the range `[0, 10^4]`.", "`-10^5 <= Node.val <= 10^5`"],
    starterCode: {
      cpp: `#include <iostream>\n\nusing namespace std;\n\nstruct ListNode {\n    int val;\n    ListNode *next;\n    ListNode(int x) : val(x), next(nullptr) {}\n};\n\nclass Solution {\npublic:\n    bool hasCycle(ListNode *head) {\n        // Write code here\n        return false;\n    }\n};\n\nint main() {\n    ListNode* head = new ListNode(1);\n    Solution sol;\n    cout << (sol.hasCycle(head) ? "True" : "False") << endl;\n    return 0;\n}`,
      python: `from typing import Optional\n\nclass ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\nclass Solution:\n    def hasCycle(self, head: Optional[ListNode]) -> bool:\n        # Write code here\n        return False\n\nif __name__ == "__main__":\n    head = ListNode(1)\n    sol = Solution()\n    print(sol.hasCycle(head))`
    },
    solutions: {
      cpp: `#include <iostream>\n\nusing namespace std;\n\nstruct ListNode {\n    int val;\n    ListNode *next;\n    ListNode(int x) : val(x), next(nullptr) {}\n};\n\nclass Solution {\npublic:\n    bool hasCycle(ListNode *head) {\n        ListNode *slow = head, *fast = head;\n        while (fast && fast->next) {\n            slow = slow->next;\n            fast = fast->next->next;\n            if (slow == fast) return true;\n        }\n        return false;\n    }\n};\n\nint main() {\n    ListNode* head = new ListNode(3);\n    head->next = new ListNode(2);\n    head->next->next = new ListNode(0);\n    head->next->next->next = new ListNode(-4);\n    // Construct cycle: link -4 to index 1 node (2)\n    head->next->next->next->next = head->next;\n    \n    Solution sol;\n    cout << "Has Cycle: " << (sol.hasCycle(head) ? "True" : "False") << " (Expected: True)" << endl;\n    return 0;\n}`,
      python: `from typing import Optional\n\nclass ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\nclass Solution:\n    def hasCycle(self, head: Optional[ListNode]) -> bool:\n        slow, fast = head, head\n        while fast and fast.next:\n            slow = slow.next\n            fast = fast.next.next\n            if slow == fast:\n                return True\n        return False\n\nif __name__ == "__main__":\n    head = ListNode(3)\n    head.next = ListNode(2)\n    head.next.next = ListNode(0)\n    head.next.next.next = ListNode(-4)\n    # Construct cycle\n    head.next.next.next.next = head.next\n    \n    sol = Solution()\n    print(f"Has Cycle: {sol.hasCycle(head)} (Expected: True)")`
    },
    complexity: { time: "O(n)", space: "O(1)" },
    explanation: "This is solved using Floyd's Tortoise and Hare algorithm. We traverse the list with a `slow` pointer moving 1 step at a time and a `fast` pointer moving 2 steps. If a cycle exists, the `fast` pointer will eventually overlap the `slow` pointer. If it hits the end of the list, no cycle exists."
  },
  {
    id: 27,
    name: "LRU Cache",
    category: "Linked List",
    difficulty: "Medium",
    leetCodeUrl: "https://leetcode.com/problems/lru-cache/",
    description: "Design a data structure that follows the constraints of a **Least Recently Used (LRU) cache**.\n\nImplement the `LRUCache` class:\n* `LRUCache(int capacity)` Initialize the LRU cache with positive size `capacity`.\n* `int get(int key)` Return the value of the `key` if the key exists, otherwise return `-1`.\n* `void put(int key, int value)` Update the value of the `key` if the `key` exists. Otherwise, add the `key-value` pair to the cache. If the number of keys exceeds the `capacity` from this operation, **evict** the least recently used key.",
    examples: [
      { input: "[\"LRUCache\",\"put\",\"put\",\"get\",\"put\",\"get\",\"put\",\"get\",\"get\",\"get\"]\\n[[2],[1,1],[2,2],[1],[3,3],[2],[4,4],[1],[3],[4]]", output: "[null,null,null,1,null,-1,null,-1,3,4]" }
    ],
    constraints: ["`1 <= capacity <= 3000`", "`0 <= key <= 10^4`", "`0 <= value <= 10^5`", "At most `2 * 10^5` calls will be made to `get` and `put`."],
    starterCode: {
      cpp: `#include <iostream>\n#include <unordered_map>\n\nusing namespace std;\n\nclass LRUCache {\npublic:\n    LRUCache(int capacity) {\n        \n    }\n    \n    int get(int key) {\n        return -1;\n    }\n    \n    void put(int key, int value) {\n        \n    }\n};\n\nint main() {\n    LRUCache cache(2);\n    cache.put(1, 1);\n    cout << cache.get(1) << endl;\n    return 0;\n}`,
      python: `class LRUCache:\n    def __init__(self, capacity: int):\n        pass\n        \n    def get(self, key: int) -> int:\n        return -1\n        \n    def put(self, key: int, value: int) -> None:\n        pass\n\nif __name__ == "__main__":\n    cache = LRUCache(2)\n    cache.put(1, 1)\n    print(cache.get(1))`
    },
    solutions: {
      cpp: `#include <iostream>\n#include <unordered_map>\n\nusing namespace std;\n\nclass LRUCache {\nprivate:\n    struct Node {\n        int key, val;\n        Node* prev;\n        Node* next;\n        Node(int k, int v) : key(k), val(v), prev(nullptr), next(nullptr) {}\n    };\n    \n    int cap;\n    unordered_map<int, Node*> cache;\n    Node* head;\n    Node* tail;\n    \n    void remove(Node* node) {\n        node->prev->next = node->next;\n        node->next->prev = node->prev;\n    }\n    \n    void insert(Node* node) {\n        Node* nextTemp = head->next;\n        head->next = node;\n        node->prev = head;\n        node->next = nextTemp;\n        nextTemp->prev = node;\n    }\npublic:\n    LRUCache(int capacity) {\n        cap = capacity;\n        head = new Node(0, 0);\n        tail = new Node(0, 0);\n        head->next = tail;\n        tail->prev = head;\n    }\n    \n    int get(int key) {\n        if (cache.count(key)) {\n            Node* node = cache[key];\n            remove(node);\n            insert(node);\n            return node->val;\n        }\n        return -1;\n    }\n    \n    void put(int key, int value) {\n        if (cache.count(key)) {\n            Node* node = cache[key];\n            node->val = value;\n            remove(node);\n            insert(node);\n        } else {\n            if (cache.size() >= cap) {\n                Node* lru = tail->prev;\n                remove(lru);\n                cache.erase(lru->key);\n                delete lru;\n            }\n            Node* node = new Node(key, value);\n            cache[key] = node;\n            insert(node);\n        }\n    }\n};\n\nint main() {\n    LRUCache cache(2);\n    cache.put(1, 1);\n    cache.put(2, 2);\n    cout << "Get 1: " << cache.get(1) << " (Expected: 1)" << endl;\n    cache.put(3, 3); // evicts key 2\n    cout << "Get 2: " << cache.get(2) << " (Expected: -1)" << endl;\n    return 0;\n}`,
      python: `class Node:\n    def __init__(self, key, val):\n        self.key, self.val = key, val\n        self.prev = self.next = None\n\nclass LRUCache:\n    def __init__(self, capacity: int):\n        self.cap = capacity\n        self.cache = {} # map key to node\n        self.left, self.right = Node(0, 0), Node(0, 0)\n        self.left.next, self.right.prev = self.right, self.left\n        \n    def remove(self, node):\n        prev, nxt = node.prev, node.next\n        prev.next, nxt.prev = nxt, prev\n        \n    def insert(self, node):\n        prev, nxt = self.right.prev, self.right\n        prev.next = nxt.prev = node\n        node.next, node.prev = nxt, prev\n        \n    def get(self, key: int) -> int:\n        if key in self.cache:\n            self.remove(self.cache[key])\n            self.insert(self.cache[key])\n            return self.cache[key].val\n        return -1\n        \n    def put(self, key: int, value: int) -> None:\n        if key in self.cache:\n            self.remove(self.cache[key])\n        self.cache[key] = Node(key, value)\n        self.insert(self.cache[key])\n        \n        if len(self.cache) > self.cap:\n            lru = self.left.next\n            self.remove(lru)\n            del self.cache[lru.key]\n\nif __name__ == "__main__":\n    cache = LRUCache(2)\n    cache.put(1, 1)\n    cache.put(2, 2)\n    print(f"Get 1: {cache.get(1)} (Expected: 1)")\n    cache.put(3, 3) # evicts key 2\n    print(f"Get 2: {cache.get(2)} (Expected: -1)")`
    },
    complexity: { time: "O(1) for both get and put", space: "O(capacity)" },
    explanation: "To execute cache searches and updates in constant time, we combine a Hash Map and a Doubly Linked List. The hash map maps cache keys to node pointers, guaranteeing $O(1)$ lookups. The doubly linked list preserves the usage history order: the most recently used item is placed at the head, and the least recently used item rests at the tail."
  },

  // ==================== TREES ====================
  {
    id: 28,
    name: "Invert Binary Tree",
    category: "Trees",
    difficulty: "Easy",
    leetCodeUrl: "https://leetcode.com/problems/invert-binary-tree/",
    description: "Given the `root` of a binary tree, invert the tree, and return *its root*.",
    examples: [
      { input: "root = [4,2,7,1,3,6,9]", output: "[4,7,2,9,6,3,1]" }
    ],
    constraints: ["The number of nodes in the tree is in the range `[0, 100]`.", "`-100 <= Node.val <= 100`"],
    starterCode: {
      cpp: `#include <iostream>\n\nusing namespace std;\n\nstruct TreeNode {\n    int val;\n    TreeNode *left;\n    TreeNode *right;\n    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}\n};\n\nclass Solution {\npublic:\n    TreeNode* invertTree(TreeNode* root) {\n        // Write code here\n        return root;\n    }\n};\n\nint main() {\n    TreeNode* root = new TreeNode(4);\n    root->left = new TreeNode(2);\n    root->right = new TreeNode(7);\n    Solution sol;\n    sol.invertTree(root);\n    return 0;\n}`,
      python: `from typing import Optional\n\nclass TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\nclass Solution:\n    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:\n        # Write code here\n        return root\n\nif __name__ == "__main__":\n    root = TreeNode(4, TreeNode(2), TreeNode(7))\n    sol = Solution()\n    sol.invertTree(root)`
    },
    solutions: {
      cpp: `#include <iostream>\n\nusing namespace std;\n\nstruct TreeNode {\n    int val;\n    TreeNode *left;\n    TreeNode *right;\n    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}\n};\n\nclass Solution {\npublic:\n    TreeNode* invertTree(TreeNode* root) {\n        if (!root) return nullptr;\n        TreeNode* temp = root->left;\n        root->left = invertTree(root->right);\n        root->right = invertTree(temp);\n        return root;\n    }\n};\n\nvoid printTree(TreeNode* node) {\n    if (!node) return;\n    cout << node->val << " ";\n    printTree(node->left);\n    printTree(node->right);\n}\n\nint main() {\n    TreeNode* root = new TreeNode(4);\n    root->left = new TreeNode(2);\n    root->right = new TreeNode(7);\n    \n    Solution sol;\n    TreeNode* inverted = sol.invertTree(root);\n    cout << "Inverted Pre-order: ";\n    printTree(inverted);\n    cout << " (Expected: 4 7 2)" << endl;\n    return 0;\n}`,
      python: `from typing import Optional\n\nclass TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\nclass Solution:\n    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:\n        if not root:\n            return None\n        tmp = root.left\n        root.left = self.invertTree(root.right)\n        root.right = self.invertTree(tmp)\n        return root\n\ndef printTree(node):\n    if not node: return\n    print(node.val, end=" ")\n    printTree(node.left)\n    printTree(node.right)\n\nif __name__ == "__main__":\n    root = TreeNode(4, TreeNode(2), TreeNode(7))\n    sol = Solution()\n    inverted = sol.invertTree(root)\n    print("Inverted Pre-order: ", end="")\n    printTree(inverted)\n    print("(Expected: 4 7 2)")`
    },
    complexity: { time: "O(n)", space: "O(h) where h is height" },
    explanation: "This is solved recursively (DFS). For each node, we swap its left and right child pointers, and recursively invoke our inversion function on the newly swapped left and right subtrees. The base case is a null root, which just returns null."
  },
  {
    id: 29,
    name: "Maximum Depth of Binary Tree",
    category: "Trees",
    difficulty: "Easy",
    leetCodeUrl: "https://leetcode.com/problems/maximum-depth-of-binary-tree/",
    description: "Given the `root` of a binary tree, return *its maximum depth*.\n\nA binary tree's **maximum depth** is the number of nodes along the longest path from the root node down to the farthest leaf node.",
    examples: [
      { input: "root = [3,9,20,null,null,15,7]", output: "3" }
    ],
    constraints: ["The number of nodes in the tree is in the range `[0, 10^4]`.", "`-100 <= Node.val <= 100`"],
    starterCode: {
      cpp: `#include <iostream>\n#include <algorithm>\n\nusing namespace std;\n\nstruct TreeNode {\n    int val;\n    TreeNode *left;\n    TreeNode *right;\n    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}\n};\n\nclass Solution {\npublic:\n    int maxDepth(TreeNode* root) {\n        // Write code here\n        return 0;\n    }\n};\n\nint main() {\n    TreeNode* root = new TreeNode(3);\n    Solution sol;\n    cout << sol.maxDepth(root) << endl;\n    return 0;\n}`,
      python: `from typing import Optional\n\nclass TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\nclass Solution:\n    def maxDepth(self, root: Optional[TreeNode]) -> int:\n        # Write code here\n        return 0\n\nif __name__ == "__main__":\n    root = TreeNode(3)\n    sol = Solution()\n    print(sol.maxDepth(root))`
    },
    solutions: {
      cpp: `#include <iostream>\n#include <algorithm>\n\nusing namespace std;\n\nstruct TreeNode {\n    int val;\n    TreeNode *left;\n    TreeNode *right;\n    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}\n};\n\nclass Solution {\npublic:\n    int maxDepth(TreeNode* root) {\n        if (!root) return 0;\n        return 1 + max(maxDepth(root->left), maxDepth(root->right));\n    }\n};\n\nint main() {\n    TreeNode* root = new TreeNode(3);\n    root->left = new TreeNode(9);\n    root->right = new TreeNode(20);\n    root->right->left = new TreeNode(15);\n    root->right->right = new TreeNode(7);\n    \n    Solution sol;\n    cout << "Max depth: " << sol.maxDepth(root) << " (Expected: 3)" << endl;\n    return 0;\n}`,
      python: `from typing import Optional\n\nclass TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\nclass Solution:\n    def maxDepth(self, root: Optional[TreeNode]) -> int:\n        if not root:\n            return 0\n        return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))\n\nif __name__ == "__main__":\n    root = TreeNode(3, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))\n    sol = Solution()\n    print(f"Max depth: {sol.maxDepth(root)} (Expected: 3)")`
    },
    complexity: { time: "O(n)", space: "O(h)" },
    explanation: "The depth of a binary tree is calculated recursively. If the node is null, its depth is `0`. Otherwise, the depth is equal to `1` (counting the current node) plus the maximum depth between its left subtree and its right subtree."
  },
  {
    id: 30,
    name: "Diameter of Binary Tree",
    category: "Trees",
    difficulty: "Easy",
    leetCodeUrl: "https://leetcode.com/problems/diameter-of-binary-tree/",
    description: "Given the `root` of a binary tree, return *the length of the **diameter** of the tree*.\n\nThe **diameter** of a binary tree is the **length of the longest path** between any two nodes in a tree. This path may or may not pass through the `root`.\n\nThe length of a path between two nodes is represented by the number of edges between them.",
    examples: [
      { input: "root = [1,2,3,4,5]", output: "3", explanation: "3 is the length of the path [4,2,1,3] or [5,2,1,3]." }
    ],
    constraints: ["The number of nodes in the tree is in the range `[1, 10^4]`.", "`-100 <= Node.val <= 100`"],
    starterCode: {
      cpp: `#include <iostream>\n#include <algorithm>\n\nusing namespace std;\n\nstruct TreeNode {\n    int val;\n    TreeNode *left;\n    TreeNode *right;\n    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}\n};\n\nclass Solution {\npublic:\n    int diameterOfBinaryTree(TreeNode* root) {\n        // Write code here\n        return 0;\n    }\n};\n\nint main() {\n    TreeNode* root = new TreeNode(1);\n    Solution sol;\n    cout << sol.diameterOfBinaryTree(root) << endl;\n    return 0;\n}`,
      python: `from typing import Optional\n\nclass TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\nclass Solution:\n    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:\n        # Write code here\n        return 0\n\nif __name__ == "__main__":\n    root = TreeNode(1)\n    sol = Solution()\n    print(sol.diameterOfBinaryTree(root))`
    },
    solutions: {
      cpp: `#include <iostream>\n#include <algorithm>\n\nusing namespace std;\n\nstruct TreeNode {\n    int val;\n    TreeNode *left;\n    TreeNode *right;\n    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}\n};\n\nclass Solution {\nprivate:\n    int max_diameter = 0;\n    int height(TreeNode* node) {\n        if (!node) return 0;\n        int lh = height(node->left);\n        int rh = height(node->right);\n        max_diameter = max(max_diameter, lh + rh);\n        return 1 + max(lh, rh);\n    }\npublic:\n    int diameterOfBinaryTree(TreeNode* root) {\n        height(root);\n        return max_diameter;\n    }\n};\n\nint main() {\n    TreeNode* root = new TreeNode(1);\n    root->left = new TreeNode(2);\n    root->right = new TreeNode(3);\n    root->left->left = new TreeNode(4);\n    root->left->right = new TreeNode(5);\n    \n    Solution sol;\n    cout << "Diameter: " << sol.diameterOfBinaryTree(root) << " (Expected: 3)" << endl;\n    return 0;\n}`,
      python: `from typing import Optional\n\nclass TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\nclass Solution:\n    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:\n        res = [0]\n        \n        def dfs(root):\n            if not root:\n                return -1\n            left = dfs(root.left)\n            right = dfs(root.right)\n            res[0] = max(res[0], 2 + left + right)\n            return 1 + max(left, right)\n            \n        dfs(root)\n        return res[0]\n\nif __name__ == "__main__":\n    root = TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)), TreeNode(3))\n    sol = Solution()\n    print(f"Diameter: {sol.diameterOfBinaryTree(root)} (Expected: 3)")`
    },
    complexity: { time: "O(n)", space: "O(h)" },
    explanation: "At any node, the longest path that passes through it as the inflection point is `height(left_child) + height(right_child)`. We use a recursive function to compute tree height. During the depth traversal, we calculate this potential diameter for every node, and update a global maximum."
  },
  {
    id: 31,
    name: "Balanced Binary Tree",
    category: "Trees",
    difficulty: "Easy",
    leetCodeUrl: "https://leetcode.com/problems/balanced-binary-tree/",
    description: "Given a binary tree, determine if it is **height-balanced**.\n\nA **height-balanced** binary tree is a binary tree in which the depth of the two subtrees of every node never differs by more than one.",
    examples: [
      { input: "root = [3,9,20,null,null,15,7]", output: "true" }
    ],
    constraints: ["The number of nodes in the tree is in the range `[0, 5000]`.", "`-10^4 <= Node.val <= 10^4`"],
    starterCode: {
      cpp: `#include <iostream>\n#include <algorithm>\n\nusing namespace std;\n\nstruct TreeNode {\n    int val;\n    TreeNode *left;\n    TreeNode *right;\n    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}\n};\n\nclass Solution {\npublic:\n    bool isBalanced(TreeNode* root) {\n        // Write code here\n        return false;\n    }\n};\n\nint main() {\n    TreeNode* root = new TreeNode(3);\n    Solution sol;\n    cout << (sol.isBalanced(root) ? "True" : "False") << endl;\n    return 0;\n}`,
      python: `from typing import Optional\n\nclass TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\nclass Solution:\n    def isBalanced(self, root: Optional[TreeNode]) -> bool:\n        # Write code here\n        return False\n\nif __name__ == "__main__":\n    root = TreeNode(3)\n    sol = Solution()\n    print(sol.isBalanced(root))`
    },
    solutions: {
      cpp: `#include <iostream>\n#include <algorithm>\n#include <cstdlib>\n\nusing namespace std;\n\nstruct TreeNode {\n    int val;\n    TreeNode *left;\n    TreeNode *right;\n    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}\n};\n\nclass Solution {\nprivate:\n    int checkHeight(TreeNode* node) {\n        if (!node) return 0;\n        int lh = checkHeight(node->left);\n        if (lh == -1) return -1;\n        int rh = checkHeight(node->right);\n        if (rh == -1) return -1;\n        if (abs(lh - rh) > 1) return -1;\n        return 1 + max(lh, rh);\n    }\npublic:\n    bool isBalanced(TreeNode* root) {\n        return checkHeight(root) != -1;\n    }\n};\n\nint main() {\n    TreeNode* root = new TreeNode(3);\n    root->left = new TreeNode(9);\n    root->right = new TreeNode(20);\n    root->right->left = new TreeNode(15);\n    root->right->right = new TreeNode(7);\n    \n    Solution sol;\n    cout << "Is balanced: " << (sol.isBalanced(root) ? "True" : "False") << " (Expected: True)" << endl;\n    return 0;\n}`,
      python: `from typing import Optional\n\nclass TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\nclass Solution:\n    def isBalanced(self, root: Optional[TreeNode]) -> bool:\n        def dfs(root):\n            if not root:\n                return [True, 0]\n            left, right = dfs(root.left), dfs(root.right)\n            balanced = left[0] and right[0] and abs(left[1] - right[1]) <= 1\n            return [balanced, 1 + max(left[1], right[1])]\n            \n        return dfs(root)[0]\n\nif __name__ == "__main__":\n    root = TreeNode(3, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))\n    sol = Solution()\n    print(f"Is balanced: {sol.isBalanced(root)} (Expected: True)")`
    },
    complexity: { time: "O(n)", space: "O(h)" },
    explanation: "We write a recursive function that returns the height of the subtree if it is balanced, or `-1` if it is unbalanced. For each node, we check if the left or right subtree is unbalanced. If they are balanced, we verify if the height difference exceeds `1`. If it does, we return `-1` to propagate the unbalance upward."
  },
  {
    id: 32,
    name: "Same Tree",
    category: "Trees",
    difficulty: "Easy",
    leetCodeUrl: "https://leetcode.com/problems/same-tree/",
    description: "Given the roots of two binary trees `p` and `q`, write a function to check if they are the same or not.\n\nTwo binary trees are considered the same if they are structurally identical, and the nodes have the same value.",
    examples: [
      { input: "p = [1,2,3], q = [1,2,3]", output: "true" }
    ],
    constraints: ["The number of nodes in both trees is in the range `[0, 100]`.", "`-10^4 <= Node.val <= 10^4`"],
    starterCode: {
      cpp: `#include <iostream>\n\nusing namespace std;\n\nstruct TreeNode {\n    int val;\n    TreeNode *left;\n    TreeNode *right;\n    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}\n};\n\nclass Solution {\npublic:\n    bool isSameTree(TreeNode* p, TreeNode* q) {\n        // Write code here\n        return false;\n    }\n};\n\nint main() {\n    TreeNode* p = new TreeNode(1);\n    TreeNode* q = new TreeNode(1);\n    Solution sol;\n    cout << (sol.isSameTree(p, q) ? "True" : "False") << endl;\n    return 0;\n}`,
      python: `from typing import Optional\n\nclass TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\nclass Solution:\n    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:\n        # Write code here\n        return False\n\nif __name__ == "__main__":\n    p = TreeNode(1)\n    q = TreeNode(1)\n    sol = Solution()\n    print(sol.isSameTree(p, q))`
    },
    solutions: {
      cpp: `#include <iostream>\n\nusing namespace std;\n\nstruct TreeNode {\n    int val;\n    TreeNode *left;\n    TreeNode *right;\n    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}\n};\n\nclass Solution {\npublic:\n    bool isSameTree(TreeNode* p, TreeNode* q) {\n        if (!p && !q) return true;\n        if (!p || !q) return false;\n        if (p->val != q->val) return false;\n        return isSameTree(p->left, q->left) && isSameTree(p->right, q->right);\n    }\n};\n\nint main() {\n    TreeNode* p = new TreeNode(1);\n    p->left = new TreeNode(2);\n    p->right = new TreeNode(3);\n    \n    TreeNode* q = new TreeNode(1);\n    q->left = new TreeNode(2);\n    q->right = new TreeNode(3);\n    \n    Solution sol;\n    cout << "Same tree: " << (sol.isSameTree(p, q) ? "True" : "False") << " (Expected: True)" << endl;\n    return 0;\n}`,
      python: `from typing import Optional\n\nclass TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\nclass Solution:\n    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:\n        if not p and not q:\n            return True\n        if not p or not q:\n            return False\n        if p.val != q.val:\n            return False\n        return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)\n\nif __name__ == "__main__":\n    p = TreeNode(1, TreeNode(2), TreeNode(3))\n    q = TreeNode(1, TreeNode(2), TreeNode(3))\n    sol = Solution()\n    print(f"Same Tree: {sol.isSameTree(p, q)} (Expected: True)")`
    },
    complexity: { time: "O(min(n, m))", space: "O(min(hp, hq))" },
    explanation: "Two trees are identical if and only if: 1. Both roots are null (base case), 2. Both roots are non-null and match in value, 3. The left subtrees are structurally identical, 4. The right subtrees are structurally identical. We verify this recursively."
  },
  {
    id: 33,
    name: "Subtree of Another Tree",
    category: "Trees",
    difficulty: "Easy",
    leetCodeUrl: "https://leetcode.com/problems/subtree-of-another-tree/",
    description: "Given the roots of two binary trees `root` and `subRoot`, return `true` if there is a subtree of `root` with the same structure and node values of `subRoot` and `false` otherwise.\n\nA subtree of a binary tree `tree` is a tree that consists of a node in `tree` and all of this node's descendants. The tree `tree` could also be considered as a subtree of itself.",
    examples: [
      { input: "root = [3,4,5,1,2], subRoot = [4,1,2]", output: "true" }
    ],
    constraints: ["The number of nodes in the `root` tree is up to `2000`.", "The number of nodes in the `subRoot` tree is up to `1000`."],
    starterCode: {
      cpp: `#include <iostream>\n\nusing namespace std;\n\nstruct TreeNode {\n    int val;\n    TreeNode *left;\n    TreeNode *right;\n    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}\n};\n\nclass Solution {\npublic:\n    bool isSubtree(TreeNode* root, TreeNode* subRoot) {\n        // Write code here\n        return false;\n    }\n};\n\nint main() {\n    TreeNode* r = new TreeNode(1);\n    TreeNode* s = new TreeNode(1);\n    Solution sol;\n    cout << (sol.isSubtree(r, s) ? "True" : "False") << endl;\n    return 0;\n}`,
      python: `from typing import Optional\n\nclass TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\nclass Solution:\n    def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:\n        # Write code here\n        return False\n\nif __name__ == "__main__":\n    r = TreeNode(1)\n    s = TreeNode(1)\n    sol = Solution()\n    print(sol.isSubtree(r, s))`
    },
    solutions: {
      cpp: `#include <iostream>\n\nusing namespace std;\n\nstruct TreeNode {\n    int val;\n    TreeNode *left;\n    TreeNode *right;\n    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}\n};\n\nclass Solution {\nprivate:\n    bool isSame(TreeNode* p, TreeNode* q) {\n        if (!p && !q) return true;\n        if (!p || !q) return false;\n        return (p->val == q->val) && isSame(p->left, q->left) && isSame(p->right, q->right);\n    }\npublic:\n    bool isSubtree(TreeNode* root, TreeNode* subRoot) {\n        if (!subRoot) return true;\n        if (!root) return false;\n        if (isSame(root, subRoot)) return true;\n        return isSubtree(root->left, subRoot) || isSubtree(root->right, subRoot);\n    }\n};\n\nint main() {\n    TreeNode* root = new TreeNode(3);\n    root->left = new TreeNode(4);\n    root->right = new TreeNode(5);\n    root->left->left = new TreeNode(1);\n    root->left->right = new TreeNode(2);\n    \n    TreeNode* subRoot = new TreeNode(4);\n    subRoot->left = new TreeNode(1);\n    subRoot->right = new TreeNode(2);\n    \n    Solution sol;\n    cout << "Is subtree: " << (sol.isSubtree(root, subRoot) ? "True" : "False") << " (Expected: True)" << endl;\n    return 0;\n}`,
      python: `from typing import Optional\n\nclass TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\nclass Solution:\n    def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:\n        if not subRoot: return True\n        if not root: return False\n        if self.sameTree(root, subRoot):\n            return True\n        return self.isSubtree(root.left, subRoot) or self.isSubtree(root.right, subRoot)\n        \n    def sameTree(self, p, q):\n        if not p and not q:\n            return True\n        if p and q and p.val == q.val:\n            return self.sameTree(p.left, q.left) and self.sameTree(p.right, q.right)\n        return False\n\nif __name__ == "__main__":\n    root = TreeNode(3, TreeNode(4, TreeNode(1), TreeNode(2)), TreeNode(5))\n    subRoot = TreeNode(4, TreeNode(1), TreeNode(2))\n    sol = Solution()\n    print(f"Is subtree: {sol.isSubtree(root, subRoot)} (Expected: True)")`
    },
    complexity: { time: "O(n * m)", space: "O(h_root)" },
    explanation: "A tree `subRoot` is a subtree of `root` if they are identical, or if `subRoot` is a subtree of `root->left`, or if `subRoot` is a subtree of `root->right`. We reuse our helper `isSameTree` function to verify if the trees are identical at the current node."
  },
  {
    id: 34,
    name: "Lowest Common Ancestor of a Binary Search Tree",
    category: "Trees",
    difficulty: "Medium",
    leetCodeUrl: "https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/",
    description: "Given a binary search tree (BST), find the lowest common ancestor (LCA) node of two given nodes in the BST.\n\nAccording to the definition of LCA on Wikipedia: “The lowest common ancestor is defined between two nodes `p` and `q` as the lowest node in `T` that has both `p` and `q` as descendants (where we allow **a node to be a descendant of itself**).”",
    examples: [
      { input: "root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 8", output: "6" }
    ],
    constraints: ["The number of nodes in the tree is in the range `[2, 10^5]`.", "All `Node.val` are unique.", "`p` and `q` will exist in the BST and `p != q`."],
    starterCode: {
      cpp: `#include <iostream>\n\nusing namespace std;\n\nstruct TreeNode {\n    int val;\n    TreeNode *left;\n    TreeNode *right;\n    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}\n};\n\nclass Solution {\npublic:\n    TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q) {\n        // Write code here\n        return root;\n    }\n};\n\nint main() {\n    TreeNode* root = new TreeNode(6);\n    TreeNode* p = new TreeNode(2);\n    TreeNode* q = new TreeNode(8);\n    root->left = p;\n    root->right = q;\n    Solution sol;\n    cout << sol.lowestCommonAncestor(root, p, q)->val << endl;\n    return 0;\n}`,
      python: `class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\nclass Solution:\n    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':\n        # Write code here\n        return root\n\nif __name__ == "__main__":\n    p = TreeNode(2)\n    q = TreeNode(8)\n    root = TreeNode(6, p, q)\n    sol = Solution()\n    print(sol.lowestCommonAncestor(root, p, q).val)`
    },
    solutions: {
      cpp: `#include <iostream>\n\nusing namespace std;\n\nstruct TreeNode {\n    int val;\n    TreeNode *left;\n    TreeNode *right;\n    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}\n};\n\nclass Solution {\npublic:\n    TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q) {\n        TreeNode* curr = root;\n        while (curr) {\n            if (p->val > curr->val && q->val > curr->val) {\n                curr = curr->right;\n            } else if (p->val < curr->val && q->val < curr->val) {\n                curr = curr->left;\n            } else {\n                return curr;\n            }\n        }\n        return nullptr;\n    }\n};\n\nint main() {\n    TreeNode* root = new TreeNode(6);\n    TreeNode* p = new TreeNode(2);\n    TreeNode* q = new TreeNode(8);\n    root->left = p;\n    root->right = q;\n    root->left->left = new TreeNode(0);\n    root->left->right = new TreeNode(4);\n    \n    Solution sol;\n    cout << "LCA: " << sol.lowestCommonAncestor(root, p, q)->val << " (Expected: 6)" << endl;\n    return 0;\n}`,
      python: `class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\nclass Solution:\n    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':\n        curr = root\n        while curr:\n            if p.val > curr.val and q.val > curr.val:\n                curr = curr.right\n            elif p.val < curr.val and q.val < curr.val:\n                curr = curr.left\n            else:\n                return curr\n\nif __name__ == "__main__":\n    p = TreeNode(2)\n    q = TreeNode(8)\n    root = TreeNode(6, p, q)\n    sol = Solution()\n    print(f"LCA: {sol.lowestCommonAncestor(root, p, q).val} (Expected: 6)")`
    },
    complexity: { time: "O(log n) = O(h)", space: "O(1)" },
    explanation: "Because the tree is a Binary Search Tree (BST), the left node is smaller than the parent, and the right node is larger. We traverse starting at the root: 1. If both `p` and `q` are larger than the current node, the LCA sits in the right subtree. 2. If both are smaller, the LCA sits in the left. 3. If there is a split (one is smaller, one is larger), the current node is the LCA."
  },
  {
    id: 35,
    name: "Binary Tree Level Order Traversal",
    category: "Trees",
    difficulty: "Medium",
    leetCodeUrl: "https://leetcode.com/problems/binary-tree-level-order-traversal/",
    description: "Given the `root` of a binary tree, return *the level order traversal of its nodes' values*. (i.e., from left to right, level by level).",
    examples: [
      { input: "root = [3,9,20,null,null,15,7]", output: "[[3],[9,20],[15,7]]" }
    ],
    constraints: ["The number of nodes in the tree is in the range `[0, 2000]`.", "`-1000 <= Node.val <= 1000`"],
    starterCode: {
      cpp: `#include <iostream>\n#include <vector>\n#include <queue>\n\nusing namespace std;\n\nstruct TreeNode {\n    int val;\n    TreeNode *left;\n    TreeNode *right;\n    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}\n};\n\nclass Solution {\npublic:\n    vector<vector<int>> levelOrder(TreeNode* root) {\n        // Write code here\n        return {};\n    }\n};\n\nint main() {\n    TreeNode* root = new TreeNode(3);\n    Solution sol;\n    vector<vector<int>> res = sol.levelOrder(root);\n    cout << res.size() << endl;\n    return 0;\n}`,
      python: `from typing import List, Optional\nimport collections\n\nclass TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\nclass Solution:\n    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:\n        # Write code here\n        return []\n\nif __name__ == "__main__":\n    root = TreeNode(3)\n    sol = Solution()\n    print(sol.levelOrder(root))`
    },
    solutions: {
      cpp: `#include <iostream>\n#include <vector>\n#include <queue>\n\nusing namespace std;\n\nstruct TreeNode {\n    int val;\n    TreeNode *left;\n    TreeNode *right;\n    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}\n};\n\nclass Solution {\npublic:\n    vector<vector<int>> levelOrder(TreeNode* root) {\n        vector<vector<int>> res;\n        if (!root) return res;\n        queue<TreeNode*> q;\n        q.push(root);\n        while (!q.empty()) {\n            int sz = q.size();\n            vector<int> level;\n            for (int i = 0; i < sz; ++i) {\n                TreeNode* node = q.front();\n                q.pop();\n                level.push_back(node->val);\n                if (node->left) q.push(node->left);\n                if (node->right) q.push(node->right);\n            }\n            res.push_back(level);\n        }\n        return res;\n    }\n};\n\nint main() {\n    TreeNode* root = new TreeNode(3);\n    root->left = new TreeNode(9);\n    root->right = new TreeNode(20);\n    root->right->left = new TreeNode(15);\n    root->right->right = new TreeNode(7);\n    \n    Solution sol;\n    vector<vector<int>> res = sol.levelOrder(root);\n    cout << "Level Order:\\n";\n    for (auto& row : res) {\n        cout << "[ ";\n        for (int x : row) cout << x << " ";\n        cout << "] ";\n    }\n    cout << " (Expected: [3] [9 20] [15 7])" << endl;\n    return 0;\n}`,
      python: `from typing import List, Optional\nimport collections\n\nclass TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\nclass Solution:\n    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:\n        res = []\n        q = collections.deque()\n        if root:\n            q.append(root)\n        while q:\n            val = []\n            for i in range(len(q)):\n                node = q.popleft()\n                val.append(node.val)\n                if node.left:\n                    q.append(node.left)\n                if node.right:\n                    q.append(node.right)\n            res.append(val)\n        return res\n\nif __name__ == "__main__":\n    root = TreeNode(3, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))\n    sol = Solution()\n    print(f"Level Order: {sol.levelOrder(root)} (Expected: [[3], [9, 20], [15, 7]])")`
    },
    complexity: { time: "O(n)", space: "O(n) (widest level size)" },
    explanation: "This is solved using Breadth-First Search (BFS). We use a queue. For each step of our main loop, we record the size of the queue (which represents the exact number of nodes at the current level). We iterate through these nodes, pop them, collect their values, and insert their non-null children back into the queue."
  },
  {
    id: 36,
    name: "Binary Tree Right Side View",
    category: "Trees",
    difficulty: "Medium",
    leetCodeUrl: "https://leetcode.com/problems/binary-tree-right-side-view/",
    description: "Given the `root` of a binary tree, imagine yourself standing on the **right side** of it, return *the values of the nodes you can see ordered from top to bottom*.",
    examples: [
      { input: "root = [1,2,3,null,5,null,4]", output: "[1,3,4]" }
    ],
    constraints: ["The number of nodes in the tree is in the range `[0, 100]`.", "`-100 <= Node.val <= 100`"],
    starterCode: {
      cpp: `#include <iostream>\n#include <vector>\n\nusing namespace std;\n\nstruct TreeNode {\n    int val;\n    TreeNode *left;\n    TreeNode *right;\n    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}\n};\n\nclass Solution {\npublic:\n    vector<int> rightSideView(TreeNode* root) {\n        // Write code here\n        return {};\n    }\n};\n\nint main() {\n    TreeNode* root = new TreeNode(1);\n    Solution sol;\n    vector<int> res = sol.rightSideView(root);\n    cout << res.size() << endl;\n    return 0;\n}`,
      python: `from typing import List, Optional\nimport collections\n\nclass TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\nclass Solution:\n    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:\n        # Write code here\n        return []\n\nif __name__ == "__main__":\n    root = TreeNode(1)\n    sol = Solution()\n    print(sol.rightSideView(root))`
    },
    solutions: {
      cpp: `#include <iostream>\n#include <vector>\n\nusing namespace std;\n\nstruct TreeNode {\n    int val;\n    TreeNode *left;\n    TreeNode *right;\n    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}\n};\n\nclass Solution {\nprivate:\n    void dfs(TreeNode* node, int depth, vector<int>& res) {\n        if (!node) return;\n        if (depth == res.size()) {\n            res.push_back(node->val);\n        }\n        dfs(node->right, depth + 1, res);\n        dfs(node->left, depth + 1, res);\n    }\npublic:\n    vector<int> rightSideView(TreeNode* root) {\n        vector<int> res;\n        dfs(root, 0, res);\n        return res;\n    }\n};\n\nint main() {\n    TreeNode* root = new TreeNode(1);\n    root->left = new TreeNode(2);\n    root->right = new TreeNode(3);\n    root->left->right = new TreeNode(5);\n    root->right->right = new TreeNode(4);\n    \n    Solution sol;\n    vector<int> res = sol.rightSideView(root);\n    cout << "Right side view: ";\n    for (int x : res) cout << x << " ";\n    cout << " (Expected: 1 3 4)" << endl;\n    return 0;\n}`,
      python: `from typing import List, Optional\nimport collections\n\nclass TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\nclass Solution:\n    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:\n        res = []\n        q = collections.deque([root])\n        while q:\n            rightSide = None\n            qLen = len(q)\n            for i in range(qLen):\n                node = q.popleft()\n                if node:\n                    rightSide = node\n                    q.append(node.left)\n                    q.append(node.right)\n            if rightSide:\n                res.append(rightSide.val)\n        return res\n\nif __name__ == "__main__":\n    root = TreeNode(1, TreeNode(2, None, TreeNode(5)), TreeNode(3, None, TreeNode(4)))\n    sol = Solution()\n    print(f"Right Side View: {sol.rightSideView(root)} (Expected: [1, 3, 4])")`
    },
    complexity: { time: "O(n)", space: "O(h)" },
    explanation: "This is efficiently solved using a custom Depth First Search (DFS) where we traverse the **right subtree first**. We pass down a `depth` variable. If the depth is equal to the size of our result list, it implies this is the first node we have seen at this level. We explore the right then left subtrees."
  },
  {
    id: 37,
    name: "Count Good Nodes in Binary Tree",
    category: "Trees",
    difficulty: "Medium",
    leetCodeUrl: "https://leetcode.com/problems/count-good-nodes-in-binary-tree/",
    description: "Given a binary tree `root`, a node *X* in the tree is named **good** if in the path from root to *X* there are no nodes with a value *greater than* X.\n\nReturn the number of **good** nodes in the binary tree.",
    examples: [
      { input: "root = [3,1,4,3,null,1,5]", output: "4", explanation: "Root (3) is always good. Node (4) is good since path 3->4 has max 4. Node (5) is good. Node (3) under (1) is good since max value is 3." }
    ],
    constraints: ["The number of nodes in the binary tree is in the range `[1, 10^5]`.", "`-10^4 <= Node.val <= 10^4`"],
    starterCode: {
      cpp: `#include <iostream>\n#include <algorithm>\n\nusing namespace std;\n\nstruct TreeNode {\n    int val;\n    TreeNode *left;\n    TreeNode *right;\n    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}\n};\n\nclass Solution {\npublic:\n    int goodNodes(TreeNode* root) {\n        // Write code here\n        return 0;\n    }\n};\n\nint main() {\n    TreeNode* root = new TreeNode(3);\n    Solution sol;\n    cout << sol.goodNodes(root) << endl;\n    return 0;\n}`,
      python: `class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\nclass Solution:\n    def goodNodes(self, root: TreeNode) -> int:\n        # Write code here\n        return 0\n\nif __name__ == "__main__":\n    root = TreeNode(3)\n    sol = Solution()\n    print(sol.goodNodes(root))`
    },
    solutions: {
      cpp: `#include <iostream>\n#include <algorithm>\n\nusing namespace std;\n\nstruct TreeNode {\n    int val;\n    TreeNode *left;\n    TreeNode *right;\n    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}\n};\n\nclass Solution {\nprivate:\n    int dfs(TreeNode* node, int max_so_far) {\n        if (!node) return 0;\n        int good = 0;\n        if (node->val >= max_so_far) {\n            good = 1;\n            max_so_far = node->val;\n        }\n        return good + dfs(node->left, max_so_far) + dfs(node->right, max_so_far);\n    }\npublic:\n    int goodNodes(TreeNode* root) {\n        return dfs(root, root->val);\n    }\n};\n\nint main() {\n    TreeNode* root = new TreeNode(3);\n    root->left = new TreeNode(1);\n    root->right = new TreeNode(4);\n    root->left->left = new TreeNode(3);\n    root->right->left = new TreeNode(1);\n    root->right->right = new TreeNode(5);\n    \n    Solution sol;\n    cout << "Good nodes: " << sol.goodNodes(root) << " (Expected: 4)" << endl;\n    return 0;\n}`,
      python: `class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\nclass Solution:\n    def goodNodes(self, root: TreeNode) -> int:\n        def dfs(node, maxVal):\n            if not node:\n                return 0\n            res = 1 if node.val >= maxVal else 0\n            maxVal = max(maxVal, node.val)\n            res += dfs(node.left, maxVal)\n            res += dfs(node.right, maxVal)\n            return res\n            \n        return dfs(root, root.val)\n\nif __name__ == "__main__":\n    root = TreeNode(3, TreeNode(1, TreeNode(3)), TreeNode(4, TreeNode(1), TreeNode(5)))\n    sol = Solution()\n    print(f"Good nodes: {sol.goodNodes(root)} (Expected: 4)")`
    },
    complexity: { time: "O(n)", space: "O(h)" },
    explanation: "We utilize DFS to traverse from root to leaf, maintaining a `max_so_far` value along the current path. At each node, we check if its value is greater than or equal to `max_so_far`. If it is, the node is \"good\" and we increment our count. We then pass `max(max_so_far, node->val)` down to its children."
  },
  {
    id: 38,
    name: "Validate Binary Search Tree",
    category: "Trees",
    difficulty: "Medium",
    leetCodeUrl: "https://leetcode.com/problems/validate-binary-search-tree/",
    description: "Given the `root` of a binary tree, determine if it is a valid binary search tree (BST).\n\nA **valid BST** is defined as follows:\n* The left subtree of a node contains only nodes with keys **less than** the node's key.\n* The right subtree of a node contains only nodes with keys **greater than** the node's key.\n* Both the left and right subtrees must also be binary search trees.",
    examples: [
      { input: "root = [2,1,3]", output: "true" }
    ],
    constraints: ["The number of nodes in the tree is in the range `[1, 10^4]`.", "`-2^31 <= Node.val <= 2^31 - 1`"],
    starterCode: {
      cpp: `#include <iostream>\n#include <climits>\n\nusing namespace std;\n\nstruct TreeNode {\n    int val;\n    TreeNode *left;\n    TreeNode *right;\n    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}\n};\n\nclass Solution {\npublic:\n    bool isValidBST(TreeNode* root) {\n        // Write code here\n        return false;\n    }\n};\n\nint main() {\n    TreeNode* root = new TreeNode(2);\n    Solution sol;\n    cout << (sol.isValidBST(root) ? "True" : "False") << endl;\n    return 0;\n}`,
      python: `from typing import Optional\n\nclass TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\nclass Solution:\n    def isValidBST(self, root: Optional[TreeNode]) -> bool:\n        # Write code here\n        return False\n\nif __name__ == "__main__":\n    root = TreeNode(2)\n    sol = Solution()\n    print(sol.isValidBST(root))`
    },
    solutions: {
      cpp: `#include <iostream>\n#include <climits>\n\nusing namespace std;\n\nstruct TreeNode {\n    int val;\n    TreeNode *left;\n    TreeNode *right;\n    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}\n};\n\nclass Solution {\nprivate:\n    bool validate(TreeNode* node, long long min_val, long long max_val) {\n        if (!node) return true;\n        if (node->val <= min_val || node->val >= max_val) return false;\n        return validate(node->left, min_val, node->val) && \n               validate(node->right, node->val, max_val);\n    }\npublic:\n    bool isValidBST(TreeNode* root) {\n        return validate(root, LLONG_MIN, LLONG_MAX);\n    }\n};\n\nint main() {\n    TreeNode* root = new TreeNode(2);\n    root->left = new TreeNode(1);\n    root->right = new TreeNode(3);\n    \n    Solution sol;\n    cout << "Is Valid BST: " << (sol.isValidBST(root) ? "True" : "False") << " (Expected: True)" << endl;\n    return 0;\n}`,
      python: `from typing import Optional\n\nclass TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\nclass Solution:\n    def isValidBST(self, root: Optional[TreeNode]) -> bool:\n        def valid(node, left, right):\n            if not node:\n                return True\n            if not (left < node.val < right):\n                return False\n            return valid(node.left, left, node.val) and valid(node.right, node.val, right)\n            \n        return valid(root, float("-inf"), float("inf"))\n\nif __name__ == "__main__":\n    root = TreeNode(2, TreeNode(1), TreeNode(3))\n    sol = Solution()\n    print(f"Is Valid BST: {sol.isValidBST(root)} (Expected: True)")`
    },
    complexity: { time: "O(n)", space: "O(h)" },
    explanation: "A BST is valid if the values of all nodes in a node's left subtree are strictly less than the node's value, and all values in its right subtree are strictly greater. We write a helper function `validate(node, min, max)` that passes down these boundaries. For the left child, the upper boundary becomes `node->val`. For the right child, the lower boundary becomes `node->val`."
  },
  {
    id: 39,
    name: "Kth Smallest Element in a BST",
    category: "Trees",
    difficulty: "Medium",
    leetCodeUrl: "https://leetcode.com/problems/kth-smallest-element-in-a-bst/",
    description: "Given the `root` of a binary search tree, and an integer `k`, return *the* `k`-th *smallest value (**1-indexed**) of all the values of the nodes in the tree*.",
    examples: [
      { input: "root = [3,1,4,null,2], k = 1", output: "1" }
    ],
    constraints: ["The number of nodes in the tree is `n`.", "`1 <= k <= n <= 10^4`", "`0 <= Node.val <= 10^4`"],
    starterCode: {
      cpp: `#include <iostream>\n\nusing namespace std;\n\nstruct TreeNode {\n    int val;\n    TreeNode *left;\n    TreeNode *right;\n    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}\n};\n\nclass Solution {\npublic:\n    int kthSmallest(TreeNode* root, int k) {\n        // Write code here\n        return 0;\n    }\n};\n\nint main() {\n    TreeNode* root = new TreeNode(3);\n    Solution sol;\n    cout << sol.kthSmallest(root, 1) << endl;\n    return 0;\n}`,
      python: `from typing import Optional\n\nclass TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\nclass Solution:\n    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:\n        # Write code here\n        return 0\n\nif __name__ == "__main__":\n    root = TreeNode(3)\n    sol = Solution()\n    print(sol.kthSmallest(root, 1))`
    },
    solutions: {
      cpp: `#include <iostream>\n\nusing namespace std;\n\nstruct TreeNode {\n    int val;\n    TreeNode *left;\n    TreeNode *right;\n    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}\n};\n\nclass Solution {\nprivate:\n    int count = 0;\n    int ans = -1;\n    void inorder(TreeNode* node, int k) {\n        if (!node || ans != -1) return;\n        inorder(node->left, k);\n        count++;\n        if (count == k) {\n            ans = node->val;\n            return;\n        }\n        inorder(node->right, k);\n    }\npublic:\n    int kthSmallest(TreeNode* root, int k) {\n        inorder(root, k);\n        return ans;\n    }\n};\n\nint main() {\n    TreeNode* root = new TreeNode(3);\n    root->left = new TreeNode(1);\n    root->right = new TreeNode(4);\n    root->left->right = new TreeNode(2);\n    \n    Solution sol;\n    cout << "Kth Smallest: " << sol.kthSmallest(root, 1) << " (Expected: 1)" << endl;\n    return 0;\n}`,
      python: `from typing import Optional\n\nclass TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\nclass Solution:\n    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:\n        n = 0\n        stack = []\n        curr = root\n        \n        while curr or stack:\n            while curr:\n                stack.append(curr)\n                curr = curr.left\n            curr = stack.pop()\n            n += 1\n            if n == k:\n                return curr.val\n            curr = curr.right\n\nif __name__ == "__main__":\n    root = TreeNode(3, TreeNode(1, None, TreeNode(2)), TreeNode(4))\n    sol = Solution()\n    print(f"Kth Smallest: {sol.kthSmallest(root, 1)} (Expected: 1)")`
    },
    complexity: { time: "O(n)", space: "O(h)" },
    explanation: "An In-order Traversal (`Left -> Node -> Right`) of a Binary Search Tree visits nodes in strictly sorted ascending order. We traverse the tree in-order, keeping a counter. When the counter reaches `k`, the current node's value is our answer."
  },

  // ==================== HEAP / PRIORITY QUEUE ====================
  {
    id: 40,
    name: "Kth Largest Element in a Stream",
    category: "Heap / Priority Queue",
    difficulty: "Easy",
    leetCodeUrl: "https://leetcode.com/problems/kth-largest-element-in-a-stream/",
    description: "Design a class to find the `k`-th largest element in a stream. Note that it is the `k`-th largest element in the sorted order, not the `k`-th distinct element.\n\nImplement `KthLargest` class:\n* `KthLargest(int k, int[] nums)` Initializes the object with the integer `k` and the stream of integers `nums`.\n* `int add(int val)` Appends the integer `val` to the stream and returns the element representing the `k`-th largest element in the stream.",
    examples: [
      { input: "[\"KthLargest\",\"add\",\"add\",\"add\",\"add\",\"add\"]\\n[[3,[4,5,8,2]],[3],[5],[10],[9],[4]]", output: "[null,4,5,5,8,8]" }
    ],
    constraints: ["`1 <= k <= 10^4`", "`0 <= nums.length <= 10^4`", "`-10^4 <= nums[i], val <= 10^4`", "At most `10^4` calls to `add`."],
    starterCode: {
      cpp: `#include <iostream>\n#include <vector>\n#include <queue>\n\nusing namespace std;\n\nclass KthLargest {\npublic:\n    KthLargest(int k, vector<int>& nums) {\n        \n    }\n    \n    int add(int val) {\n        return 0;\n    }\n};\n\nint main() {\n    vector<int> nums = {4, 5, 8, 2};\n    KthLargest* obj = new KthLargest(3, nums);\n    cout << obj->add(3) << endl;\n    return 0;\n}`,
      python: `from typing import List\nimport heapq\n\nclass KthLargest:\n    def __init__(self, k: int, nums: List[int]):\n        pass\n            \n    def add(self, val: int) -> int:\n        return 0\n\nif __name__ == "__main__":\n    obj = KthLargest(3, [4, 5, 8, 2])\n    print(obj.add(3))`
    },
    solutions: {
      cpp: `#include <iostream>\n#include <vector>\n#include <queue>\n\nusing namespace std;\n\nclass KthLargest {\nprivate:\n    priority_queue<int, vector<int>, greater<int>> min_heap;\n    int k_size;\npublic:\n    KthLargest(int k, vector<int>& nums) {\n        k_size = k;\n        for (int num : nums) {\n            add(num);\n        }\n    }\n    \n    int add(int val) {\n        min_heap.push(val);\n        if (min_heap.size() > k_size) {\n            min_heap.pop();\n        }\n        return min_heap.top();\n    }\n};\n\nint main() {\n    vector<int> nums = {4, 5, 8, 2};\n    KthLargest kthLargest(3, nums);\n    cout << "Add 3: " << kthLargest.add(3) << " (Expected: 4)" << endl;\n    cout << "Add 5: " << kthLargest.add(5) << " (Expected: 5)" << endl;\n    cout << "Add 10: " << kthLargest.add(10) << " (Expected: 5)" << endl;\n    return 0;\n}`,
      python: `from typing import List\nimport heapq\n\nclass KthLargest:\n    def __init__(self, k: int, nums: List[int]):\n        self.minHeap, self.k = nums, k\n        heapq.heapify(self.minHeap)\n        while len(self.minHeap) > k:\n            heapq.heappop(self.minHeap)\n            \n    def add(self, val: int) -> int:\n        heapq.heappush(self.minHeap, val)\n        if len(self.minHeap) > self.k:\n            heapq.heappop(self.minHeap)\n        return self.minHeap[0]\n\nif __name__ == "__main__":\n    obj = KthLargest(3, [4, 5, 8, 2])\n    print(f"Add 3: {obj.add(3)} (Expected: 4)")\n    print(f"Add 5: {obj.add(5)} (Expected: 5)")\n    print(f"Add 10: {obj.add(10)} (Expected: 5)")`
    },
    complexity: { time: "O(log k) for add, O(n log k) for initialization", space: "O(k)" },
    explanation: "We utilize a Min Heap of maximum size `k`. A min-heap keeps the smallest of the `k` largest items at its root. When we insert an element, if the heap exceeds size `k`, we pop the top (evicting the smallest of the top `k` elements). The `k`th largest is then always sitting at the top of the heap."
  },
  {
    id: 41,
    name: "Last Stone Weight",
    category: "Heap / Priority Queue",
    difficulty: "Easy",
    leetCodeUrl: "https://leetcode.com/problems/last-stone-weight/",
    description: "You are given an array of integers `stones` where `stones[i]` is the weight of the `i`-th stone.\n\nWe are playing a game with the stones. On each turn, we choose the **heaviest two stones** and smash them together. Suppose the heaviest two stones have weights `x` and `y` with `x <= y`. The result of this smash is:\n* If `x == y`, both stones are destroyed,\n* If `x != y`, the stone of weight `x` is destroyed, and the stone of weight `y` has new weight `y - x`.\n\nAt the end of the game, there is **at most one** stone left.\n\nReturn *the weight of the last remaining stone*. If no stones are left, return `0`.",
    examples: [
      { input: "stones = [2,7,4,1,8,1]", output: "1" }
    ],
    constraints: ["`1 <= stones.length <= 30`", "`1 <= stones[i] <= 1000`"],
    starterCode: {
      cpp: `#include <iostream>\n#include <vector>\n#include <queue>\n\nusing namespace std;\n\nclass Solution {\npublic:\n    int lastStoneWeight(vector<int>& stones) {\n        // Write code here\n        return 0;\n    }\n};\n\nint main() {\n    Solution sol;\n    vector<int> stones = {2, 7, 4, 1, 8, 1};\n    cout << sol.lastStoneWeight(stones) << endl;\n    return 0;\n}`,
      python: `from typing import List\nimport heapq\n\nclass Solution:\n    def lastStoneWeight(self, stones: List[int]) -> int:\n        # Write code here\n        return 0\n\nif __name__ == "__main__":\n    sol = Solution()\n    print(sol.lastStoneWeight([2, 7, 4, 1, 8, 1]))`
    },
    solutions: {
      cpp: `#include <iostream>\n#include <vector>\n#include <queue>\n\nusing namespace std;\n\nclass Solution {\npublic:\n    int lastStoneWeight(vector<int>& stones) {\n        priority_queue<int> max_heap(stones.begin(), stones.end());\n        while (max_heap.size() > 1) {\n            int y = max_heap.top(); max_heap.pop();\n            int x = max_heap.top(); max_heap.pop();\n            if (x != y) {\n                max_heap.push(y - x);\n            }\n        }\n        return max_heap.empty() ? 0 : max_heap.top();\n    }\n};\n\nint main() {\n    Solution sol;\n    vector<int> stones = {2, 7, 4, 1, 8, 1};\n    cout << "Last stone weight: " << sol.lastStoneWeight(stones) << " (Expected: 1)" << endl;\n    return 0;\n}`,
      python: `from typing import List\nimport heapq\n\nclass Solution:\n    def lastStoneWeight(self, stones: List[int]) -> int:\n        stones = [-s for s in stones]\n        heapq.heapify(stones)\n        \n        while len(stones) > 1:\n            first = heapq.heappop(stones)\n            second = heapq.heappop(stones)\n            if second > first:\n                heapq.heappush(stones, first - second)\n                \n        stones.append(0)\n        return abs(stones[0])\n\nif __name__ == "__main__":\n    sol = Solution()\n    print(f"Last stone weight: {sol.lastStoneWeight([2, 7, 4, 1, 8, 1])} (Expected: 1)")`
    },
    complexity: { time: "O(n log n)", space: "O(n)" },
    explanation: "We need to repeatedly pull the two largest stones. We utilize a Max Heap. C++ `priority_queue` is a max-heap by default. Python's `heapq` is a min-heap, so we multiply all values by `-1` to simulate a max-heap. In each step, we pop the two largest stones. If they differ, we push the remaining difference back. We stop when $\\le 1$ stones remain."
  },
  {
    id: 42,
    name: "Kth Largest Element in an Array",
    category: "Heap / Priority Queue",
    difficulty: "Medium",
    leetCodeUrl: "https://leetcode.com/problems/kth-largest-element-in-an-array/",
    description: "Given an integer array `nums` and an integer `k`, return *the* `k`-th *largest element in the array*.\n\nNote that it is the `k`-th largest element in the sorted order, not the `k`-th distinct element.\n\nCan you solve it without sorting in `O(n)` time?",
    examples: [
      { input: "nums = [3,2,1,5,6,4], k = 2", output: "5" }
    ],
    constraints: ["`1 <= k <= nums.length <= 10^5`", "`-10^4 <= nums[i] <= 10^4`"],
    starterCode: {
      cpp: `#include <iostream>\n#include <vector>\n#include <queue>\n\nusing namespace std;\n\nclass Solution {\npublic:\n    int findKthLargest(vector<int>& nums, int k) {\n        // Write code here\n        return 0;\n    }\n};\n\nint main() {\n    Solution sol;\n    vector<int> nums = {3, 2, 1, 5, 6, 4};\n    cout << sol.findKthLargest(nums, 2) << endl;\n    return 0;\n}`,
      python: `from typing import List\nimport heapq\n\nclass Solution:\n    def findKthLargest(self, nums: List[int], k: int) -> int:\n        # Write code here\n        return 0\n\nif __name__ == "__main__":\n    sol = Solution()\n    print(sol.findKthLargest([3, 2, 1, 5, 6, 4], 2))`
    },
    solutions: {
      cpp: `#include <iostream>\n#include <vector>\n#include <queue>\n\nusing namespace std;\n\nclass Solution {\npublic:\n    int findKthLargest(vector<int>& nums, int k) {\n        priority_queue<int, vector<int>, greater<int>> min_heap;\n        for (int num : nums) {\n            min_heap.push(num);\n            if (min_heap.size() > k) {\n                min_heap.pop();\n            }\n        }\n        return min_heap.top();\n    }\n};\n\nint main() {\n    Solution sol;\n    vector<int> nums = {3, 2, 1, 5, 6, 4};\n    cout << "Kth largest: " << sol.findKthLargest(nums, 2) << " (Expected: 5)" << endl;\n    return 0;\n}`,
      python: `from typing import List\nimport heapq\n\nclass Solution:\n    def findKthLargest(self, nums: List[int], k: int) -> int:\n        minHeap = []\n        for num in nums:\n            heapq.heappush(minHeap, num)\n            if len(minHeap) > k:\n                heapq.heappop(minHeap)\n        return minHeap[0]\n\nif __name__ == "__main__":\n    sol = Solution()\n    print(f"Kth largest: {sol.findKthLargest([3, 2, 1, 5, 6, 4], 2)} (Expected: 5)")`
    },
    complexity: { time: "O(n log k)", space: "O(k)" },
    explanation: "We utilize a Min Heap of size `k`. We iterate through the array, pushing elements into the heap. If the size of the heap exceeds `k`, we pop the smallest element. After traversing the whole array, the minimum element of the `k` largest elements will be at the top of our heap, which is the `k`th largest."
  },

  // ==================== GRAPHS ====================
  {
    id: 43,
    name: "Number of Islands",
    category: "Graphs",
    difficulty: "Medium",
    leetCodeUrl: "https://leetcode.com/problems/number-of-islands/",
    description: "Given an `m x n` 2D binary grid `grid` which represents a map of `'1'`s (land) and `'0'`s (water), return *the number of islands*.\n\nAn **island** is surrounded by water and is formed by connecting adjacent lands horizontally or vertically. You may assume all four edges of the grid are all surrounded by water.",
    examples: [
      { input: "grid = [[\"1\",\"1\",\"1\",\"1\",\"0\"], [\"1\",\"1\",\"0\",\"1\",\"0\"], [\"1\",\"1\",\"0\",\"0\",\"0\"], [\"0\",\"0\",\"0\",\"0\",\"0\"]]", output: "1" }
    ],
    constraints: ["`m == grid.length`", "`n == grid[i].length`", "`1 <= m, n <= 300`", "`grid[i][j]` is `'0'` or `'1'`."],
    starterCode: {
      cpp: `#include <iostream>\n#include <vector>\n\nusing namespace std;\n\nclass Solution {\npublic:\n    int numIslands(vector<vector<char>>& grid) {\n        // Write code here\n        return 0;\n    }\n};\n\nint main() {\n    Solution sol;\n    vector<vector<char>> grid = {\n        {'1','1','0','0','0'},\n        {'1','1','0','0','0'},\n        {'0','0','1','0','0'},\n        {'0','0','0','1','1'}\n    };\n    cout << sol.numIslands(grid) << endl;\n    return 0;\n}`,
      python: `from typing import List\nimport collections\n\nclass Solution:\n    def numIslands(self, grid: List[List[str]]) -> int:\n        # Write code here\n        return 0\n\nif __name__ == "__main__":\n    sol = Solution()\n    grid = [\n        ["1","1","0","0","0"],\n        ["1","1","0","0","0"],\n        ["0","0","1","0","0"],\n        ["0","0","0","1","1"]\n    ]\n    print(sol.numIslands(grid))`
    },
    solutions: {
      cpp: `#include <iostream>\n#include <vector>\n\nusing namespace std;\n\nclass Solution {\nprivate:\n    void dfs(vector<vector<char>>& grid, int r, int c) {\n        int m = grid.size(), n = grid[0].size();\n        if (r < 0 || c < 0 || r >= m || c >= n || grid[r][c] == '0') return;\n        \n        grid[r][c] = '0'; \n        dfs(grid, r + 1, c);\n        dfs(grid, r - 1, c);\n        dfs(grid, r, c + 1);\n        dfs(grid, r, c - 1);\n    }\npublic:\n    int numIslands(vector<vector<char>>& grid) {\n        if (grid.empty()) return 0;\n        int islands = 0;\n        for (int i = 0; i < grid.size(); ++i) {\n            for (int j = 0; j < grid[0].size(); ++j) {\n                if (grid[i][j] == '1') {\n                    islands++;\n                    dfs(grid, i, j);\n                }\n            }\n        }\n        return islands;\n    }\n};\n\nint main() {\n    Solution sol;\n    vector<vector<char>> grid = {\n        {'1','1','0','0','0'},\n        {'1','1','0','0','0'},\n        {'0','0','1','0','0'},\n        {'0','0','0','1','1'}\n    };\n    cout << "Islands: " << sol.numIslands(grid) << " (Expected: 3)" << endl;\n    return 0;\n}`,
      python: `from typing import List\nimport collections\n\nclass Solution:\n    def numIslands(self, grid: List[List[str]]) -> int:\n        if not grid: return 0\n        \n        rows, cols = len(grid), len(grid[0])\n        visit = set()\n        islands = 0\n        \n        def bfs(r, c):\n            q = collections.deque()\n            visit.add((r, c))\n            q.append((r, c))\n            while q:\n                row, col = q.popleft()\n                directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]\n                for dr, dc in directions:\n                    nr, nc = row + dr, col + dc\n                    if (nr in range(rows) and nc in range(cols) and \n                        grid[nr][nc] == "1" and (nr, nc) not in visit):\n                        q.append((nr, nc))\n                        visit.add((nr, nc))\n                        \n        for r in range(rows):\n            for c in range(cols):\n                if grid[r][c] == "1" and (r, c) not in visit:\n                    bfs(r, c)\n                    islands += 1\n        return islands\n\nif __name__ == "__main__":\n    sol = Solution()\n    grid = [\n        ["1","1","0","0","0"],\n        ["1","1","0","0","0"],\n        ["0","0","1","0","0"],\n        ["0","0","0","1","1"]\n    ]\n    print(f"Islands: {sol.numIslands(grid)} (Expected: 3)")`
    },
    complexity: { time: "O(m * n)", space: "O(m * n)" },
    explanation: "We scan the 2D grid cell by cell. When we find a `'1'` (land), we increment our island count and trigger a Depth First Search (DFS) or Breadth First Search (BFS) to traverse all adjacent horizontally or vertically connected land cells. We mark visited cells as `'0'` to prevent re-visiting them."
  },
  {
    id: 44,
    name: "Max Area of Island",
    category: "Graphs",
    difficulty: "Medium",
    leetCodeUrl: "https://leetcode.com/problems/max-area-of-island/",
    description: "You are given an `m x n` binary matrix `grid`. An island is a group of `1`s (representing land) connected **4-directionally** (horizontal or vertical.) You may assume all four edges of the grid are surrounded by water.\n\nThe **area** of an island is the number of cells with a value `1` in the island.\n\nReturn *the maximum **area** of an island in* `grid`. If there is no island, return `0`.",
    examples: [
      { input: "grid = [[0,0,1,0,0,0,0,1,0,0,0,0,0], ...]", output: "6" }
    ],
    constraints: ["`m == grid.length`", "`n == grid[i].length`", "`1 <= m, n <= 50`", "`grid[i][j]` is `0` or `1`."],
    starterCode: {
      cpp: `#include <iostream>\n#include <vector>\n#include <algorithm>\n\nusing namespace std;\n\nclass Solution {\npublic:\n    int maxAreaOfIsland(vector<vector<int>>& grid) {\n        // Write code here\n        return 0;\n    }\n};\n\nint main() {\n    Solution sol;\n    vector<vector<int>> grid = {\n        {0,0,1,0,0},\n        {0,0,1,1,0},\n        {0,1,1,0,0},\n        {0,0,0,1,1}\n    };\n    cout << sol.maxAreaOfIsland(grid) << endl;\n    return 0;\n}`,
      python: `from typing import List\n\nclass Solution:\n    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:\n        # Write code here\n        return 0\n\nif __name__ == "__main__":\n    sol = Solution()\n    grid = [\n        [0,0,1,0,0],\n        [0,0,1,1,0],\n        [0,1,1,0,0],\n        [0,0,0,1,1]\n    ]\n    print(sol.maxAreaOfIsland(grid))`
    },
    solutions: {
      cpp: `#include <iostream>\n#include <vector>\n#include <algorithm>\n\nusing namespace std;\n\nclass Solution {\nprivate:\n    int dfs(vector<vector<int>>& grid, int r, int c) {\n        if (r < 0 || c < 0 || r >= grid.size() || c >= grid[0].size() || grid[r][c] == 0) return 0;\n        grid[r][c] = 0;\n        return 1 + dfs(grid, r + 1, c) + dfs(grid, r - 1, c) + dfs(grid, r, c + 1) + dfs(grid, r, c - 1);\n    }\npublic:\n    int maxAreaOfIsland(vector<vector<int>>& grid) {\n        int max_area = 0;\n        for (int i = 0; i < grid.size(); ++i) {\n            for (int j = 0; j < grid[0].size(); ++j) {\n                if (grid[i][j] == 1) {\n                    max_area = max(max_area, dfs(grid, i, j));\n                }\n            }\n        }\n        return max_area;\n    }\n};\n\nint main() {\n    Solution sol;\n    vector<vector<int>> grid = {\n        {0,0,1,0,0},\n        {0,0,1,1,0},\n        {0,1,1,0,0},\n        {0,0,0,1,1}\n    };\n    cout << "Max area: " << sol.maxAreaOfIsland(grid) << " (Expected: 5)" << endl;\n    return 0;\n}`,
      python: `from typing import List\n\nclass Solution:\n    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:\n        ROWS, COLS = len(grid), len(grid[0])\n        visit = set()\n        \n        def dfs(r, c):\n            if r < 0 or r >= ROWS or c < 0 or c >= COLS or grid[r][c] == 0 or (r, c) in visit:\n                return 0\n            visit.add((r, c))\n            return (1 + dfs(r + 1, c) +\n                       dfs(r - 1, c) +\n                       dfs(r, c + 1) +\n                       dfs(r, c - 1))\n                       \n        max_area = 0\n        for r in range(ROWS):\n            for c in range(COLS):\n                if grid[r][c] == 1 and (r, c) not in visit:\n                    max_area = max(max_area, dfs(r, c))\n        return max_area\n\nif __name__ == "__main__":\n    sol = Solution()\n    grid = [\n        [0,0,1,0,0],\n        [0,0,1,1,0],\n        [0,1,1,0,0],\n        [0,0,0,1,1]\n    ]\n    print(f"Max Area: {sol.maxAreaOfIsland(grid)} (Expected: 5)")`
    },
    complexity: { time: "O(m * n)", space: "O(m * n)" },
    explanation: "This is a direct extension of the 'Number of Islands' problem. As we traverse the grid and locate land (`1`), we trigger a DFS. Instead of just marking nodes visited, our DFS returns `1` (for the current node) plus the sums returned by all recursive DFS calls on adjacent cells. We keep track of the maximum area."
  },
  {
    id: 45,
    name: "Clone Graph",
    category: "Graphs",
    difficulty: "Medium",
    leetCodeUrl: "https://leetcode.com/problems/clone-graph/",
    description: "Given a reference of a node in a **connected** undirected graph.\n\nReturn a **deep copy** (clone) of the graph.\n\nEach node in the graph contains a value (`int`) and a list (`List[Node]`) of its neighbors.\n\n```cpp\nclass Node {\npublic:\n    int val;\n    vector<Node*> neighbors;\n};\n```",
    examples: [
      { input: "adjList = [[2,4],[1,3],[2,4],[1,3]]", output: "[[2,4],[1,3],[2,4],[1,3]]" }
    ],
    constraints: ["The number of nodes in the graph is in the range `[0, 100]`.", "`1 <= Node.val <= 100`", "Node values are unique.", "The Graph is connected and has no duplicate edges."],
    starterCode: {
      cpp: `#include <iostream>\n#include <vector>\n#include <unordered_map>\n\nusing namespace std;\n\nclass Node {\npublic:\n    int val;\n    vector<Node*> neighbors;\n    Node() : val(0) {}\n    Node(int _val) : val(_val) {}\n};\n\nclass Solution {\npublic:\n    Node* cloneGraph(Node* node) {\n        // Write code here\n        return node;\n    }\n};\n\nint main() {\n    Node* node = new Node(1);\n    Solution sol;\n    Node* clone = sol.cloneGraph(node);\n    cout << clone->val << endl;\n    return 0;\n}`,
      python: `from typing import Optional\n\nclass Node:\n    def __init__(self, val = 0, neighbors = None):\n        self.val = val\n        self.neighbors = neighbors if neighbors is not None else []\n\nclass Solution:\n    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:\n        # Write code here\n        return node\n\nif __name__ == "__main__":\n    node = Node(1)\n    sol = Solution()\n    clone = sol.cloneGraph(node)\n    print(clone.val)`
    },
    solutions: {
      cpp: `#include <iostream>\n#include <vector>\n#include <unordered_map>\n\nusing namespace std;\n\nclass Node {\npublic:\n    int val;\n    vector<Node*> neighbors;\n    Node() : val(0) {}\n    Node(int _val) : val(_val) {}\n};\n\nclass Solution {\nprivate:\n    unordered_map<Node*, Node*> copies;\npublic:\n    Node* cloneGraph(Node* node) {\n        if (!node) return nullptr;\n        if (copies.count(node)) return copies[node];\n        \n        Node* copy = new Node(node->val);\n        copies[node] = copy;\n        for (Node* neighbor : node->neighbors) {\n            copy->neighbors.push_back(cloneGraph(neighbor));\n        }\n        return copy;\n    }\n};\n\nint main() {\n    Node* node1 = new Node(1);\n    Node* node2 = new Node(2);\n    node1->neighbors.push_back(node2);\n    node2->neighbors.push_back(node1);\n    \n    Solution sol;\n    Node* clone = sol.cloneGraph(node1);\n    cout << "Cloned root node value: " << clone->val << " (Expected: 1)" << endl;\n    cout << "Cloned neighbor value: " << clone->neighbors[0]->val << " (Expected: 2)" << endl;\n    return 0;\n}`,
      python: `from typing import Optional\n\nclass Node:\n    def __init__(self, val = 0, neighbors = None):\n        self.val = val\n        self.neighbors = neighbors if neighbors is not None else []\n\nclass Solution:\n    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:\n        oldToNew = {}\n        \n        def dfs(node):\n            if not node:\n                return None\n            if node in oldToNew:\n                return oldToNew[node]\n                \n            copy = Node(node.val)\n            oldToNew[node] = copy\n            for neighbor in node.neighbors:\n                copy.neighbors.append(dfs(neighbor))\n            return copy\n            \n        return dfs(node)\n\nif __name__ == "__main__":\n    node1 = Node(1)\n    node2 = Node(2)\n    node1.neighbors.append(node2)\n    node2.neighbors.append(node1)\n    \n    sol = Solution()\n    clone = sol.cloneGraph(node1)\n    print(f"Cloned root node: {clone.val} (Expected: 1)")\n    print(f"Cloned neighbor node: {clone.neighbors[0].val} (Expected: 2)")`
    },
    complexity: { time: "O(V + E)", space: "O(V)" },
    explanation: "To clone a graph, we must avoid circular dependency lockups. We utilize a Hash Map that maps original nodes to their corresponding cloned counterparts. We trigger a DFS: 1. If the node has already been cloned, return the cloned instance. 2. Otherwise, construct a new node copy, record it in our map, recursively clone all its neighbors, and link them to the new clone."
  },
  {
    id: 46,
    name: "Pacific Atlantic Water Flow",
    category: "Graphs",
    difficulty: "Medium",
    leetCodeUrl: "https://leetcode.com/problems/pacific-atlantic-water-flow/",
    description: "There is an `m x n` rectangular island that borders both the **Pacific Ocean** and **Atlantic Ocean**. The Pacific Ocean touches the island's left and top edges, and the Atlantic Ocean touches the island's right and bottom edges.\n\nThe island is partitioned into a grid of square cells. You are given an `m x n` integer matrix `heights` where `heights[r][c]` represents the height above sea level of the cell at coordinate `(r, c)`.\n\nRain water can flow to neighboring cells in four directions (up, down, left, and right) if the neighboring cell's height is **less than or equal to** the current cell's height. Water can flow from any cell adjacent to an ocean into the ocean.\n\nReturn *a **2D list** of grid coordinates* `result` *where* `result[i] = [ri, ci]` *denotes that rain water can flow from cell* `(ri, ci)` *to **both** the Pacific and Atlantic oceans*.",
    examples: [
      { input: "heights = [[1,2,2,3,5],[3,2,3,4,4],[2,4,5,3,1],[6,7,1,4,5],[5,1,1,2,4]]", output: "[[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]]" }
    ],
    constraints: ["`m == heights.length`", "`n == heights[r].length`", "`1 <= m, n <= 200`", "`0 <= heights[r][c] <= 10^5`"],
    starterCode: {
      cpp: `#include <iostream>\n#include <vector>\n\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<vector<int>> pacificAtlantic(vector<vector<int>>& heights) {\n        // Write code here\n        return {};\n    }\n};\n\nint main() {\n    Solution sol;\n    vector<vector<int>> grid = {{1, 2}, {2, 1}};\n    sol.pacificAtlantic(grid);\n    return 0;\n}`,
      python: `from typing import List\n\nclass Solution:\n    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:\n        # Write code here\n        return []\n\nif __name__ == "__main__":\n    sol = Solution()\n    print(sol.pacificAtlantic([[1, 2], [2, 1]]))`
    },
    solutions: {
      cpp: `#include <iostream>\n#include <vector>\n\nusing namespace std;\n\nclass Solution {\nprivate:\n    int m, n;\n    void dfs(vector<vector<int>>& heights, int r, int c, int prev_h, vector<vector<bool>>& ocean) {\n        if (r < 0 || c < 0 || r >= m || c >= n || ocean[r][c] || heights[r][c] < prev_h) return;\n        ocean[r][c] = true;\n        dfs(heights, r + 1, c, heights[r][c], ocean);\n        dfs(heights, r - 1, c, heights[r][c], ocean);\n        dfs(heights, r, c + 1, heights[r][c], ocean);\n        dfs(heights, r, c - 1, heights[r][c], ocean);\n    }\npublic:\n    vector<vector<int>> pacificAtlantic(vector<vector<int>>& heights) {\n        vector<vector<int>> res;\n        if (heights.empty()) return res;\n        m = heights.size(); n = heights[0].size();\n        \n        vector<vector<bool>> pac(m, vector<bool>(n, false));\n        vector<vector<bool>> atl(m, vector<bool>(n, false));\n        \n        for (int i = 0; i < m; ++i) {\n            dfs(heights, i, 0, -1, pac);\n            dfs(heights, i, n - 1, -1, atl);\n        }\n        for (int j = 0; j < n; ++j) {\n            dfs(heights, 0, j, -1, pac);\n            dfs(heights, m - 1, j, -1, atl);\n        }\n        \n        for (int i = 0; i < m; ++i) {\n            for (int j = 0; j < n; ++j) {\n                if (pac[i][j] && atl[i][j]) {\n                    res.push_back({i, j});\n                }\n            }\n        }\n        return res;\n    }\n};\n\nint main() {\n    Solution sol;\n    vector<vector<int>> grid = {\n        {1, 2, 2, 3, 5},\n        {3, 2, 3, 4, 4},\n        {2, 4, 5, 3, 1},\n        {6, 7, 1, 4, 5},\n        {5, 1, 1, 2, 4}\n    };\n    vector<vector<int>> res = sol.pacificAtlantic(grid);\n    cout << "Flow coordinates:\\n";\n    for (auto& coord : res) {\n        cout << "[" << coord[0] << ", " << coord[1] << "] ";\n    }\n    cout << endl;\n    return 0;\n}`,
      python: `from typing import List\n\nclass Solution:\n    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:\n        ROWS, COLS = len(heights), len(heights[0])\n        pac, atl = set(), set()\n        \n        def dfs(r, c, visit, prevHeight):\n            if ((r, c) in visit or\n                r < 0 or c < 0 or r == ROWS or c == COLS or\n                heights[r][c] < prevHeight):\n                return\n            visit.add((r, c))\n            dfs(r + 1, c, visit, heights[r][c])\n            dfs(r - 1, c, visit, heights[r][c])\n            dfs(r, c + 1, visit, heights[r][c])\n            dfs(r, c - 1, visit, heights[r][c])\n            \n        for c in range(COLS):\n            dfs(0, c, pac, heights[0][c])\n            dfs(ROWS - 1, c, atl, heights[ROWS - 1][c])\n            \n        for r in range(ROWS):\n            dfs(r, 0, pac, heights[r][0])\n            dfs(r, COLS - 1, atl, heights[r][COLS - 1])\n            \n        res = []\n        for r in range(ROWS):\n            for c in range(COLS):\n                if (r, c) in pac and (r, c) in atl:\n                    res.append([r, c])\n        return res\n\nif __name__ == "__main__":\n    sol = Solution()\n    grid = [\n        [1, 2, 2, 3, 5],\n        [3, 2, 3, 4, 4],\n        [2, 4, 5, 3, 1],\n        [6, 7, 1, 4, 5],\n        [5, 1, 1, 2, 4]\n    ]\n    print(f"Flow coordinates: {sol.pacificAtlantic(grid)}")`
    },
    complexity: { time: "O(m * n)", space: "O(m * n)" },
    explanation: "Instead of searching downwards from each cell to see if they reach both oceans (which takes $O(m^2 \\cdot n^2)$), we work in reverse. We start at the coastal ocean cells and search **upwards** (only moving to equal or higher neighbors). We trigger a DFS from the Pacific borders and another from the Atlantic. Cells visited in both DFS runs are the solution."
  },
  {
    id: 47,
    name: "Surrounded Regions",
    category: "Graphs",
    difficulty: "Medium",
    leetCodeUrl: "https://leetcode.com/problems/surrounded-regions/",
    description: "Given an `m x n` matrix `board` containing `'X'` and `'O'`, *capture all regions that are 4-directionally surrounded by* `'X'`.\n\nA region is **captured** by flipping all `'O'`s into `'X'`s in that surrounded region.",
    examples: [
      { input: "board = [[\"X\",\"X\",\"X\",\"X\"],[\"X\",\"O\",\"O\",\"X\"],[\"X\",\"X\",\"O\",\"X\"],[\"X\",\"O\",\"X\",\"X\"]]", output: "[[\"X\",\"X\",\"X\",\"X\"],[\"X\",\"X\",\"X\",\"X\"],[\"X\",\"X\",\"X\",\"X\"],[\"X\",\"O\",\"X\",\"X\"]]" }
    ],
    constraints: ["`m == board.length`", "`n == board[i].length`", "`1 <= m, n <= 200`", "`board[i][j]` is `'X'` or `'O'`."],
    starterCode: {
      cpp: `#include <iostream>\n#include <vector>\n\nusing namespace std;\n\nclass Solution {\npublic:\n    void solve(vector<vector<char>>& board) {\n        // Write code here\n    }\n};\n\nint main() {\n    Solution sol;\n    vector<vector<char>> board = {{'X', 'O'}, {'O', 'X'}};\n    sol.solve(board);\n    return 0;\n}`,
      python: `from typing import List\n\nclass Solution:\n    def solve(self, board: List[List[str]]) -> None:\n        # Write code here\n        pass\n\nif __name__ == "__main__":\n    sol = Solution()\n    board = [["X", "O"], ["O", "X"]]\n    sol.solve(board)`
    },
    solutions: {
      cpp: `#include <iostream>\n#include <vector>\n\nusing namespace std;\n\nclass Solution {\nprivate:\n    int m, n;\n    void dfs(vector<vector<char>>& board, int r, int c) {\n        if (r < 0 || c < 0 || r >= m || c >= n || board[r][c] != 'O') return;\n        board[r][c] = 'T';\n        dfs(board, r + 1, c);\n        dfs(board, r - 1, c);\n        dfs(board, r, c + 1);\n        dfs(board, r, c - 1);\n    }\npublic:\n    void solve(vector<vector<char>>& board) {\n        if (board.empty()) return;\n        m = board.size(); n = board[0].size();\n        \n        for (int i = 0; i < m; ++i) {\n            dfs(board, i, 0);\n            dfs(board, i, n - 1);\n        }\n        for (int j = 0; j < n; ++j) {\n            dfs(board, 0, j);\n            dfs(board, m - 1, j);\n        }\n        \n        for (int i = 0; i < m; ++i) {\n            for (int j = 0; j < n; ++j) {\n                if (board[i][j] == 'O') board[i][j] = 'X';\n                else if (board[i][j] == 'T') board[i][j] = 'O';\n            }\n        }\n    }\n};\n\nint main() {\n    Solution sol;\n    vector<vector<char>> board = {\n        {'X', 'X', 'X', 'X'},\n        {'X', 'O', 'O', 'X'},\n        {'X', 'X', 'O', 'X'},\n        {'X', 'O', 'X', 'X'}\n    };\n    sol.solve(board);\n    cout << "Board state after solving:\\n";\n    for (auto& row : board) {\n        for (char c : row) cout << c << " ";\n        cout << "\\n";\n    }\n    return 0;\n}`,
      python: `from typing import List\n\nclass Solution:\n    def solve(self, board: List[List[str]]) -> None:\n        ROWS, COLS = len(board), len(board[0])\n        \n        def capture(r, c):\n            if r < 0 or c < 0 or r == ROWS or c == COLS or board[r][c] != "O":\n                return\n            board[r][c] = "T"\n            capture(r + 1, c)\n            capture(r - 1, c)\n            capture(r, c + 1)\n            capture(r, c - 1)\n            \n        for r in range(ROWS):\n            for c in range(COLS):\n                if board[r][c] == "O" and (r in [0, ROWS - 1] or c in [0, COLS - 1]):\n                    capture(r, c)\n                    \n        for r in range(ROWS):\n            for c in range(COLS):\n                if board[r][c] == "O":\n                    board[r][c] = "X"\n                    \n        for r in range(ROWS):\n            for c in range(COLS):\n                if board[r][c] == "T":\n                    board[r][c] = "O"\n\nif __name__ == "__main__":\n    sol = Solution()\n    board = [\n        ["X","X","X","X"],\n        ["X","O","O","X"],\n        ["X","X","O","X"],\n        ["X","O","X","X"]\n    ]\n    sol.solve(board)\n    print(f"Board solved: {board}")`
    },
    complexity: { time: "O(m * n)", space: "O(m * n)" },
    explanation: "Any cell containing `'O'` that resides on the grid boundary, or is connected to a boundary cell with `'O'`s, cannot be captured. We start by launching a DFS from all `'O'`s on the boundaries, and mark them as `'T'` (temporary safe). After marking, we scan the board: we flip unmarked `'O'`s to `'X'`, and revert `'T'`s back to `'O'`s."
  },
  {
    id: 48,
    name: "Course Schedule",
    category: "Graphs",
    difficulty: "Medium",
    leetCodeUrl: "https://leetcode.com/problems/course-schedule/",
    description: "There are a total of `numCourses` courses you have to take, labeled from `0` to `numCourses - 1`. You are given an array `prerequisites` where `prerequisites[i] = [ai, bi]` indicates that you **must** take course `bi` first if you want to take course `ai`.\n\n* For example, the pair `[0, 1]`, indicates that to take course `0` you have to first take course `1`.\n\nReturn `true` if you can finish all courses. Otherwise, return `false`.",
    examples: [
      { input: "numCourses = 2, prerequisites = [[1,0]]", output: "true", explanation: "There are a total of 2 courses to take. To take course 1 you should have finished course 0. So it is possible." }
    ],
    constraints: ["`1 <= numCourses <= 2000`", "`0 <= prerequisites.length <= 5000`", "`prerequisites[i].length == 2`", "All prerequisite pairs are **unique**."],
    starterCode: {
      cpp: `#include <iostream>\n#include <vector>\n\nusing namespace std;\n\nclass Solution {\npublic:\n    bool canFinish(int numCourses, vector<vector<int>>& prerequisites) {\n        // Write code here\n        return false;\n    }\n};\n\nint main() {\n    Solution sol;\n    vector<vector<int>> pre = {{1, 0}};\n    cout << (sol.canFinish(2, pre) ? "True" : "False") << endl;\n    return 0;\n}`,
      python: `from typing import List\n\nclass Solution:\n    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:\n        # Write code here\n        return False\n\nif __name__ == "__main__":\n    sol = Solution()\n    print(sol.canFinish(2, [[1, 0]]))`
    },
    solutions: {
      cpp: `#include <iostream>\n#include <vector>\n\nusing namespace std;\n\nclass Solution {\nprivate:\n    bool hasCycle(int node, vector<vector<int>>& adj, vector<int>& visit) {\n        if (visit[node] == 1) return true; \n        if (visit[node] == 2) return false; \n        \n        visit[node] = 1;\n        for (int neighbor : adj[node]) {\n            if (hasCycle(neighbor, adj, visit)) return true;\n        }\n        visit[node] = 2;\n        return false;\n    }\npublic:\n    bool canFinish(int numCourses, vector<vector<int>>& prerequisites) {\n        vector<vector<int>> adj(numCourses);\n        for (auto& pre : prerequisites) {\n            adj[pre[1]].push_back(pre[0]);\n        }\n        \n        vector<int> visit(numCourses, 0); \n        for (int i = 0; i < numCourses; ++i) {\n            if (hasCycle(i, adj, visit)) return false;\n        }\n        return true;\n    }\n};\n\nint main() {\n    Solution sol;\n    vector<vector<int>> pre = {{1, 0}};\n    cout << "Can Finish Courses: " << (sol.canFinish(2, pre) ? "True" : "False") << " (Expected: True)" << endl;\n    return 0;\n}`,
      python: `from typing import List\n\nclass Solution:\n    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:\n        preMap = {i: [] for i in range(numCourses)}\n        for crs, pre in prerequisites:\n            preMap[crs].append(pre)\n            \n        visitSet = set()\n        \n        def dfs(crs):\n            if crs in visitSet:\n                return False\n            if preMap[crs] == []:\n                return True\n                \n            visitSet.add(crs)\n            for pre in preMap[crs]:\n                if not dfs(pre): return False\n            visitSet.remove(crs)\n            preMap[crs] = [] \n            return True\n            \n        for crs in range(numCourses):\n            if not dfs(crs):\n                return False\n        return True\n\nif __name__ == "__main__":\n    sol = Solution()\n    print(f"Can Finish: {sol.canFinish(2, [[1, 0]])} (Expected: True)")`
    },
    complexity: { time: "O(V + E)", space: "O(V + E)" },
    explanation: "This is a classical Cycle Detection in a Directed Graph. It can be solved using Topological Sort or DFS. We represent courses as nodes and prerequisites as directed edges. We maintain a cycle-detection visiting set (or 3-state vector). If during our traversal of neighbors we hit a node that is currently in the 'visiting' state, a cycle exists, so we return `false`."
  },
  {
    id: 49,
    name: "Course Schedule II",
    category: "Graphs",
    difficulty: "Medium",
    leetCodeUrl: "https://leetcode.com/problems/course-schedule-ii/",
    description: "There are a total of `numCourses` courses you have to take, labeled from `0` to `numCourses - 1`. You are given an array `prerequisites` where `prerequisites[i] = [ai, bi]` indicates that you **must** take course `bi` first if you want to take course `ai`.\n\nReturn *the ordering of courses you should take to finish all courses. If there are many valid answers, return **any** of them. If it is impossible to finish all courses, return **an empty array**.*",
    examples: [
      { input: "numCourses = 4, prerequisites = [[1,0],[2,0],[3,1],[3,2]]", output: "[0,2,1,3]" }
    ],
    constraints: ["`1 <= numCourses <= 2000`", "`0 <= prerequisites.length <= 5000`", "`prerequisites[i].length == 2`"],
    starterCode: {
      cpp: `#include <iostream>\n#include <vector>\n\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> findOrder(int numCourses, vector<vector<int>>& prerequisites) {\n        // Write code here\n        return {};\n    }\n};\n\nint main() {\n    Solution sol;\n    vector<vector<int>> pre = {{1, 0}};\n    vector<int> order = sol.findOrder(2, pre);\n    for (int x : order) cout << x << " ";\n    cout << endl;\n    return 0;\n}`,
      python: `from typing import List\n\nclass Solution:\n    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:\n        # Write code here\n        return []\n\nif __name__ == "__main__":\n    sol = Solution()\n    print(sol.findOrder(2, [[1, 0]]))`
    },
    solutions: {
      cpp: `#include <iostream>\n#include <vector>\n\nusing namespace std;\n\nclass Solution {\nprivate:\n    bool hasCycle(int node, vector<vector<int>>& adj, vector<int>& visit, vector<int>& order) {\n        if (visit[node] == 1) return true;\n        if (visit[node] == 2) return false;\n        \n        visit[node] = 1;\n        for (int neighbor : adj[node]) {\n            if (hasCycle(neighbor, adj, visit, order)) return true;\n        }\n        visit[node] = 2;\n        order.push_back(node); \n        return false;\n    }\npublic:\n    vector<int> findOrder(int numCourses, vector<vector<int>>& prerequisites) {\n        vector<vector<int>> adj(numCourses);\n        for (auto& pre : prerequisites) {\n            adj[pre[0]].push_back(pre[1]);\n        }\n        \n        vector<int> order;\n        vector<int> visit(numCourses, 0);\n        for (int i = 0; i < numCourses; ++i) {\n            if (hasCycle(i, adj, visit, order)) return {};\n        }\n        return order;\n    }\n};\n\nint main() {\n    Solution sol;\n    vector<vector<int>> pre = {{1, 0}, {2, 0}, {3, 1}, {3, 2}};\n    vector<int> order = sol.findOrder(4, pre);\n    cout << "Order: ";\n    for (int x : order) cout << x << " ";\n    cout << " (Expected: 0 2 1 3 or 0 1 2 3)" << endl;\n    return 0;\n}`,
      python: `from typing import List\n\nclass Solution:\n    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:\n        prereq = {c: [] for c in range(numCourses)}\n        for crs, pre in prerequisites:\n            prereq[crs].append(pre)\n            \n        output = []\n        visit, cycle = set(), set()\n        \n        def dfs(crs):\n            if crs in cycle:\n                return False\n            if crs in visit:\n                return True\n                \n            cycle.add(crs)\n            for pre in prereq[crs]:\n                if not dfs(pre):\n                    return False\n            cycle.remove(crs)\n            visit.add(crs)\n            output.append(crs)\n            return True\n            \n        for c in range(numCourses):\n            if not dfs(c):\n                return []\n        return output\n\nif __name__ == "__main__":\n    sol = Solution()\n    print(f"Order: {sol.findOrder(4, [[1, 0], [2, 0], [3, 1], [3, 2]])} (Expected: [0, 1, 2, 3] or [0, 2, 1, 3])")`
    },
    complexity: { time: "O(V + E)", space: "O(V + E)" },
    explanation: "This is a Topological Sort problem. We construct a directed graph where an edge runs from course to prerequisite. Using DFS, we check for cycles while building our ordering post-order (adding a node to our list once all its prerequisites have been fully traversed). If a cycle is detected, we return an empty array."
  }
];
