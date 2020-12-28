from web import app

@app.route("/")
def hello():
    return "hello world"

if __name__ == "__main__":    
    app.run(debug=True,use_reloader=True)