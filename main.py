from flask import Flask, render_template, request, session, redirect, url_for
import os
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session handling

# Load questions from JSON file
def load_questions():
    file_path = os.path.join(os.getcwd(), 'questions', 'question.json')  # Match your directory
    with open(file_path, 'r') as f:
        return json.load(f)

def get_medium_quiz_data(quiz_type):
    file_path = os.path.join(os.getcwd(), 'questions', 'medium_questions.json')
    with open(file_path, 'r') as f:
        all_questions = json.load(f)
    return all_questions.get(quiz_type, [])

def get_hard_quiz_data(quiz_type):
    file_path = os.path.join(os.getcwd(), 'questions', 'hard_questions.json')
    with open(file_path, 'r') as f:
        all_questions = json.load(f)
    return all_questions.get(quiz_type, [])

questions = load_questions()

@app.route('/')
def index():
    return render_template('index.html', active_page='index')

@app.route('/about')
def about():
    return render_template('about.html', active_page='about')

@app.route('/contact')
def contact():
    return render_template('contact.html', active_page='contact')

@app.route('/quiz/easy')
def quiz_easy():
    return render_template('quiz_easy.html', active_page='quiz_easy')

@app.route('/quiz/easy/guess_character_image', methods=['GET', 'POST'])
def quiz_guess_character_image():
    return handle_quiz('guess_character_image', 'quiz_easy_results')

@app.route('/quiz/easy/guess_lead_character', methods=['GET', 'POST'])
def quiz_guess_lead_character():
    return handle_quiz('guess_lead_character', 'quiz_easy_results')

@app.route('/quiz/easy/guess_game_by_enemy', methods=['GET', 'POST'])
def quiz_guess_game_by_enemy():
    return handle_quiz('guess_game_by_enemy', 'quiz_easy_results')

def handle_quiz(quiz_type, results_route):
    if 'question_index' not in session or session.get('current_quiz') != quiz_type:
        session['question_index'] = 0
        session['score'] = 0
        session['current_quiz'] = quiz_type

    if request.method == 'POST':
        selected_option = request.form.get('option')
        current_question = questions[quiz_type][session['question_index']]

        if selected_option == current_question['answer']:
            session['score'] += 1

        session['question_index'] += 1

        if session['question_index'] >= len(questions[quiz_type]):
            return redirect(url_for(results_route))

    current_question = questions[quiz_type][session['question_index']]
    return render_template('quiz_question.html', question=current_question, index=session['question_index'] + 1)



@app.route('/quiz/easy/results')
def quiz_easy_results():
    score = session.get('score', 0)
    total_questions = len(questions[session.get('current_quiz', '')])
    session.pop('question_index', None)  # Reset question index
    session.pop('current_quiz', None)  # Reset current quiz type
    session.pop('score', None)  # Reset score
    return render_template('quiz_easy_results.html', score=score, total_questions=total_questions)


@app.route('/quiz/medium')
def quiz_medium():
    return render_template('quiz_medium.html', active_page='quiz_medium')

@app.route('/quiz/medium/complete_game_name', methods=['GET', 'POST'])
def complete_game_name():
    questions = get_medium_quiz_data('complete_game_name')
    return render_template('complete_game_name.html', questions=questions)

@app.route('/quiz/medium/guess_game_by_plot', methods=['GET', 'POST'])
def guess_game_by_plot():
    questions = get_medium_quiz_data('guess_game_by_plot')
    return render_template('guess_game_by_plot.html', questions=questions)

@app.route('/quiz/medium/match_year', methods=['GET', 'POST'])
def match_year():
    questions = get_medium_quiz_data('match_year')
    return render_template('match_year.html', questions=questions)



@app.route('/quiz/hard')
def quiz_hard():
    return render_template('quiz_hard.html', active_page='quiz_hard')

@app.route('/quiz/hard/guess_game_item', methods=['GET', 'POST'])
def guess_game_item():
    if 'question_index' not in session:
        session['question_index'] = 0
        session['score'] = 0

    questions = get_hard_quiz_data('guess_game_item')
    question_index = session['question_index']

    if request.method == 'POST':
        selected_answer = request.form.get('answer')
        current_question = questions[question_index]

        if selected_answer == current_question['answer']:
            session['score'] += 1
            session['question_index'] += 1

            # Check if there are more questions
            if session['question_index'] >= len(questions):
                return redirect(url_for('quiz_hard_results'))

            # Redirect to the same page to load the next question
            return redirect(url_for('guess_game_item'))
        else:
            # End the game if the answer is incorrect
            return redirect(url_for('quiz_hard_results'))

    # Render the current question
    current_question = questions[question_index]
    return render_template('guess_game_item.html', question=current_question)

@app.route('/quiz/hard/guess_game_world', methods=['GET', 'POST'])
def guess_game_world():
    if 'question_index' not in session:
        session['question_index'] = 0
        session['score'] = 0

    questions = get_hard_quiz_data('guess_game_world')
    question_index = session['question_index']

    if request.method == 'POST':
        selected_answer = request.form.get('answer')
        current_question = questions[question_index]

        if selected_answer == current_question['answer']:
            session['score'] += 1
            session['question_index'] += 1

            if session['question_index'] >= len(questions):
                return redirect(url_for('quiz_hard_results'))

            return redirect(url_for('guess_game_world'))
        else:
            return redirect(url_for('quiz_hard_results'))

    current_question = questions[question_index]
    return render_template('guess_game_world.html', question=current_question)


@app.route('/quiz/hard/hard_quiz_3', methods=['GET', 'POST'])
def hard_quiz_3():
    if 'question_index' not in session:
        session['question_index'] = 0
        session['score'] = 0

    questions = get_hard_quiz_data('hard_quiz_3')
    question_index = session['question_index']

    if request.method == 'POST':
        selected_answer = request.form.get('answer')
        current_question = questions[question_index]

        if selected_answer == current_question['answer']:
            session['score'] += 1
            session['question_index'] += 1

            if session['question_index'] >= len(questions):
                return redirect(url_for('quiz_hard_results'))

            return redirect(url_for('hard_quiz_3'))
        else:
            return redirect(url_for('quiz_hard_results'))

    current_question = questions[question_index]
    return render_template('hard_quiz_3.html', question=current_question)


@app.route('/quiz/hard/results')
def quiz_hard_results():
    score = session.get('score', 0)
    session.pop('question_index', None)
    session.pop('score', None)
    return render_template('quiz_hard_results.html', score=score)


if __name__ == '__main__':
    app.run(debug=True)
