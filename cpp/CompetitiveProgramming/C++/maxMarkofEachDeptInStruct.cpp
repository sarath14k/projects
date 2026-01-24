#include <iostream>
#include <vector>
#include <unordered_map>
#include <string>
#include <algorithm>

struct Student
{
    int studentId;
    std::string studentDept;
    int studentMarks;
};

void findMaxMarksInEachDept(const std::vector<Student> &students)
{
    std::unordered_map<std::string, int> deptMaxMarks;

    for (const auto &student : students)
    {
        if (deptMaxMarks.find(student.studentDept) == deptMaxMarks.end())
        {
            deptMaxMarks[student.studentDept] = student.studentMarks;
        }
        else
        {
            deptMaxMarks[student.studentDept] = std::max(deptMaxMarks[student.studentDept], student.studentMarks);
        }
    }

    // Print the results
    for (const auto &dept : deptMaxMarks)
    {
        std::cout << "Department: " << dept.first << ", Max Marks: " << dept.second << std::endl;
    }
}

int main()
{
    std::vector<Student> students = {
        {1, "CS", 85},
        {2, "EE", 90},
        {3, "CS", 95},
        {4, "ME", 80},
        {5, "EE", 88},
        {6, "CS", 78},
        {7, "ME", 92}};

    findMaxMarksInEachDept(students);

    return 0;
}
