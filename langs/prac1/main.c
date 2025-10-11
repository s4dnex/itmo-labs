#include <stdio.h>
#include <assert.h>

int isUppercaseLetter(char c) {
	return (c >= 'A' && c <= 'Z');
}

int isLowercaseLetter(char c) {
	return (c >= 'a' && c <= 'z');
}

void cipher(char text[], int shift) {
	for (int i = 0; text[i] != '\0'; i++) {
		if (isUppercaseLetter(text[i])) {
			text[i] = (text[i] - 'A' + shift + 26) % 26 + 'A';
		}
		else if (isLowercaseLetter(text[i])) {
			text[i] = (text[i] - 'a' + shift + 26) % 26 + 'a';
		}
	}
	return;
}

void decipher(char text[], int shift) {
	cipher(text, -shift);
}

int main(int argc, char* argv[])
{
	char text[] = "Hello, World, xyz";
	printf("Original: %s\n", text);
	int shift = 12;
	assert(shift >= 0 && shift <= 26);
	cipher(text, shift);
	printf("Encrypted (shift=%d): %s\n", shift, text);
	decipher(text, shift);
	printf("Decrypted: %s\n", text);
	return 0;
}