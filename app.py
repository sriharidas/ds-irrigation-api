import numpy as np
from flask import Flask, request, jsonify, render_template
# import pickle
import mysql.connector

# isnerting data into db

# data = pd.read_excel("result.xlsx")
# title = data.columns
# print(title)

db = mysql.connector.connect(host = "localhost", user="root",  database = "datascience", port="3309")
cursor = db.cursor()
# for i in data.values.tolist():
#     # print(i)
#     query = "INSERT INTO irrigation  values (" + str(i[0]) +  ", " +str(i[1]) +", " + str(i[2]) +", " +  str(i[3]) +", '"+ i[4] +"', '"+ i[5]  +"', '" + i[6] +"', '" + i [7] +"')"
#     cursor.execute(query)
#     db.commit()
# db.close()

app = Flask(__name__)
# model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('data.html')

@app.route('/predict',methods=['POST'])
def predict():
    result = ""
    fields = request.form.values()
    soil_type = [int(x) for x in request.form.values()].pop()
    if(soil_type == 1 ):
        cursor.execute("SELECT * from irrigation where Moisture > 35")
        data = cursor.fetchall()
        cursor.execute("SELECT * from irrigation where Moisture < 35 and target = 'irrigate'")
        irrigation = len(cursor.fetchall())
        cursor.execute("SELECT * from irrigation where Moisture > 35 and target = 'no_irrigation'")
        non_irrigation = len(cursor.fetchall())
        print(irrigation, non_irrigation)
        if(irrigation > non_irrigation):
            result = "irrigate"
        else:
            result = "no irrigation"
    else:
        cursor.execute("SELECT * from irrigation where Moisture > 45")
        data = cursor.fetchall()
        cursor.execute("SELECT * from irrigation where Moisture < 45 and target = 'irrigate'")
        irrigation = len(cursor.fetchall())
        cursor.execute("SELECT * from irrigation where Moisture > 45 and target = 'no_irrigation'")
        non_irrigation = len(cursor.fetchall())
        print(irrigation, non_irrigation)
        if(irrigation > non_irrigation):
            result = "irrigate"
        else:
            result = "no irrigation"

    # final_features = [np.array(int_features)]
    # prediction = model.predict(final_features)

    # output = round(prediction[0], 2)

    return render_template('data.html' , result="Result : " + str(result))

@app.route('/results',methods=['POST'])
def results():

    data = request.get_json(force=True)
    prediction = model.predict([np.array(list(data.values()))])

    output = prediction[0]
    return jsonify(output)

if __name__ == "__main__":
    app.run(debug=True)