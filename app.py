from flask import Flask, render_template, request, jsonify
from football_api import get_today_fixtures, get_predictions, get_odds
from analyzer import probabilities, implied, ev, label
import os, json

app=Flask(__name__)
BET_FILE="data/bets.json"
os.makedirs("data",exist_ok=True)
if not os.path.exists(BET_FILE): open(BET_FILE,"w").write("[]")

@app.route("/")
def home(): return render_template("index.html")

@app.route("/api/today")
def today():
    try:
        data=get_today_fixtures()
        matches=[]
        for x in data.get("response",[]):
            matches.append({
                "id":x["fixture"]["id"],
                "date":x["fixture"]["date"],
                "status":x["fixture"]["status"]["short"],
                "home":x["teams"]["home"]["name"],
                "away":x["teams"]["away"]["name"],
                "league":x["league"]["name"],
                "country":x["league"]["country"]
            })
        return jsonify({"success":True,"matches":matches})
    except Exception as e:
        return jsonify({"success":False,"error":str(e)}),500

@app.route("/api/match/<int:fixture_id>")
def match_analysis(fixture_id):
    try:
        prediction_data = get_predictions(fixture_id)
        odds_data = get_odds(fixture_id)

        prediction = prediction_data.get("response", [])
        odds = odds_data.get("response", [])

        result = {
            "success": True,
            "fixture_id": fixture_id,
            "prediction": prediction,
            "odds": odds,
            "analysis_status": "DATA_LOADED",
            "message": "Match data successfully collected."
        }

        return jsonify(result)

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
def match_analysis(fixture_id):
    try:
        pred=get_predictions(fixture_id).get("response",[])
        odds=get_odds(fixture_id).get("response",[])
        return jsonify({"success":True,"fixture_id":fixture_id,
                        "api_prediction":pred,"odds":odds,
                        "note":"API data is shown for analysis; final model will be expanded with verified form/statistics."})
    except Exception as e:
        return jsonify({"success":False,"error":str(e)}),500

@app.route("/api/model",methods=["POST"])
def model():
    try:
        d=request.get_json()
        hx=float(d["home_xg"]); ax=float(d["away_xg"])
        p=probabilities(hx,ax)
        markets={}
        names={"Home":"home","Draw":"draw","Away":"away","Over 2.5":"over25","BTTS Yes":"btts"}
        for name,key in names.items():
            value=d.get("odds",{}).get(name)
            if value not in ("",None):
                o=float(value); e=ev(p[key],o)
                markets[name]={"probability":p[key],"implied":implied(o),"ev":e,"decision":label(e)}
        return jsonify({"success":True,"probabilities":p,"markets":markets})
    except Exception as e:
        return jsonify({"success":False,"error":str(e)}),400

@app.route("/api/bankroll",methods=["POST"])
def bankroll():
    try:
        d=request.get_json(); b=float(d["bankroll"]); pct=float(d.get("percent",2))
        if b<=0 or pct<0 or pct>100: raise ValueError("Invalid bankroll or percentage.")
        return jsonify({"success":True,"stake":b*pct/100})
    except Exception as e: return jsonify({"success":False,"error":str(e)}),400

@app.route("/api/bets",methods=["GET","POST"])
def bets():
    data=json.load(open(BET_FILE))
    if request.method=="POST":
        data.append(request.get_json()); json.dump(data,open(BET_FILE,"w"),indent=2)
        return jsonify({"success":True})
    return jsonify(data)

if __name__=="__main__":
    app.run(host="0.0.0.0",port=int(os.environ.get("PORT",5000)))
