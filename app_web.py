from flask import Flask, render_template_string, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = "kunci_rahasia_kuis"

# Tampilan HTML & CSS dalam satu file
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kuis Penjumlahan Satuan</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f0f2f5; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }
        .card { background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); width: 100%; max-width: 400px; text-align: center; }
        h1 { color: #333; font-size: 24px; margin-bottom: 10px; }
        .score { font-size: 14px; color: #666; margin-bottom: 20px; }
        .question { font-size: 36px; font-weight: bold; color: #2c3e50; margin: 20px 0; }
        .options { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 20px; }
        .btn-option { padding: 15px; font-size: 20px; border: 2px solid #e0e0e0; background: #fff; border-radius: 8px; cursor: pointer; transition: all 0.2s; }
        .btn-option:hover { background: #eef2ff; border-color: #4f46e5; color: #4f46e5; }
        .feedback { font-size: 16px; font-weight: bold; margin-bottom: 15px; min-height: 24px; }
        .correct { color: #16a34a; }
        .wrong { color: #dc2626; }
        .btn-next { width: 100%; padding: 12px; font-size: 16px; background: #4f46e5; color: white; border: none; border-radius: 8px; cursor: pointer; }
        .btn-next:hover { background: #4338ca; }
    </style>
</head>
<body>
    <div class="card">
        <h1>Kuis Penjumlahan Satuan</h1>
        <div class="score">Skor: <strong>{{ session.get('score', 0) }}</strong> / {{ session.get('total', 0) }}</div>

        {% if feedback %}
            <div class="feedback {{ 'correct' if is_correct else 'wrong' }}">
                {{ feedback }}
            </div>
            <a href="{{ url_for('index') }}"><button class="btn-next">Soal Berikutnya ➔</button></a>
        {% else %}
            <div class="question">{{ num1 }} + {{ num2 }} = ?</div>
            <form method="POST" action="/check">
                <div class="options">
                    {% for opt in options %}
                        <button type="submit" name="answer" value="{{ opt }}" class="btn-option">{{ opt }}</button>
                    {% endfor %}
                </div>
            </form>
        {% endif %}
    </div>
</body>
</html>
"""

def generate_question():
    a = random.randint(0, 9)
    b = random.randint(0, 9)
    correct = a + b
    
    # Buat 3 opsi jawaban salah yang unik dan masuk akal
    wrong_options = set()
    while len(wrong_options) < 3:
        fake = random.randint(0, 18)
        if fake != correct:
            wrong_options.add(fake)
            
    options = list(wrong_options) + [correct]
    random.shuffle(options)
    
    return a, b, correct, options

@app.route("/")
def index():
    a, b, correct, options = generate_question()
    session['num1'] = a
    session['num2'] = b
    session['correct'] = correct
    
    return render_template_string(HTML_TEMPLATE, num1=a, num2=b, options=options)

@app.route("/check", methods=["POST"])
def check():
    user_ans = int(request.form.get("answer"))
    correct_ans = session.get('correct')
    
    session['total'] = session.get('total', 0) + 1
    
    if user_ans == correct_ans:
        session['score'] = session.get('score', 0) + 1
        feedback = "Benar! Bagus sekali 🎉"
        is_correct = True
    else:
        feedback = f"Salah! Jawaban yang benar adalah {correct_ans} ❌"
        is_correct = False
        
    return render_template_string(
        HTML_TEMPLATE, 
        feedback=feedback, 
        is_correct=is_correct
    )

if __name__ == "__main__":
    app.run(debug=True)
