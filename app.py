from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
@app.route("/health")
def health():
    return {"status": "ok"}


@app.route("/")
def home():
    return render_template('/home.html', title='Home Page')

@app.route("/about")
def about():
    return render_template('/about.html', title='about page')

@app.route("/estimate", methods=["POST"])
def estimate():
    print(request.form.get("email"))
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
