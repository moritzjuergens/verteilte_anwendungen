import os
from flask import Flask, Response, request
import requests
import json
from supabase import create_client, Client
from flask_cors import CORS


app = Flask(__name__, static_folder='../client/dist/',    static_url_path='/')


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
def questions():
    try:
        res = client.postgrest.from_table("questions").select("*").execute()
        return Response(json.dumps(res.data), mimetype='application/json')
    except Exception as err:
        print(err)
        return Response(status=500)


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


@app.route("/answers", methods=["POST"])
def store_results():
    payload = request.json

    try:
        client.postgrest.from_table("questions").upsert({
            "question": payload["question"],
            "answers": payload["answers"],
            "corr_idx": payload["corr_idx"]
        }).execute()
        return Response(status=200)
    except Exception as err:
        print(err)
        return Response(status=500)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
