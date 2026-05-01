from flask import Flask, request, render_template
from ai_agent.graph import build_graph

app = Flask(__name__)

graph = build_graph()


@app.route("/", methods=["GET", "POST"])
def index():
    answer = None
    query = None

    if request.method == "POST":
        query = request.form.get("query")

        if query:
            result = graph.invoke({"query": query})
            answer = result.get("final_answer")

    return render_template("index.html", query=query, answer=answer)


if __name__ == "__main__":
    app.run(debug=True)