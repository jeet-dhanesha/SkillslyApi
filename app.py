from flask import Flask, jsonify, render_template
import firebase_admin
from firebase_admin import credentials, firestore
import random

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

app = Flask(__name__)

@app.route('/')
def home():
                return render_template("index.html")

@app.route('/subjectList')
def subjectList():
                try:
                                tempSubjectList = []
                                data = db.collection("subjectList").get() 
                                for elem in data:
                                                tempSubjectList.append(elem.to_dict())
                                tempResponse = {
                                                "responseCode":200,
                                                "subjectList": tempSubjectList.copy()
                                }
                except:
                                tempResponse = {
                                                "responseCode":404,
                                                "subjectList": []
                                }
                return jsonify(tempResponse)

@app.route('/practiceQuestion/<string:subjectName>')
def practiceQuestion(subjectName):
                try:
                                tempQuestionList = []
                                data = db.collection(subjectName + "_practiceQuestions").get()
                                for elem in data:
                                                tempQuestionList.append(elem.to_dict())
                                # questionList = random.sample(tempQuestionList,10)
                                tempResponse = {
                                                "responseCode":200,
                                                "questionsDb": tempQuestionList.copy()
                                }
                except:
                                tempResponse = {
                                                "responseCode":404,
                                                "questionsDb": []
                                }
                return jsonify(tempResponse)

@app.route('/interviewQuestions/<string:subjectName>')
def interviewQuestions(subjectName):
                try:
                                tempQuestionList = []
                                data = db.collection(subjectName + "_interviewQuestions").get() 
                                for elem in data:
                                                tempQuestionList.append(elem.to_dict())
                                questionList = random.sample(tempQuestionList,10)
                                tempResponse = {
                                                "responseCode":200,
                                                "questionsDb": questionList.copy()
                                }
                except:
                                tempResponse = {
                                                "responseCode":404,
                                                "questionsDb": []
                                }
                return jsonify(tempResponse)

if __name__ == '__main__': 
                app.run(debug=True)
