from flask import Flask, render_template, request
from works import CodeToFlowchart

app = Flask(__name__)
app.secret_key = "supersecretkey"

ALLOWED_EXTENSIONS = {"py"}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def index():
    code = ""
    svg_data = None
    error = None

    if request.method == "POST":
        try:
            file = request.files.get("file")
            if file and allowed_file(file.filename):
                code = file.read().decode("utf-8")
            else:
                code = request.form.get("code", "").strip()

            if not code:
                error = "Please enter Python code or upload a .py file."
            else:
                converter = CodeToFlowchart()
                graph = converter.generate(code)
                svg_data = graph.pipe(format="svg").decode("utf-8")

        except Exception as e:
            error = f"Failed to parse the code: {str(e)}"

    return render_template("index.html", code=code, svg_data=svg_data, error=error)

if __name__ == "__main__":
    app.run(debug=True)
