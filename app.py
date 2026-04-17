from flask import Flask, render_template, request
from search import search_subtitles

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    results = []

    if request.method == "POST":
        query = request.form["query"]
        results = search_subtitles(query)
        print(len(results))

    return render_template("index.html", results=results)


if __name__ == "__main__":
    app.run(debug=True)