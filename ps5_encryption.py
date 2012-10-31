# 6.00x Problem Set 5
#
# Part 1 - HAIL CAESAR!

import string
import random

WORDLIST_FILENAME = "words.txt"

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)
def loadWords():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print "Loading word list from file..."
    inFile = open(WORDLIST_FILENAME, 'r')
    wordList = inFile.read().split()
    print "  ", len(wordList), "words loaded."
    return wordList

def isWord(wordList, word):
    """
    Determines if word is a valid word.

    wordList: list of words in the dictionary.
    word: a possible word.
    returns True if word is in wordList.

    Example:
    >>> isWord(wordList, 'bat') returns
    True
    >>> isWord(wordList, 'asdf') returns
    False
    """
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\\:;'<>?,./\"")
    return word in wordList

def randomWord(wordList):
    """
    Returns a random word.

    wordList: list of words  
    returns: a word from wordList at random
    """
    return random.choice(wordList)

def randomString(wordList, n):
    """
    Returns a string containing n random words from wordList

    wordList: list of words
    returns: a string of random words separated by spaces.
    """
    return " ".join([randomWord(wordList) for _ in range(n)])

def randomScrambled(wordList, n):
    """
    Generates a test string by generating an n-word random string
    and encrypting it with a sequence of random shifts.

    wordList: list of words
    n: number of random words to generate and scamble
    returns: a scrambled string of n random words

    NOTE:
    This function will ONLY work once you have completed your
    implementation of applyShifts!
    """
    s = randomString(wordList, n) + " "
    shifts = [(i, random.randint(0, 25)) for i in range(len(s)) if s[i-1] == ' ']
    return applyShifts(s, shifts)[:-1]

def getStoryString():
    """
    Returns a story in encrypted text.
    """
    return open("story.txt", "r").read()


# (end of helper code)
# -----------------------------------


#
# Problem 1: Encryption
#
def buildCoder(shift):
    """
    Returns a dict that can apply a Caesar cipher to a letter.
    The cipher is defined by the shift value. Ignores non-letter characters
    like punctuation, numbers and spaces.

    shift: 0 <= int < 26
    returns: dict
    """
    lowerC = list(string.ascii_lowercase)
    upperC = list(string.ascii_uppercase)

    coded_letters = {}
    lowerCDict, upperCDict = {}, {}
    iLower, newLower = 0, 0
    iUpper, newUpper = 0, 0
    
    for letters in lowerC:
        if iLower < (len(lowerC) - shift):
            lowerCDict[letters] = lowerC[iLower + shift]
            iLower += 1
        else:
            lowerCDict[letters] = lowerC[newLower]
            newLower += 1
    for letters in upperC:
        if iUpper < (len(upperC) - shift):
            upperCDict[letters] = upperC[iUpper + shift]
            iUpper += 1
        else:
            upperCDict[letters] = upperC[newUpper]
            newUpper +=1
            
    coded_letters = dict(lowerCDict.items() + upperCDict.items())

    return coded_letters           

def applyCoder(text, coder):
    """
    Applies the coder to the text. Returns the encoded text.

    text: string
    coder: dict with mappings of characters to shifted characters
    returns: text after mapping coder chars to original text
    """
    textList = list(text)
    codedList = []  
    for char in textList:
        if char in coder:
            codedList.append(coder[char])
        else:
            codedList.append(char)
    final = ''.join(codedList)
    return final
            
    

def applyShift(text, shift):
    """
    Given a text, returns a new text Caesar shifted by the given shift
    offset. Lower case letters should remain lower case, upper case
    letters should remain upper case, and all other punctuation should
    stay as it is.

    text: string to apply the shift to
    shift: amount to shift the text (0 <= int < 26)
    returns: text after being shifted by specified amount.
    """
    ### TODO.
    ### HINT: This is a wrapper function.
    return applyCoder(text, buildCoder(shift))

#
# Problem 2: Decryption
#
def findBestShift(wordList, text):
    """
    Finds a shift key that can decrypt the encoded text.

    text: string
    returns: 0 <= int < 26
    """
    max_real_words = 0
    best_shift = 0
    table = string.maketrans("","")
    
    for i in range(0, 26):
        counter = 0
        text_shift = applyShift(text, i)

        shifted_list = text_shift.translate(table, string.punctuation).split()

        for word in shifted_list:
            if word in wordList:
                counter += 1
            
        if counter > max_real_words:
            max_real_words = counter
            best_shift = i

    return best_shift




def decryptStory():
    """
    Using the methods you created in this problem set,
    decrypt the story given by the function getStoryString().
    Use the functions getStoryString and loadWords to get the
    raw data you need.

    returns: string - story in plain text
    """
    story = getStoryString()

    shift = findBestShift(wordList, story)

    decrypted_story = applyShift(story, shift)
    return decrypted_story # Remove this comment when you code the function

#
# Build data structures used for entire session and run encryption
#

if __name__ == '__main__':
    wordList = loadWords()
    decryptStory()
