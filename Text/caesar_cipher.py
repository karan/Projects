"""
Caesar Cipher - Enter the cipher number and the program will "encrypt" them with
the Caesar cipher (a.k.a. ROT #). Type the word "exit" when you're finished.
"""

while True:
    try:
        cipher = int(raw_input("Enter the cipher number: "))
        break
    except ValueError:
        print "I need a valid integer, please."

print "Enter the text to be encoded."
print "Enter \"exit\" to leave."

if __name__ == '__main__':
    while True:
        text = raw_input("> ")
        encoded = []
        
        if text.lower() == "exit":
            break
        
        for letter in text:
            if letter.isalpha():
                is_upper = False
                
                if letter == letter.upper():
                    is_upper = True
                    letter = letter.lower()

                value = (ord(letter) - 97 + cipher) % 26
                if is_upper:
                    value -= 32
                     
                encoded.append(chr(value + 97))
            else:
                encoded.append(letter)
                
            print ''.join(encoded)
