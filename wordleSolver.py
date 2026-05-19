from collections import Counter

guess = ""
feedback = ""
guess_list=[]
with open('5letterWords.txt') as f:
    for line in f:
        guess_list.append(line.strip())



def filter(temp_list, prevGuess, result):
    keepers = []

    for word in temp_list:
        ok = True
        
        for i in range(5):
            if result[i] == "g":
                if word[i] != prevGuess[i]:
                    ok = False
                    break
            elif result[i] == "y":
                if prevGuess[i] == word[i] or prevGuess[i] not in word:
                    ok = False
                    break
            elif result[i] == "x":
                if prevGuess[i] in word:
                    ok = False
                    break
        
        if ok:
            keepers.append(word)

    return keepers
#-----------------------declaring letter scores-----------------------

letterScores = {"a":[5.8,18.1,9.3,8.9,6],"b":[6.8,.7,2.6,1.9,.5],"c":[6.5,.7,2.6,1.9,.5],
                "d":[4.9,.7,3.1,3.7,5.9],"e":[2.2,12.5,6.7,17,11.7],"f":[4.3,.3,1.4,1.7,.6],
                "g":[4.6,.6,2.9,3.3,1.2],"h":[3.6,4.1,1,1.9,2.9],"i":[1.2,10.8,7.9,7,2.6],
                "j":[1.5,.1,.4,.3,.1],"k":[2.9,.8,2.2,3.8,2.1],"l":[4.2,5.2,6.5,5.9,3.6],
                "m":[6.4,1.4,3.9,3,1.5],"n":[3.1,2.6,7.5,6,4.2],"o":[2.4,16.2,7.5,5.6,3.4],
                "p":[7.6,1.7,2.9,3.1,1.1],"q":[.7,.1,.1,.1,.1],"r":[5.4,6.9,9.1,5.5,5],
                "s":[11.2,.8,4.1,4,30],"t":[6,1.7,5,7,5.4],"u":[1.5,9.2,5.1,3.3,.7],
                "v":[2,.4,1.9,1,.1],"w":[3,1.2,2.1,1,.5],"x":[.1,.4,1,.1,.6],
                "y":[1.4,2.1,1.7,.8,10.4],"z":[.8,.2,1.1,1,.3]}

#-----------------------score each word -----------------------------

def scoreWord(word: str,
              scores: dict[str, list[float]],   #5 weights per letter
              repeat_factor: float = 0.6) -> float:
    running_total = 0.0
    seen = set()                                #track letters already scored once

    for idx, ch in enumerate(word.lower()):   
        base_weight = scores[ch][idx]           
        running_total += base_weight if ch not in seen else base_weight * repeat_factor
        seen.add(ch)

    return running_total


wordScores = {w: scoreWord(w, letterScores) for w in guess_list}

def pickTopWord(scores):
    highWord = max(scores, key=scores.get)
    return highWord, scores[highWord]



#----------------------mainLoop--------------------------------------

tempScore = {w:scoreWord(w, letterScores) for w in guess_list}
firstWord, point = pickTopWord(tempScore)



print("\nThe calculated best word is: ",firstWord)
print("Below you enter in the word you tried and the feedback you recieved")

for guesses in range(6):

    while True:
        guess = input("\nword: ").lower()
        print("g-green, y-yellow, x-wrong/grey")

        # make sure both strings are exactly five alphabetic characters
        if len(guess) != 5 or not guess.isalpha():
            print("Make sure the word you enter and the feedback are both 5 characters long")
            continue          
        break            
    feedback = input("Enter the results of your word:")     

    if feedback == "ggggg":
        print("Nice Job")
        break
    else:
        guess_list = filter(guess_list, guess, feedback)
        wordScores={w:scoreWord(w, letterScores) for w in guess_list}
        topWord, points=pickTopWord(wordScores)
        print("The best guess would be: ",topWord)

