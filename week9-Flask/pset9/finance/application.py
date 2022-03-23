# TODO: conferir condições para efetuar a compra (agora, a conferencia está apenas no html e pode ser burlada) e arrumar a exibição das tabelas do index.html. Depois fazer a pagina do historico
# e adicionar alguma funcionalidade, talvez saque e deposito

import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]
    
    symbols = db.execute(
        "SELECT symbol, name, SUM(shares) as total_shares FROM transactions WHERE user_id = ? GROUP BY symbol", user_id)
    
    cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]
    
    total_money = cash
    for symbol in symbols:
        symbol_total = lookup(symbol["symbol"])["price"] * symbol["total_shares"]
        total_money += symbol_total
    
    return render_template("index.html", symbols=symbols, cash=usd(cash), lookup=lookup, usd=usd, total_money=usd(total_money))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        symbol_info = lookup(symbol)
        
        if not symbol_info:
            return apology("Please, enter a valid symbol")
            
        shares = request.form.get("shares")
        user_id = session["user_id"]
        cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]
        symbol_price = symbol_info["price"]
        symbol_name = symbol_info["name"]
        
        try:
            shares = int(shares)
        except:
            return apology("Sorry, invalid number of shares")
        
        if int(shares) <= 0:
            return apology("Sorry, invalid number of shares")
        
        total_price = symbol_price * shares
        if cash < total_price:
            return apology("Sorry, you don't have enough funds to buy this many shares")
        
        else:
            db.execute("UPDATE users SET cash = ? WHERE id = ?", cash - total_price, user_id)
            db.execute("INSERT INTO transactions (user_id, name, shares, price, type, symbol) VALUES (?, ?, ?, ?, ?, ?)",
                       user_id, symbol_name, int(shares), symbol_price, "buy", symbol)
                        
        return redirect("/")
        
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    
    history = db.execute("SELECT symbol, name, price, shares, type, time FROM transactions WHERE user_id = ?", user_id)
    
    return render_template("history.html", history=history, usd=usd)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        symbol_info = lookup(symbol)
        
        if not symbol_info:
            return apology("Please, enter a valid symbol")
        
        return render_template("quoted.html", symbol=symbol_info, usd=usd, symbol_name=symbol.upper())    
    
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        
        if not username or not password or not confirmation:
            return apology("Please fill all the fields")
            
        if password != confirmation:
            return apology("Passwords do not match!")
            
        hash_value = generate_password_hash(password)
        
        if not db.execute("SELECT username FROM users WHERE username = ?", username):
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash_value)
        else:
            return apology("Username is already registered!")
        
        return redirect("/")
        
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user_id = session["user_id"]
    
    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        shares = int(request.form.get("shares"))
        symbol_info = lookup(symbol)
        symbol_price = symbol_info["price"]
        symbol_name = symbol_info["name"]
        
        shares_owned = db.execute(
            "SELECT SUM(shares) as total_shares FROM transactions WHERE user_id = ? AND symbol = ? GROUP BY user_id", user_id, symbol)[0]["total_shares"]
        
        if shares <= 0:
            return apology("Sorry, invalid number of shares")
            
        if shares > shares_owned:
            return apology(f"Sorry, you only have {shares_owned} shares of {symbol}")
            
        sell_price = symbol_price * shares
        current_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]
        db.execute("UPDATE users SET cash = ? WHERE id = ?", current_cash + sell_price, user_id)
        db.execute("INSERT INTO transactions (user_id, name, shares, price, type, symbol) VALUES (?, ?, ?, ?, ?, ?)",
                   user_id, symbol_name, -shares, symbol_price, "sell", symbol)
                    
        return redirect("/")
        
    else:
        symbols = db.execute("SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol", user_id)
        
        return render_template("sell.html", symbols=symbols)


@app.route("/deposit", methods=["GET", "POST"])
@login_required
def deposit():
    if request.method == "POST":
        hundreds_of_thousands = request.form.get("hundreds-of-thousands")
        thousands = request.form.get("thousands")
        cents = request.form.get("cents")
        type = request.form.get("operation")

        # Check for user input errors
        if not cents:
            cents = "00"
        
        if not thousands:
            return apology("Please, insert a valid amount")
        
        elif len(hundreds_of_thousands) > 3 or len(thousands) != 3 or len(cents) != 2:
            return apology("Please, insert a valid amount")
        
        elif int(hundreds_of_thousands or thousands or cents) < 0:
            return apology("Please, insert a valid amount")
            
        elif type != ("deposit"):
            return apology("Invalid operation")
        
        user_id = session["user_id"]
        amount = f"{hundreds_of_thousands}{thousands}.{cents}"
        
        # Check operation limits
        if float(amount) < 100.00:
            return apology("Sorry, you can't deposit less than $100.00")
        
        elif float(amount) > 100000.00:
            return apology("Sorry, you can't deposit more than $100,000.00")
        
        # Store the operation infos
        session["operation"] = {"type": type, "amount": amount}
            
        return redirect("/confirmation")
        
    else:
        user_id = session["user_id"]
        cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]
        
        return render_template("deposit.html", cash=usd(cash))


@app.route("/withdraw", methods=["GET", "POST"])
@login_required
def withdraw():
    if request.method == "POST":
        hundreds_of_thousands = request.form.get("hundreds-of-thousands")
        thousands = request.form.get("thousands")
        cents = request.form.get("cents")
        type = request.form.get("operation")
        
        # Check for user input errors
        if not cents:
            cents = "00"
        
        if not thousands:
            return apology("Please, insert a valid amount")
        
        elif len(hundreds_of_thousands) > 3 or len(thousands) != 3 or len(cents) != 2:
            return apology("Please, insert a valid amount")
        
        elif int(hundreds_of_thousands or thousands or cents) < 0:
            return apology("Please, insert a valid amount")
            
        elif type != ("withdraw"):
            return apology("Invalid operation")
        
        user_id = session["user_id"]
        amount = f"{hundreds_of_thousands}{thousands}.{cents}"
        
        # Check operation limits
        if float(amount) < 100.00:
            return apology("Sorry, you can't withdraw less than $100.00")
        
        elif float(amount) > 100000.00:
            return apology("Sorry, you can't withdraw more than $100,000.00")
            
        cash = cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]
        user_id = session["user_id"]
        
        # Check if user has funds for the withdraw
        if cash < float(amount):
            return apology("Sorry! Insufficient Funds.")
        
        # Store the operation infos
        session["operation"] = {"type": type, "amount": amount}
            
        return redirect("/confirmation")
        
    else:
        user_id = session["user_id"]
        cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]
        
        return render_template("withdraw.html", cash=usd(cash))


@app.route("/confirmation", methods=["GET", "POST"])
@login_required
def confirmation():
    # Confirm deposit or withdraw
    user_id = session["user_id"]
    operation_type = session["operation"]["type"]
    amount = session["operation"]["amount"]
    
    # Confirm deposit
    if request.method == "POST" and operation_type == "deposit":
        cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash + float(amount), user_id)
        
        return redirect("/")
    
    # Confirm Withdraw
    elif request.method == "POST" and operation_type == "withdraw":
        cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash - float(amount), user_id)
        
        return redirect("/")
        
    else:
        return render_template("confirmation.html", operation_type=operation_type, amount=usd(float(amount)))


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
