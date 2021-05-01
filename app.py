from flask import Flask, jsonify, render_template
import firebase_admin
from firebase_admin import credentials, firestore
import spacy
from sentifish import Sentiment
import random

nlp = en_core_web_sm.load()


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)



db = firestore.client()

app = Flask(__name__)

@app.route('/')
def home():
                try:
                                return "Success"
              
                except Exception as e:
                                return str(e)

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
                                                "questionsDb": tempQuestionList.copy()
                                }
                except:
                                tempResponse = {
                                                "responseCode":404,
                                                "questionsDb": []
                                }
                return jsonify(tempResponse)

@app.route('/answerScore')
def getScore():
                try:
                                referenceAnswer = request.args.get("referenceAnswer", default='-1', type=str)
                                userAnswer = request.args.get("userAnswer", default='-1', type=str)
          
                                obj=Sentiment(userAnswer)
                                sentimentScore = obj.analyze()
                  
                                doc1 = nlp(userAnswer)
                                doc2 = nlp(referenceAnswer)
                                correctAnswerScore = doc1.similarity(doc2)
                      
                                spell = SpellChecker()
                                tempX= list(userAnswer)
                                misspelled = spell.unknown(tempX)
                                count=0
                                for word in misspelled:
                                    count+=1
                                
                                tempResponse = {
                                                "responseCode":200,
                                                "sentimentScore":round(sentimentScore+1),
                                                "correctAnswerScore":round(correctAnswerScore*6),
                                                "fluencyScore": round((count/len(tempX))*2)
                                }
              
                except Exception as e:
                                tempResponse = {
                                                "responseCode":404,
                                                "sentimentScore":0,
                                                "correctAnswerScore":0,
                                                "fluencyScore": 0
                                }
                return str(e)

if __name__ == '__main__': 
                app.run(debug=True)
