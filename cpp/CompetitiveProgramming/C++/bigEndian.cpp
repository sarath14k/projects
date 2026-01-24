#include <iostream>
using namespace std;

// Function to check if system is little-endian or big-endian
bool isLittleEndian()
{
    unsigned int num = 1;
    // If the least significant byte is stored at the lowest memory address, it's little-endian
    return (*(char *)&num == 1);
}

// Function to display byte order (for educational purposes)
void showByteOrder(unsigned int num)
{
    unsigned char *bytePointer = (unsigned char *)&num;
    cout << "Byte order in memory: ";
    for (int i = 0; i < sizeof(num); ++i)
    {
        printf("%02x ", bytePointer[i]);
    }
    cout << endl;
}

int main()
{
    unsigned int num = 0x12345678;

    cout << "Original number in hex: 0x" << hex << num << endl;

    if (isLittleEndian())
    {
        cout << "System is Little Endian" << endl;
    }
    else
    {
        cout << "System is Big Endian" << endl;
    }

    // Display the byte order
    showByteOrder(num);

    return 0;
}
