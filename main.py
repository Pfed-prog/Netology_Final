from flask import Flask, request, jsonify, render_template
import numpy as np
import pickle
import pandas as pd
#libraries

app = Flask(__name__, template_folder='templates') #Initialize the flask App
model = pickle.load(open('finalized_model.sav', 'rb'))


cols=['php', 'javascript', 'laravel', 'html', 'symfony', 'sql', 'linux', 'css', 'jquery', 'yii', 'redis', 'docker', 'rabbitmq', 'ajax', 'python', 'git', 'django', 'ооп', 'rest', 'flask', 'английский язык', 'c++', 'c/c++', 'qt', 'stl', 'c#', 'boost']
@app.route("/")
def starter():
  return render_template('index.html')

@app.route("/test.html")
def ask():
  return render_template('test.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    
    # retrieving values from form
    init_features = [x for x in request.form.values()]
    final = list(map(int, init_features[:27]))
    df = pd.DataFrame([final], columns=cols)
    for i in cols:
        df[i] = df[i].apply(lambda x: 1 if x>3 else 0)

    prediction = model.predict(df) # making prediction
    proba = model.predict_proba(df) # underlying probabilities
    ''''''
    # logika
    # тест на баланс
    # добавить вопросы

    rec = ''

    pr1 = proba[0][0][0]
    pr2 = proba[1][0][0]
    pr3 = proba[2][0][0]

    cond_pr =  max(pr1, pr2, pr3)
    
    if cond_pr==pr1: 
        rec = 'PHP/SQL: back-end разработка и базы данных: https://netology.ru/programs/php-sql'
    elif cond_pr == pr2:
        rec = 'Fullstack-разработчик на Python: https://netology.ru/programs/fullstack-python-dev#/'
    else:
        rec = 'Программирование на языке C++: https://stepik.org/course/7/promo'
        
    return render_template('result.html', pred=f'{prediction}', pr = f'{rec}')


if __name__ == '__main__':
  app.run(debug=True)