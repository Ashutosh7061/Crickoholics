import pandas as pd
import numpy as np
from collections import OrderedDict


df=pd.read_csv('match1.csv')
#print(df.head())

df1=pd.read_csv('deliveries1.csv')

all_bowlers=list(set(list(df1['bowler'])))
all_batsmans=list(set(list(df1['batter'])))
combine=df.merge(df1,on='match_id')

def teamAPI():
    ipl_teams=list(set(list(df['team1'])+list(df['team2'])))
    teams={
        'Teams':ipl_teams
    }
    return teams

def all_batsmanAPI():
    all_batsman=list(set(list(df1['batter'])+list(df1['non_striker'])))
    response={
        "Batsman":all_batsman
    }
    return response
def team_vs_teamAPI(team1,team2):
    valid_teams=list(set(list(df['team1'])+list(df['team2'])))
    
    if team1 in valid_teams and team2 in valid_teams: 
        total_played=df[((df['team1']==team1) &  (df['team2']==team2)) | ((df['team1']==team2) & (df['team2']==team1))]
        total=total_played.shape[0]
        team1_won=total_played['winner'].value_counts()[team1]
        team2_won=total_played['winner'].value_counts()[team2]
        draw_match=total-(team1_won+team2_won)

        response={
            "Total Match Played":str(total),
            team1:str(team1_won),
            team2:str(team2_won),
            "Draws":str(draw_match)
        }
        return response
    else:
        return {"Message":"Invalid Input"}
    
def teamRecordAPI(team):
    valid_teams=list(set(list(df['team1'])+list(df['team2'])))
    if team in valid_teams:
        counts=df[(df['team1']==team) | (df['team2']==team)].copy()
        match_played=counts.shape[0]
        won=counts[counts.winner==team].shape[0]
        losses=counts[counts.winner!=team].shape[0]
        draw=counts[(counts['result']=='tie') ].shape[0]
        title=counts[(counts['match_type']=='Final') & (counts['winner']==team)].shape[0]
        toss_won=counts[counts['toss_winner']==team].shape[0]
        not_declared=counts[counts['winner'].isnull()].shape[0]

        response={
            'Total Match Played':match_played,
            'Toss Won':toss_won,
            'Match Won':won,
            'Match Losses':losses,
            'Match Draw':draw,
            'Result Not Declared':not_declared,
            'Title':title
        }
        return response
    else:
        return {"Message":"Invalid Input"}

def allBowlersAPI():
    all_bowlers=list(set(list(df1['bowler'])))
    response={
        "Bowlers":all_bowlers
    }
    return response

def bowlerRecordsAPI(name):
    if name in all_bowlers:
        mom=df[df['player_of_match']==name].shape[0]
        bowl=df1[df1['bowler']==name]
        total_ball=bowl.shape[0]
        run_delivered=bowl['total_runs'].sum()
        wicket=bowl['is_wicket'].sum()
        four=bowl[bowl['total_runs']==4].shape[0]
        six=bowl[bowl['total_runs']==6].shape[0]
        over=total_ball//6
        economy=run_delivered/over if over>0 else 0
        match_wickets=bowl.groupby('match_id')['is_wicket'].sum()
        three_plus_wickets=(match_wickets >= 3).sum()
        total_innings=bowl.groupby(['match_id', 'inning']).ngroups
        best_match=match_wickets.idxmax()
        best_wickets=match_wickets.max()
        best_runs_conceded=bowl[bowl['match_id'] == best_match]['total_runs'].sum()

        response={
            "bowler":name,
            "total_overs":over,
            "total_wickets":int(wicket),
            "total_runs_delivered ":int(run_delivered),
            "economy_rate":round(economy, 2),
            "three_plus_wicket_matches":int(three_plus_wickets),
            "total_innings":int(total_innings),
            "best_bowling_figure":f"{int(best_wickets)}/{int(best_runs_conceded)}",
            "man of the match":mom,
            "four":four,
            "six":six
        }
        return response
    else:
        return {"Message":"Invalid Input"}
    
def batsmanRecordAPI(name):
    if name in all_batsmans:
        bat_data=df1[df1['batter']==name]
        mom=df[df['player_of_match']==name].shape[0]
        no_of_strike=bat_data.shape[0]
        no_of_over=no_of_strike//6
        score=bat_data['batsman_runs'].sum()
        innings=bat_data.groupby('match_id').sum().shape[0]
        highest=bat_data.groupby(['match_id','inning'])['batsman_runs'].sum().max()
        dismissal=df1[df1['player_dismissed']==name].shape[0]
        fours=bat_data[bat_data['batsman_runs']==4].shape[0]
        sixes=bat_data[bat_data['batsman_runs']==6].shape[0]
        hundreds=sum(bat_data.groupby(['match_id','inning'])['batsman_runs'].sum()>=100)
        fifty_plus=sum((bat_data.groupby(["match_id", "inning"])["batsman_runs"].sum() >= 50) & 
                        (bat_data.groupby(["match_id", "inning"])["batsman_runs"].sum() < 100))
        batting_average=score/dismissal if dismissal > 0 else score
        economy_rate=(score/no_of_strike) * 6 if no_of_strike> 0 else 0
        not_outs=innings-dismissal

        response = {
            "batsman": name,
            "total_runs": int(score),  
            "batting_average": f'{batting_average:.2f}',
            "total_fours": int(fours), 
            "total_sixes": int(sixes),  
            "man_of_the_match_count": int(mom),  
            "dismissal_count": int(dismissal),  
            "not_outs": int(not_outs),  
            "highest_score": int(highest),  
            "fifty_plus_scores": int(fifty_plus),  
            "hundred_plus_scores": int(hundreds),  
            "economy_rate": f'{economy_rate:.2f}'
        }
        return response
    else:
        return {"Message":"Invalid Input"}
    
    
def get_batsman_stats_teamAPI(batsman_name, opponent_team):
    batsman_data = combine[(combine["batter"] == batsman_name) & (combine["bowling_team"] == opponent_team)]
    
    if batsman_data.empty:
        return {"error": "No data available for this batsman against the given opponent."}
    
    total_runs = batsman_data["batsman_runs"].sum()
    total_fours = (batsman_data["batsman_runs"] == 4).sum()
    total_sixes = (batsman_data["batsman_runs"] == 6).sum()
    innings_played = batsman_data["match_id"].nunique()
    dismissals = batsman_data["player_dismissed"].dropna().nunique()
    best_score = batsman_data.groupby("match_id")["batsman_runs"].sum().max()
    fifties = (batsman_data.groupby("match_id")["batsman_runs"].sum() >= 50).sum()
    centuries = (batsman_data.groupby("match_id")["batsman_runs"].sum() >= 100).sum()
    total_balls_faced = len(batsman_data)
    strike_rate = (total_runs / total_balls_faced) * 100 if total_balls_faced > 0 else 0
    batting_average = total_runs / dismissals if dismissals > 0 else total_runs
    mom_count = batsman_data[batsman_data["player_of_match"] == batsman_name]["match_id"].nunique()

    response={
        "batsman": batsman_name,
        "opponent_team": opponent_team,
        "total_runs": int(total_runs),
        "total_sixes": int(total_sixes),
        "total_fours": int(total_fours),
        "fifties": int(fifties),
        "centuries": int(centuries),
        "dismissals": int(dismissals),
        "best_score":int( best_score),
        "innings_played": int(innings_played),
        "strike_rate": int(round(strike_rate, 2)),
        "batting_average": int(round(batting_average, 2)),
        "MOM":int(mom_count)
    }
    return response

def get_bowler_stats_teamAPI(bowler_name, opponent_team):
    bowler_data = combine[(combine["bowler"] == bowler_name) & (combine["batting_team"] == opponent_team)]
    
    total_wickets = bowler_data["player_dismissed"].dropna().nunique()  # Unique dismissals
    total_runs_conceded = bowler_data["total_runs"].sum()
    
    # Handle balls bowled (ignoring wides, ensuring NaN handling)
    balls_bowled = len(bowler_data[bowler_data["extras_type"].fillna("") != "wides"])
    overs_bowled = balls_bowled // 6 + (balls_bowled % 6) / 6.0
    
    economy_rate = total_runs_conceded / overs_bowled if overs_bowled > 0 else 0
    strike_rate = balls_bowled / total_wickets if total_wickets > 0 else 0
    bowling_average = total_runs_conceded / total_wickets if total_wickets > 0 else 0
    
    best_wickets = bowler_data.groupby("match_id")["player_dismissed"].nunique().max()  # Improved calculation
    mom_count = bowler_data[bowler_data["player_of_match"] ==bowler_name]["match_id"].nunique()

    response={
        "bowler": bowler_name,
        "opponent_team": opponent_team,
        "total_wickets": int(total_wickets),
        "best_wickets": int(best_wickets),
        "total_runs_conceded": int(total_runs_conceded),
        "balls_bowled": int(balls_bowled),
        "economy_rate": int(round(economy_rate, 2)),
        "strike_rate": int(round(strike_rate, 2)),
        "bowling_average": int(round(bowling_average, 2)),
        "MOM":int(mom_count)
    }
    return response

def get_top_batsmen_overall_API():
    top_batsmen = combine.groupby("batter")["batsman_runs"].sum().nlargest(5).reset_index()
    return top_batsmen.to_dict(orient="records")

def get_top_batsmen_overall_API():
    top_bowler= combine.groupby("bowler")["is_wicket"].sum().nlargest(5).reset_index()
    return top_bowler.to_dict(orient="records")

def match_summary_API(match_id):
    combine['match_id'] = combine['match_id'].astype(str).str.strip()
    match_id = str(match_id).strip()
    match = combine[combine['match_id'] == match_id]  


    # General match details
    season = match['season'].unique()[0]
    city = match['city'].unique()[0]
    venue = match['venue'].unique()[0]   # take column season find all unique value and retuen 1st value(here only 1 value)
    team1 = match['team1'].unique()[0]
    team2 = match['team2'].unique()[0]
    toss_winner = match['toss_winner'].values[0]
    toss_decision = match['toss_decision'].values[0]
    match_winner = match['winner'].values[0]
    mom = match['player_of_match'].values[0]

    # Runs and boundaries
    total_run = match['total_runs'].sum()
    run_inni1 = match[match['inning'] == 1]['total_runs'].sum()
    run_inni2 = match[match['inning'] == 2]['total_runs'].sum()
    total_sixes = (match['total_runs'] == 6).sum()
    total_fours = (match['total_runs'] == 4).sum()

    # Match result details
    won_by = match['result'].values[0]
    difference = match['result_margin'].values[0]
    
    # Best bowler (most wickets)
    wicket_counts = match.groupby('bowler')['is_wicket'].sum()
    max_wicket = wicket_counts.max()
    max_wicketer = wicket_counts.idxmax()

    # Best batter (most runs)
    run_counts = match.groupby('batter')['batsman_runs'].sum()
    max_run = run_counts.max()
    max_run_scorer = run_counts.idxmax()

    # Umpires and Super Over
    umpire1 = match['umpire1'].values[0]
    umpire2 = match['umpire2'].values[0]
    super_over = match['super_over'].values[0]

    # Create dictionary response
    response = OrderedDict([
        ("match_id", int(match_id)),
        ("season", str(season)),
        ("city", str(city)),
        ("venue", str(venue)),
        ("team1", str(team1)),
        ("team2", str(team2)),
        ("toss_winner", str(toss_winner)),
        ("toss_decision", str(toss_decision)),
        ("match_winner", str(match_winner)),
        ("player_of_match", str(mom)),
        ("total_run", int(total_run)),
        ("run_innings_1", int(run_inni1)),
        ("run_innings_2", int(run_inni2)),
        ("total_sixes", int(total_sixes)),
        ("total_fours", int(total_fours)),
        ("won_by", str(won_by)),
        ("difference", int(difference)),
        ("top_bowler", str(max_wicketer)),
        ("max_wickets", int(max_wicket)),
        ("top_scorer", str(max_run_scorer)),
        ("max_runs", int(max_run)),
        ("umpire1", str(umpire1)),
        ("umpire2", str(umpire2)),
        ("super_over", str(super_over))
    ])

    return response
