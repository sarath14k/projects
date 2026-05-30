public class CompareStringUsingXOR {

    /**
     * Warning: This logic will return true for ANAGRAMS (e.g., "abc" and "cba") 
     * because XOR is commutative and associative. It does NOT strictly check 
     * character-by-character sequence equality. 
     * 
     * For example: 'a'^'b' ^ 'b'^'a' = 0
     */
    public static boolean compareStringsUsingXOR(String str1, String str2) {
        // If lengths are different, strings are not equal
        if (str1.length() != str2.length()) {
            return false;
        }

        // XOR all characters of the strings
        int result = 0;
        for (int i = 0; i < str1.length(); ++i) {
            result ^= (str1.charAt(i) ^ str2.charAt(i));
        }

        // If result is 0, strings might be equal (or anagrams); otherwise, they are not
        return result == 0;
    }

    public static void main(String[] args) {
        String str1 = "hello";
        String str2 = "hello";
        String str3 = "world";
        String str4 = "olleh"; // Anagram of hello

        if (compareStringsUsingXOR(str1, str2)) {
            System.out.println("str1 and str2 are equal");
        } else {
            System.out.println("str1 and str2 are not equal");
        }

        if (compareStringsUsingXOR(str1, str3)) {
            System.out.println("str1 and str3 are equal");
        } else {
            System.out.println("str1 and str3 are not equal");
        }

        // Demonstrating the logic flaw of XOR comparison
        if (compareStringsUsingXOR(str1, str4)) {
            System.out.println("str1 and str4 (anagram) are evaluated as EQUAL (This is the XOR bug!)");
        } else {
            System.out.println("str1 and str4 are not equal");
        }
    }
}
