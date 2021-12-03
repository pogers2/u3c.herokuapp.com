from os import error
from flask import Flask, jsonify, render_template

app = Flask(__name__, template_folder="cdn/html", static_folder="cdn")

@app.errorhandler(400)
def error400(error):
    return render_template("error.html", error_code=400, error="400 Bad Request", ctx="Bad request from client to the server."), 400

@app.errorhandler(403)
def error403(error):
    return render_template("error.html", error_code=403, error="403 Forbidden", ctx="You don't have access to this page."), 403

@app.errorhandler(404)
def error404(error):
    return render_template("error.html", error_code=404, error="404 Not Found", ctx="The page you were looking for doesn't exist."), 404

@app.errorhandler(405)
def error405(error):
    return render_template("error.html", error_code=405, error="405 Method Not Allowed", ctx="HTTP Method Not Allowed"), 405

@app.errorhandler(500)
def error500(error):
    return render_template("error.html", error_code=500, error="500 Internal Server Error", ctx="The server cannot process your request, try again later."), 500

@app.route("/")
def index():
    return render_template("index.html"), 200

@app.route("/status_code/<error_code>") # This was used to check if the status codes and context was aligned properly, I am keeping it for now but it may be removed.
def sctest(error_code=None):
    error_dict = {"400": {"error": "400 Bad Request", "ctx": "Bad request from client to the server."}, "403": {"error": "403 Forbidden", "ctx": "You don't have access to this page."}, "404": {"error": "404 Not Found", "ctx": "The page you were looking for doesn't exist."}, "405": {"error": "405 Method Not Allowed", "ctx": "HTTP Method Not Allowed"}, "500": {"error": "500 Internal Server Error", "ctx": "The server cannot process your request, try again later."}}
    if error_code is None or error_code not in error_dict:
        return render_template("error.html", error_code=404, error="404 Not Found", ctx="Error code doesn't exist, if you want an index of them go to /ext/errors"), 404
    else:
        return render_template("error.html", error_code=error_code, error=error_dict[error_code]["error"], ctx=error_dict[error_code]["ctx"]), error_code

@app.route("/ext/<path>")
def ext(path=None):
    paths = ["errors", "mods"]
    if path == None or path not in paths:
        return error404(error)
    if path == "errors":
        return jsonify({"message:": "All possible site HTTP status codes, for now.", "400": {"error": "400 Bad Request", "ctx": "Bad request from client to the server."}, "403": {"error": "403 Forbidden", "ctx": "You don't have access to this page."}, "404": {"error": "404 Not Found", "ctx": "The page you were looking for doesn't exist."}, "405": {"error": "405 Method Not Allowed", "ctx": "HTTP Method Not Allowed"}, "500": {"error": "500 Internal Server Error", "ctx": "The server cannot process your request, try again later."}})
    if path == "mods":
        return "javascript: r = new XMLHttpRequest(); r.open('GET', 'https://raw.githubusercontent.com/DarkSnakeGang/GoogleSnakeDarkMode/main/custom_color_scheme.js'); r.onload = function() { eval(this.responseText + 'snake.dark();'); }; r.send(); javascript: r = new XMLHttpRequest(); r.open('GET', 'https://raw.githubusercontent.com/DarkSnakeGang/GoogleSnakeCustomMenuStuff/main/custom.js'); r.onload = function() { eval(this.responseText + 'snake.more_menu();'); }; r.send();"
    
if __name__ == "__main__":
    app.run()