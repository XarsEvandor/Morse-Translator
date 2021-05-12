import sys
import subprocess
import platform

# use pip to install pynput:
subprocess.check_call([sys.executable, '-m', 'pip', 'install',
                       'pynput'])

from pynput.keyboard import Listener, Key


morse_table = {'A': '.-', 'B': '-...',
                    'C': '-.-.', 'D': '-..', 'E': '.',
                    'F': '..-.', 'G': '--.', 'H': '....',
                    'I': '..', 'J': '.---', 'K': '-.-',
                    'L': '.-..', 'M': '--', 'N': '-.',
                    'O': '---', 'P': '.--.', 'Q': '--.-',
                    'R': '.-.', 'S': '...', 'T': '-',
                    'U': '..-', 'V': '...-', 'W': '.--',
                    'X': '-..-', 'Y': '-.--', 'Z': '--..',
                    '1': '.----', '2': '..---', '3': '...--',
                    '4': '....-', '5': '.....', '6': '-....',
                    '7': '--...', '8': '---..', '9': '----.',
                    '0': '-----', ',': '--..--', '.': '.-.-.-',
                    '?': '..--..', '/': '-..-.', '-': '-....-',
                    '(': '-.--.', ')': '-.--.-', '!': '-.-.--'}

char_list = []
morse_list = []

print("Welcome to the real-time morse encryptor. Please start typing to begin.\nPress esc to stop.")

#This method checks for the platform the program is run on and it runs code that clears the terminal.
def clear_screen():
    # thanks to: https://stackoverflow.com/a/23075152/2923937
    if platform.system() == "Windows":
        subprocess.Popen("cls", shell=True).communicate()
    else:
        print("\033c", end="")


def morse_encryptor(key):
    if hasattr(key, 'char'):  # Write the character pressed if available

        #When a character is pressed, the key will be saved in a list, the screen will refresh and the contents of the list will be displayed.
        #Since we only pop entries from the list when the backspace is pressed, the list will include all characters typed and display them next to each other.

        #Some keyboard inputs conflict with the upper method. This is to prevent the program from crashing in such case.
        try:
            input_char = key.char.upper()
        except AttributeError:
            input_char = key.char
        
        char_list.append(input_char)

        clear_screen()
        for char in char_list:
            print(char, end="")
        sys.stdout.flush()

    if hasattr(key, 'char'):  # Write the character pressed in morse code
        #This is to avoid errors when ctr+'char' is pressed. Since ctr is not a char the input ctr+"char" returns a NoneType value and it cannot be concated with a space.
        #Please beware as ctrl commands might still affect your IDE if you are running the script in an emulated terminal and not a separate window.
        try:
            morse_list.append(morse_table.get(input_char) + " ")
        except TypeError:
            char_list.pop()
        print("\n\n")

        for char in morse_list:
            print(char, end="")
        sys.stdout.flush()

    elif key == Key.space:  # If space was pressed, write a space, in morse code the separator between words is marked by 7 time units, here we represent it with a straight line
        char_list.append(" ")
        morse_list.append(" | ")
        clear_screen()
        
        for char in char_list:
            print(char, end="")

        print("\n\n")

        for char in morse_list:
            print(char, end="")

        sys.stdout.flush()

    elif key == Key.enter:  # If enter was pressed, write a new line
        char_list.append("\n")
        morse_list.append("\n")
        clear_screen()

        for char in char_list:
            print(char, end="")

        print("\n\n")

        for char in morse_list:
            print(char, end="")

        sys.stdout.flush()

    elif key == Key.tab:  # If tab was pressed, write a tab
        char_list.append("\t")
        morse_list.append("\t")
        clear_screen()
        
        for char in char_list:
            print(char, end="")

        print("\n\n")

        for char in morse_list:
            print(char, end="")

        sys.stdout.flush()

    elif key == Key.backspace:  # If backspace is pressed, remove the last input
        # We use try-except to avoid index errors if you try to pop from an empty list,
        # however we do not want to display an error message.
        try:
            char_list.pop()
        except IndexError:
            None

        try:
            morse_list.pop()
        except IndexError:
            None

        clear_screen()

        for char in char_list:
            print(char, end="")

        print("\n\n")

        for char in morse_list:
            print(char, end="")

        sys.stdout.flush()
    
    elif key == Key.esc:
        clear_screen()
        print("\nThank you!\n\n-.....--.-.- -.-----..--.-.--")
        exit()

    else:  # If anything else was pressed, write [<key_name>]
        print('[' + key.name + ']', end="")
        sys.stdout.flush()

with Listener(on_press=morse_encryptor) as listener:
    listener.join()

