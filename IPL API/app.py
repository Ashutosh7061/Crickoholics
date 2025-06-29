from flask import Flask,jsonify,request
import ipl as ipl


app=Flask(__name__)

@app.route('/')
def Home():
    return "Hello, World!"
@app.route("/api/team")
def team():
    teams=ipl.teamAPI();  #When ever we create any api then its return file must be a json type
    return jsonify(teams)
@app.route("/api/allBatsman")
def all_batsman():
    response=ipl.all_batsmanAPI()
    return jsonify(response)
@app.route("/api/allBowlers")
def allBowlers():  
    response=ipl.allBowlersAPI()
    return jsonify(response)

@app.route("/api/teamVteam")
def teamVteam():
    team1=request.args.get('team1')
    team2=request.args.get('team2')
    response=ipl.team_vs_teamAPI(team1,team2)
    return jsonify(response)

@app.route("/api/teamRecord")
def teamRecord():
    team=request.args.get('team')
    response=ipl.teamRecordAPI(team)
    return jsonify(response)


@app.route("/api/batsmanRecord")
def batsmanRecord():
    name=request.args.get('name')
    response=ipl.batsmanRecordAPI(name)
    return jsonify(response)

@app.route("/api/bowlerRecord")
def bowlerRecord():
    name=request.args.get('name')
    response=ipl.bowlerRecordsAPI(name)
    return jsonify(response)


@app.route("/api/batsmanVsteam")
def batsmanVsteam():
    name=request.args.get('name')
    team=request.args.get('team')
    response=ipl.get_batsman_stats_teamAPI(name,team)
    return jsonify(response)


@app.route("/api/bowlerVsteam")
def bowlerVsteam():
    name=request.args.get('name')
    team=request.args.get('team')
    response=ipl.get_bowler_stats_teamAPI(name,team)
    return jsonify(response)

@app.route("/api/topbatsman")
def top5batsman():
    response=ipl.get_top_bowler_overall_API()
    return jsonify(response)

@app.route("/api/topbowler")
def top5bowler():
    response=ipl.get_top_batsmen_overall_API()
    return jsonify(response)

@app.route("/api/matchSummary")
def matchSummary():
    match_id=request.args.get('match_id')
    response=ipl.match_summary_API(match_id)
    return jsonify(response)


if __name__=="__main__":
    app.run(debug=True)