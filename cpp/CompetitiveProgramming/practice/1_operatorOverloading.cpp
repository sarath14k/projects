#include <iostream>
using namespace std;

class Point {
	public:
		int x, y;
		Point operator+(const Point& other) {
			Point temp;
			temp.x = this->x + other.x;
			temp.y = this->y + other.y;
			return temp;
		}
};

int main() {
	Point p1; p1.x = 10; p1.y = 20;
	Point p2; p2.x = 5; p2.y = 5;

	// Usese the overload operator
	Point p3 = p1 + p2;
	cout << "New point: " << p3.x << ", " << p3.y << '\n';
	return 0;
}
