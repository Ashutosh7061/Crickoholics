from flask import Flask,render_template,request
import requests

app=Flask(__name__)

@app.route("/")
def index():
        return render_template("index.html")
    
@app.route("/maximizeRatings", methods=["POST"])
def maximize_ratings():
    ratings = request.json.get("ratings", [])
    max_sum = maximizeRatings(ratings)
    return {"max_sum": max_sum}

@app.route("/contactUs")

def contactUs():
    return render_template("contact.html")
@app.route("/ipl")
def ipl():
    response=requests.get('http://127.0.0.1:5000/api/team')
    teams=response.json()['Teams']
    
    response1=requests.get('http://127.0.0.1:5000/api/allBatsman')
    batsman=response1.json()['Batsman']
    
    response2=requests.get('http://127.0.0.1:5000/api/allBowlers')
    bowlers=response2.json()['Bowlers']
    
    return render_template("ipl.html",teams=sorted(teams),batsman=sorted(batsman),bowlers=sorted(bowlers))

@app.route('/teamvteam')
def team_vs_team():
    team1=request.args.get('team1')
    team2=request.args.get('team2')
    response=requests.get('http://127.0.0.1:5000/api/teamVteam?team1={}&team2={}'.format(team1,team2))
    response1=response.json()
    
    response2=requests.get('http://127.0.0.1:5000/api/team')
    teams=response2.json()['Teams']
    
    response3=requests.get('http://127.0.0.1:5000/api/allBatsman')
    batsman=response3.json()['Batsman']
    
    response4=requests.get('http://127.0.0.1:5000/api/allBowlers')
    bowlers=response4.json()['Bowlers']
    
    return render_template('ipl.html',result=response1,teams=sorted(teams),batsman=sorted(batsman),bowlers=sorted(bowlers))

@app.route("/teamindividual")
def teamIndividual():
    team=request.args.get('team')
    response=requests.get('http://127.0.0.1:5000/api/teamRecord?team={}'.format(team))
    response1=response.json()
    
    response2=requests.get('http://127.0.0.1:5000/api/team')
    teams=response2.json()['Teams']
    
    response3=requests.get('http://127.0.0.1:5000/api/allBatsman')
    batsman=response3.json()['Batsman']
    
    response4=requests.get('http://127.0.0.1:5000/api/allBowlers')
    bowlers=response4.json()['Bowlers']
    
    return render_template('ipl.html',result1=response1,teams=sorted(teams),batsman=sorted(batsman),bowlers=sorted(bowlers))

@app.route("/matchSummary")
def matchSummary():
    match_id=request.args.get('match_id')
    response=requests.get('http://127.0.0.1:5000/api/matchSummary?match_id={}'.format(match_id))
    response1=response.json()
    return render_template("ipl.html" ,result2=response1)

@app.route('/batsmanRecord')
def batsmanRecord():
    name=request.args.get('name')
    response=requests.get('http://127.0.0.1:5000/api/batsmanRecord?name={}'.format(name))
    response1=response.json()
    
    response2=requests.get('http://127.0.0.1:5000/api/allBatsman')
    batsman=response2.json()['Batsman']
    
    response3=requests.get('http://127.0.0.1:5000/api/team')
    teams=response3.json()['Teams']
    
    response4=requests.get('http://127.0.0.1:5000/api/allBowlers')
    bowlers=response4.json()['Bowlers']
    
    return render_template("ipl.html",result3=response1,batsman=sorted(batsman),teams=sorted(teams),bowlers=sorted(bowlers))


@app.route('/bowlersRecord')
def bowlerRecord():
    name=request.args.get('name')
    response=requests.get('http://127.0.0.1:5000/api/bowlerRecord?name={}'.format(name))
    response1=response.json()
    
    response2=requests.get('http://127.0.0.1:5000/api/allBowlers')
    bowlers=response2.json()['Bowlers']
    
    response3=requests.get('http://127.0.0.1:5000/api/allBatsman')
    batsman=response3.json()['Batsman']
    
    response4=requests.get('http://127.0.0.1:5000/api/team')
    teams=response4.json()['Teams']
    
    return render_template('ipl.html',result4=response1,bowlers=sorted(bowlers),batsman=sorted(batsman),teams=sorted(teams))
    
    
@app.route('/batsmanVsteam')
def batsmanVsteam():
    name=request.args.get('name')
    team=request.args.get('team')
    response=requests.get('http://127.0.0.1:5000/api/batsmanVsteam?name={}&team={}'.format(name,team))
    response1=response.json()
    
    response2=requests.get('http://127.0.0.1:5000/api/allBatsman')
    batsman=response2.json()['Batsman']
    
    response3=requests.get('http://127.0.0.1:5000/api/team')
    teams=response3.json()['Teams']
    
    response4=requests.get('http://127.0.0.1:5000/api/allBowlers')
    bowlers=response4.json()['Bowlers']
    
    return render_template('ipl.html',result5=response1,batsman=sorted(batsman),teams=sorted(teams),bowlers=sorted(bowlers))
    

@app.route('/bowlerVsteam')
def bowlerVsteam():
    name=request.args.get('name')
    team=request.args.get('team')
    response=requests.get('http://127.0.0.1:5000/api/bowlerVsteam?name={}&team={}'.format(name,team))
    response1=response.json()
    
    response2=requests.get('http://127.0.0.1:5000/api/allBowlers')
    bowlers=response2.json()['Bowlers']
    
    response3=requests.get('http://127.0.0.1:5000/api/team')
    teams=response3.json()['Teams']
    
    response4=requests.get('http://127.0.0.1:5000/api/allBatsman')
    batsman=response4.json()['Batsman']
    
    return render_template('ipl.html' ,result6=response1,bowlers=sorted(bowlers),teams=sorted(teams),batsman=sorted(batsman))

if __name__=='__main__':
    app.run(debug=True,port=8000)
