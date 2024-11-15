#include <iostream>
#include <algorithm>
using namespace std;

bool isContain(int arr[], int size, int key)
{
    for (int z = 0; z < size; z++)
    {
        if (arr[z] == key)
        {
            return true;
        }
    }
    return false;
}

int smallestCommon(int a[], int b[], int c[], int N, int M, int O)
{

    sort(a, a + N);

    int smallestCommon = a[0];

    for (int i = 0; i < N; i++)
    {

        int key = a[i];

        if ((isContain(b, M, key)) && (isContain(c, O, key)))
        {
            smallestCommon = key;
            return smallestCommon;
        }
    }
    return smallestCommon;
}

int main()
{
    int array1[] = {10, 50, 35, 5, 78, 2};
    int size1 = sizeof(array1) / sizeof(array1[0]);

    int array2[] = {2, 44, 21, 35, 110, 58, 10};
    int size2 = sizeof(array2) / sizeof(array2[0]);

    int array3[] = {10, 65, 88, 2, 5, 78};
    int size3 = sizeof(array3) / sizeof(array3[0]);

    int res = smallestCommon(array1, array2, array3, size1, size2, size3);

    cout << "smallestCommon : " << res << endl;
    return 0;
}
