# app.py
from flask import Flask, render_template, request, jsonify
# Import your custom logic file
import solver 

app = Flask(__name__)

@app.route("/")
def wordlesolver():
    # Grabs the starting word recommendations directly from the module
    initial_suggestions = solver.pickTopThree(list(solver.INITIAL_GUESS_LIST))
    return render_template("wordleSolver.html", starting_words=initial_suggestions)

@app.route('/submit-guess', methods=['POST'])
def handle_guess():
    data = request.get_json()
    
    guess_word = data.get('words', '') 
    color_pattern = data.get('pattern', '')
    history = data.get('history', []) 
    
    print(f"\n--- Turn Processing ---")
    print(f"Word: {guess_word} | Pattern: {color_pattern}")

    # Offload the computation entirely to solver.py
    recommendations, remaining_count = solver.run_solver_logic(history, guess_word, color_pattern)
    print(recommendations)

    return jsonify({
        "status": "success",
        "recommendations": recommendations,
        "remaining_count": remaining_count
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)