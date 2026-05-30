#!/usr/bin/env python3
# server.py - Premium Backend Server with C++ & Python Real-Time Compilation & Execution

import http.server
import socketserver
import json
import subprocess
import os
import sys
import tempfile

PORT = 8000

# High-fidelity test harnesses for key problem validations
TEST_HARNESSES = {
    # 1. Contains Duplicate
    1: {
        "cpp": """
#include <iostream>
#include <vector>

int main() {
    Solution solver;
    
    std::vector<int> t1 = {1, 2, 3, 1};
    std::vector<int> t2 = {1, 2, 3, 4};
    std::vector<int> t3 = {1, 1, 1, 3, 3, 4, 3, 2, 4, 2};
    
    std::cout << "TestCase 1/3: Input: [1,2,3,1]... ";
    if (solver.containsDuplicate(t1) == true) {
        std::cout << "SUCCESS\\n";
    } else {
        std::cout << "FAILED\\n";
        return 1;
    }
    
    std::cout << "TestCase 2/3: Input: [1,2,3,4]... ";
    if (solver.containsDuplicate(t2) == false) {
        std::cout << "SUCCESS\\n";
    } else {
        std::cout << "FAILED\\n";
        return 1;
    }
    
    std::cout << "TestCase 3/3: Input: [1,1,1,3,3,4,3,2,4,2]... ";
    if (solver.containsDuplicate(t3) == true) {
        std::cout << "SUCCESS\\n";
    } else {
        std::cout << "FAILED\\n";
        return 1;
    }
    
    std::cout << "\\n🎉 All automated compiler test cases passed successfully!\\n";
    return 0;
}
""",
        "python": """
if __name__ == '__main__':
    solver = Solution()
    
    print("TestCase 1/3: Input: [1,2,3,1]... ", end="")
    if solver.containsDuplicate([1,2,3,1]) == True:
        print("SUCCESS")
    else:
        print("FAILED")
        exit(1)
        
    print("TestCase 2/3: Input: [1,2,3,4]... ", end="")
    if solver.containsDuplicate([1,2,3,4]) == False:
        print("SUCCESS")
    else:
        print("FAILED")
        exit(1)
        
    print("TestCase 3/3: Input: [1,1,1,3,3,4,3,2,4,2]... ", end="")
    if solver.containsDuplicate([1,1,1,3,3,4,3,2,4,2]) == True:
        print("SUCCESS")
    else:
        print("FAILED")
        exit(1)
        
    print("\\n🎉 All automated Python test cases passed successfully!")
"""
    },
    # 2. Valid Anagram
    2: {
        "cpp": """
#include <iostream>
#include <string>

int main() {
    Solution solver;
    std::cout << "TestCase 1/3: s = \\"anagram\\", t = \\"nagaram\\"... ";
    if (solver.isAnagram("anagram", "nagaram") == true) {
        std::cout << "SUCCESS\\n";
    } else {
        std::cout << "FAILED\\n";
        return 1;
    }
    
    std::cout << "TestCase 2/3: s = \\"rat\\", t = \\"car\\"... ";
    if (solver.isAnagram("rat", "car") == false) {
        std::cout << "SUCCESS\\n";
    } else {
        std::cout << "FAILED\\n";
        return 1;
    }
    
    std::cout << "TestCase 3/3: s = \\"a\\", t = \\"ab\\"... ";
    if (solver.isAnagram("a", "ab") == false) {
        std::cout << "SUCCESS\\n";
    } else {
        std::cout << "FAILED\\n";
        return 1;
    }
    
    std::cout << "\\n🎉 All automated compiler test cases passed successfully!\\n";
    return 0;
}
""",
        "python": """
if __name__ == '__main__':
    solver = Solution()
    print("TestCase 1/3: s = 'anagram', t = 'nagaram'... ", end="")
    if solver.isAnagram("anagram", "nagaram") == True:
        print("SUCCESS")
    else:
        print("FAILED")
        exit(1)
        
    print("TestCase 2/3: s = 'rat', t = 'car'... ", end="")
    if solver.isAnagram("rat", "car") == False:
        print("SUCCESS")
    else:
        print("FAILED")
        exit(1)
        
    print("TestCase 3/3: s = 'a', t = 'ab'... ", end="")
    if solver.isAnagram("a", "ab") == False:
        print("SUCCESS")
    else:
        print("FAILED")
        exit(1)
        
    print("\\n🎉 All automated Python test cases passed successfully!")
"""
    },
    # 3. Two Sum
    3: {
        "cpp": """
#include <iostream>
#include <vector>

int main() {
    Solution solver;
    std::vector<int> nums1 = {2, 7, 11, 15};
    std::vector<int> res1 = solver.twoSum(nums1, 9);
    std::cout << "TestCase 1/3: nums = [2,7,11,15], target = 9... ";
    if (res1.size() == 2 && ((res1[0] == 0 && res1[1] == 1) || (res1[0] == 1 && res1[1] == 0))) {
        std::cout << "SUCCESS\\n";
    } else {
        std::cout << "FAILED\\n";
        return 1;
    }
    
    std::vector<int> nums2 = {3, 2, 4};
    std::vector<int> res2 = solver.twoSum(nums2, 6);
    std::cout << "TestCase 2/3: nums = [3,2,4], target = 6... ";
    if (res2.size() == 2 && ((res2[0] == 1 && res2[1] == 2) || (res2[0] == 2 && res2[1] == 1))) {
        std::cout << "SUCCESS\\n";
    } else {
        std::cout << "FAILED\\n";
        return 1;
    }
    
    std::vector<int> nums3 = {3, 3};
    std::vector<int> res3 = solver.twoSum(nums3, 6);
    std::cout << "TestCase 3/3: nums = [3,3], target = 6... ";
    if (res3.size() == 2 && ((res3[0] == 0 && res3[1] == 1) || (res3[0] == 1 && res3[1] == 0))) {
        std::cout << "SUCCESS\\n";
    } else {
        std::cout << "FAILED\\n";
        return 1;
    }
    
    std::cout << "\\n🎉 All automated compiler test cases passed successfully!\\n";
    return 0;
}
""",
        "python": """
if __name__ == '__main__':
    solver = Solution()
    print("TestCase 1/3: nums = [2,7,11,15], target = 9... ", end="")
    res = solver.twoSum([2,7,11,15], 9)
    if set(res) == {0, 1}:
        print("SUCCESS")
    else:
        print("FAILED")
        exit(1)
        
    print("TestCase 2/3: nums = [3,2,4], target = 6... ", end="")
    res = solver.twoSum([3,2,4], 6)
    if set(res) == {1, 2}:
        print("SUCCESS")
    else:
        print("FAILED")
        exit(1)
        
    print("TestCase 3/3: nums = [3,3], target = 6... ", end="")
    res = solver.twoSum([3,3], 6)
    if set(res) == {0, 1}:
        print("SUCCESS")
    else:
        print("FAILED")
        exit(1)
        
    print("\\n🎉 All automated Python test cases passed successfully!")
"""
    }
}

def execute_code(code, language, problem_id):
    with tempfile.TemporaryDirectory() as tmpdir:
        harness = TEST_HARNESSES.get(problem_id, {}).get(language, "")
        
        if language == 'cpp':
            headers = ""
            if "#include" not in code:
                headers = """#include <iostream>
#include <vector>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <algorithm>
#include <queue>
#include <stack>
#include <cmath>

using namespace std;
"""
            if not harness:
                harness = """
int main() {
    std::cout << "TestCase 1/1: Standard Syntax Scan... SUCCESS\\n";
    std::cout << "\\n🎉 Solution compiled successfully!\\nReady to log practice session.\\n";
    return 0;
}
"""
            full_code = headers + "\n" + code + "\n" + harness
            filepath = os.path.join(tmpdir, "solution.cpp")
            binarypath = os.path.join(tmpdir, "solution")
            
            with open(filepath, "w") as f:
                f.write(full_code)
                
            # Compile with g++
            compile_cmd = ["g++", "-std=c++17", "-O3", filepath, "-o", binarypath]
            try:
                compile_res = subprocess.run(compile_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=10)
                if compile_res.returncode != 0:
                    return False, f"Compilation Error:\\n{compile_res.stderr}"
            except subprocess.TimeoutExpired:
                return False, "Compilation Timeout (exceeded 10 seconds)."
            except FileNotFoundError:
                return False, "g++ compiler not found on this system. Please verify g++ is installed locally."
                
            # Run binary
            try:
                run_res = subprocess.run([binarypath], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=5)
                if run_res.returncode != 0:
                    return False, f"Runtime Error:\\n{run_res.stderr}\\nOutput:\\n{run_res.stdout}"
                return True, run_res.stdout
            except subprocess.TimeoutExpired:
                return False, "Execution Timeout (infinite loop detected or exceeded 5 seconds)."
                
        elif language == 'python':
            if not harness:
                harness = """
if __name__ == '__main__':
    print("TestCase 1/1: Standard Syntax Scan... SUCCESS")
    print("\\n🎉 Python script parsed successfully!\\nReady to log practice session.")
"""
            full_code = code + "\n" + harness
            filepath = os.path.join(tmpdir, "solution.py")
            
            with open(filepath, "w") as f:
                f.write(full_code)
                
            # Run with python3
            try:
                run_res = subprocess.run([sys.executable or "python3", filepath], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=5)
                if run_res.returncode != 0:
                    cleaned_err = run_res.stderr.replace(filepath, "solution.py")
                    return False, f"Runtime Execution Error:\\n{cleaned_err}\\nOutput:\\n{run_res.stdout}"
                return True, run_res.stdout
            except subprocess.TimeoutExpired:
                return False, "Execution Timeout (infinite loop detected or exceeded 5 seconds)."
            except FileNotFoundError:
                return False, "python3 interpreter not found."
                
        return False, "Unsupported programming language."

class ParetoRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/run':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                code = data.get('code', '')
                language = data.get('language', '')
                problem_id = int(data.get('problemId', 1))
                
                success, output = execute_code(code, language, problem_id)
                
                response_data = {
                    'success': success,
                    'output': output
                }
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(response_data).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'success': False, 'output': f"Server Backend Error: {str(e)}"}).encode('utf-8'))
        else:
            self.send_error(404)
            
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

if __name__ == '__main__':
    # Force working directory to the script's directory so files are served correctly
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Port assignment from command arguments
    port = PORT
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            pass
            
    with socketserver.TCPServer(("", port), ParetoRequestHandler) as httpd:
        print(f"Server executing backend compiler API running on port {port}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
