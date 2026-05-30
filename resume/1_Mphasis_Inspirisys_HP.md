# Interview Questions & Answers: Mphasis & Inspirisys (HP Projects)

## 1. "You mentioned migrating HP Windows services to C++17/C++20. Can you explain why this was necessary and what specific C++17/20 features you utilized?"
**Answer Framework:**
*   **Context:** The legacy code was stuck on older standards (UAP/Win32), which lacked modern safety and concurrency features, making maintenance difficult.
*   **Action:** I led the migration to C++17/C++20. I refactored raw pointers to smart pointers (`std::unique_ptr`, `std::shared_ptr`) to eliminate memory leaks. I leveraged C++17's `std::optional` for better error handling without relying on magic values, and `std::string_view` to optimize string passing without deep copies. 
*   **Result:** This modernized the codebase, making it significantly safer, faster, and aligned with current enterprise standards.

## 2. "How did you manage to preserve full Git commit history while decoupling repositories?"
**Answer Framework:**
*   **Context:** Moving a sub-project out of a massive monorepo into its own repository often loses the historical context of who changed what and why.
*   **Action:** I used advanced git commands like `git filter-repo` (or `git subtree split`) to surgically extract the specific directories for Analytics, DeviceDetection, and UserInfo. This rewrote the history to only include commits relevant to those files.
*   **Result:** We successfully decoupled the repositories into the new NCE org without losing a single relevant commit, ensuring developers could still `git blame` and understand the legacy context.

## 3. "Tell me about your testing strategy. How did you achieve a 100% pass rate and what is the `_RequiresPrivilege` tag?"
**Answer Framework:**
*   **Context:** Our test suites were unstable and failing randomly in CI/CD because some tests required Administrator privileges (interacting directly with Windows systems/drivers) while others did not.
*   **Action:** I completely reorganized the test suites into distinct Unit, Integration, and System layers using **VSTest** and **Google Test (gtest)**. I identified the tests failing due to permission issues and introduced a custom tagging mechanism `_RequiresPrivilege`. I then configured the Azure DevOps pipeline to only run those specific tagged tests on runner agents that were explicitly granted Admin rights.
*   **Result:** This stopped the false-negative failures, stabilizing the pipeline and achieving a 100% pass rate across DeviceDetection (85/85) and CustomTrigger (37/37).

## 4. "At Inspirisys, you migrated an HP PCL6 printer driver from VS 2013 to VS 2022 and integrated arm64. What were the biggest challenges?"
**Answer Framework:**
*   **Context:** A 9-year jump in compiler versions (VS 2013 to 2022) means massive changes in the MSVC compiler, strictness, and deprecated Windows APIs.
*   **Action:** I systematically updated project files, resolved hundreds of strict C++ conformance errors introduced by the modern compiler, and updated legacy linked libraries. For the arm64 integration, I had to ensure the codebase was architecture-agnostic, fixing pointer-to-integer cast warnings that behave differently on ARM vs x86.
*   **Result:** The driver successfully compiled and ran natively on modern ARM-based Windows machines, future-proofing HP's Universal Printer Drivers.
