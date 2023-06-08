from flask import Flask, render_template
from oauth import Oauth

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("welcome.html", discord_url=Oauth.discord_login_url)


if __name__ == "__main__":
    app.run(debug=True)
