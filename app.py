import surveys as S
from flask import Flask, render_template, redirect, request, flash, jsonify,session
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config['SECRET_KEY'] = "19191882882"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

responses = []
survey = S.surveys["satisfaction"].questions
Qnum = 0

@app.route('/')
def default_route():
    surv = S.surveys["satisfaction"].title
    return render_template("main.html", Qname = surv)


@app.route('/questions/<int:number>')
def redirect_to_current(number):
    if not number == len(responses):
        return redirect(f"/questions/{len(responses)}")

    if number == len(survey):
        return redirect('/end-quiz')

    endtext = 'Next'
    if number == len(survey)-1:
        endText = 'Finish'

    Qname = survey[number].question
    Qchoices = survey[number].choices
    return render_template('question.html', num = number, question = Qname, choices = Qchoices, button = endtext)


@app.route('/questions/<int:number>', methods=["POST"])
def show_question(number):
    
    #if not number == len(responses):
    #    return redirect(f"/questions/{len(responses)}")
    
    responses.append(request.form["ans"])
    
    if number == len(survey):
        return redirect('/end-quiz')

    endtext = 'Next'
    if number == len(survey)-1:
        endText = 'Finish'

    Qname = survey[number].question
    Qchoices = survey[number].choices
    return render_template('question.html', num = number, question = Qname, choices = Qchoices, button = endtext)


@app.route('/end-quiz')
def thank_you():
    return render_template('thanks.html')