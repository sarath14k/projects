Convert 0x1256 to 0x5612 using bitwise operator
================================================

#include <iostream>

    int main()
{
    unsigned short num = 0x1256; // Original number (16-bit)

    // Step 1: Extract higher-order byte (0x12)
    unsigned short higherByte = (num & 0xFF00) >> 8;

    // Step 2: Extract lower-order byte (0x56)
    unsigned short lowerByte = (num & 0x00FF);

    // Step 3: Shift the lower byte to the higher byte position, and higher byte to lower position
    unsigned short swapped = (lowerByte << 8) | higherByte;

    // Output the original and swapped value in hexadecimal
    std::cout << "Original: 0x" << std::hex << num << std::endl;
    std::cout << "Swapped:  0x" << std::hex << swapped << std::endl;

    return 0;
}

Extract the higher-order byte (0x12) by shifting the number 8 bits to the right.

Extract the lower-order byte (0x56) using bitwise AND with 0x00FF.

Shift the lower-order byte to the higher-order position and the higher-order byte to the lower-order 
position.

Combine the results using bitwise OR (|).

AND (&): Returns 1 if both corresponding bits are 1.
OR (|): Returns 1 if at least one of the corresponding bits is 1.
XOR (^): Returns 1 if the corresponding bits are different.
NOT (~): Flips the bits (changes 1 to 0 and vice versa).
Left Shift (<<): Shifts the bits to the left by a specified number of positions 
(equivalent to multiplying by powers of 2).

Right Shift (>>): Shifts the bits to the right by a specified number of positions 
(equivalent to dividing by powers of 2).

==============================================
Check if a Number is Odd or Even

A number is odd if its least significant bit (LSB) is 1, and it's even if the LSB is 0.

if (n & 1) {
    std::cout << "Odd";
} else {
    std::cout << "Even";
}
