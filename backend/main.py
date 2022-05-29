import os
from flask import Flask, Response, request
import requests
import json
from supabase import create_client, Client
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={r'/*': {'origins': '*'}})

supabase_url = "https://hqatoyyncrwdojrhwygi.supabase.co"
supabase_key = os.getenv("SUPABASE_KEY")
if supabase_key is None or len(supabase_key) == 0:
    raise Exception(
        "please make sure to provide the SUPABASE_KEY environment variable")

client: Client = create_client(
    supabase_url=supabase_url, supabase_key=supabase_key)


@app.route("/highscores", methods=["GET"])
def highscores():
    try:
        res = client.postgrest.from_table("highscores").select("*").execute()
        return Response(json.dumps(res.data), mimetype='application/json')
    except Exception as err:
        print(err)
        return Response(status=500)


@app.route("/questions", methods=["GET"])
def proxy_questions():
    res = requests.get("https://opentdb.com/api.php?amount=10&type=multiple")
    if res.status_code != 200:
        return Response(status=res.status_code, response="could not load questions from remote API endpoint")

    questions = res.json()
    return Response(json.dumps(questions["results"]), mimetype='application/json')


@app.route("/results", methods=["POST"])
def store_results():
    payload = request.json

    try:
        client.postgrest.from_table("highscores").upsert({
            "name": payload["player"],
            "score": payload["score"]
        }).execute()
        return Response(status=200)
    except Exception as err:
        print(err)
        return Response(status=500)
