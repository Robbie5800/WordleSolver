#solving logic for flask version

#load word list
INITIAL_GUESS_LIST = []
try:
    with open('5letterWords.txt') as f:
        for line in f:
            INITIAL_GUESS_LIST.append(line.strip().lower())
except FileNotFoundError:
    # fallback for missing file
    INITIAL_GUESS_LIST = ["apple", "react", "words", "solve", "green", "about"]

# ----------------- Letter Scoring Weights -----------------
letterScores = {
    "a":[5.8,18.1,9.3,8.9,6],"b":[6.8,.7,2.6,1.9,.5],"c":[6.5,.7,2.6,1.9,.5],
    "d":[4.9,.7,3.1,3.7,5.9],"e":[2.2,12.5,6.7,17,11.7],"f":[4.3,.3,1.4,1.7,.6],
    "g":[4.6,.6,2.9,3.3,1.2],"h":[3.6,4.1,1,1.9,2.9],"i":[1.2,10.8,7.9,7,2.6],
    "j":[1.5,.1,.4,.3,.1],"k":[2.9,.8,2.2,3.8,2.1],"l":[4.2,5.2,6.5,5.9,3.6],
    "m":[6.4,1.4,3.9,3,1.5],"n":[3.1,2.6,7.5,6,4.2],"o":[2.4,16.2,7.5,5.6,3.4],
    "p":[7.6,1.7,2.9,3.1,1.1],"q":[.7,.1,.1,.1,.1],"r":[5.4,6.9,9.1,5.5,5],
    "s":[11.2,.8,4.1,4,30],"t":[6,1.7,5,7,5.4],"u":[1.5,9.2,5.1,3.3,.7],
    "v":[2,.4,1.9,1,.1],"w":[3,1.2,2.1,1,.5],"x":[.1,.4,1,.1,.6],
    "y":[1.4,2.1,1.7,.8,10.4],"z":[.8,.2,1.1,1,.3]
}

def filter_words(temp_list, prevGuess, result):
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

def scoreWord(word: str, scores: dict, repeat_factor: float = 0.6) -> float:
    running_total = 0.0
    seen = set()
    for idx, ch in enumerate(word.lower()):   
        if ch in scores:
            base_weight = scores[ch][idx]   
            running_total += base_weight if ch not in seen else base_weight * repeat_factor
            seen.add(ch)
    return running_total

def pickTopThree(words_pool):
    if not words_pool:
        return ["none", "none", "none"]
    
    scores = {w: scoreWord(w, letterScores) for w in words_pool}
    suggestions = []
    
    for _ in range(min(3, len(scores))):
        high_word = max(scores, key=scores.get)
        suggestions.append(high_word)
        del scores[high_word]
        
    while len(suggestions) < 3:
        suggestions.append("none")
        
    return suggestions

def run_solver_logic(history, current_word, current_pattern):
    """
    Takes the full game history list plus the current round details,
    filters the global word pool, and returns the top 3 best next choices.
    """
    current_pool = list(INITIAL_GUESS_LIST)
    
    # apply from old turns
    for past in history:
        current_pool = filter_words(current_pool, past['words'].lower(), past['pattern'].lower())
        
    #apply new guess
    current_pool = filter_words(current_pool, current_word.lower(), current_pattern.lower())
    
    # get best picks
    top_recommendations = pickTopThree(current_pool)
    
    return top_recommendations, len(current_pool)