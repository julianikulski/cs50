import os
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
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


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    try:
        # select current users remaining cash balance
        user_remain_cash = db.execute("SELECT cash FROM users WHERE id = :userid",
                                      userid=session["user_id"])

        user_remain_cash = user_remain_cash[0]["cash"]

        # select all shares the user ever bought
        ever_bought = db.execute("SELECT DISTINCT symbol FROM history WHERE userid = :userid",
                                 userid=session["user_id"])

        # check how many shares were bought and store results in form of dictionary
        stock_current_shares = {}
        for item in ever_bought:
            for key in item.values():
                bought_in_total = db.execute("SELECT SUM(shares) FROM history WHERE action = :action AND userid = :userid AND symbol = :stocks_bought",
                                             userid=session["user_id"], action="buy", stocks_bought=key)
                sold_in_total = db.execute("SELECT SUM(shares) FROM history WHERE action = :action AND userid = :userid AND symbol = :stocks_sold",
                                           userid=session["user_id"], action="sell", stocks_sold=key)

                # how many shares were bought in total
                bought_in_total = bought_in_total[0]["SUM(shares)"]

                # how many shares were sold in total
                sold_in_total = sold_in_total[0]["SUM(shares)"]

                if sold_in_total == None:
                    sold_in_total = 0
                else:
                    pass

                # if there is currently at least 1 share held of a particular stock, add the symbol to a dictionary
                if bought_in_total - sold_in_total > 0:
                    current_number_shares = bought_in_total - sold_in_total
                    stock_current_shares[key] = current_number_shares

        # list of number of shares of stocks currently held
        list_stock_current_shares = list(stock_current_shares.values())

        # for all shares that are currently held, check the current price
        list_currently_held_stocks = list(stock_current_shares.keys())
        current_price_holdings = {}
        current_price_holdings_usd = {}
        for share in list_currently_held_stocks:
            current_price_holdings[share] = lookup(share)["price"]
            current_price_holdings_usd[share] = usd(lookup(share)["price"])
        list_prices_no_usd = list(current_price_holdings.values())
        list_prices = list(current_price_holdings_usd.values())

        # total value of all shares of a stock
        total_for_stocks = {}
        for stocks in list_currently_held_stocks:
            total_for_stocks[stocks] = stock_current_shares[stocks] * current_price_holdings[stocks]

        # total value of all current holdings and cash
        list_total_stocks = list(total_for_stocks.values())
        total = user_remain_cash + sum(list_total_stocks)

        # name of all current holdings
        list_name = []
        for name in list_currently_held_stocks:
            list_name.append(lookup(name)["name"])

        # total value of shares * current prices
        total_per_stock = []
        for j in range(len(list_prices)):
            total_per_stock.append(usd(list_prices_no_usd[j] * list_stock_current_shares[j]))

        # return index.html template with all relevant inputs
        return render_template("index.html", total=usd(total), user_remain_cash=usd(user_remain_cash), symbol=list_currently_held_stocks, name=list_name, shares=list_stock_current_shares, prices=list_prices, total_stocks=total_per_stock)

    except (RuntimeError, NameError):
        return render_template("index.html", total=usd(10000), user_remain_cash=usd(10000), symbol="", name="", shares="", prices="")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":
        # check if stock symbol exists
        try:
            check_symbol = lookup(request.form.get("symbol"))["symbol"]
        except:
            return apology("Stock symbol does not exist", 400)

        # check if number of shares entered is positive, not fractional and numeric
        number_shares = request.form.get("shares")

        try:
            int(number_shares)
        except ValueError:
            return apology("Positive, non-fractional number needs to be entered", 400)
        else:
            if int(float(number_shares)) < 0:
                return apology("Positive, non-fractional number needs to be entered", 400)

            # check price of stock
            check_price = lookup(request.form.get("symbol"))["price"]

            # show name of stock
            stock_name = lookup(request.form.get("symbol"))["name"]

            # check how much cash the user currently has
            remain_cash = db.execute("SELECT cash FROM users WHERE id = :userid",
                                     userid=session["user_id"])
            remain_cash = remain_cash[0]["cash"]

            # convert timestamp of purchase from epoch to regular datetime format
            timestamp = datetime.datetime.now().strftime("%a, %d %b %Y %H:%M%p")

            # create new table to keep track of the purchase
            db.execute("CREATE TABLE IF NOT EXISTS history (id INTEGER NOT NULL PRIMARY KEY, userid INTEGER NOT NULL, timestamp TIMESTAMP NOT NULL, action TEXT NOT NULL, symbol TEXT NOT NULL, stock TEXT NOT NULL, shares INTEGER NOT NULL, price REAL NOT NULL)")

            # create new table to keep track of current holdings and cash
            db.execute("CREATE TABLE IF NOT EXISTS portfolio (id INTEGER NOT NULL PRIMARY KEY, userid INTEGER NOT NULL, symbol TEXT NOT NULL, shares INTEGER NOT NULL)")

            # check whether user has enough cash to buy the stock
            if float(remain_cash) >= check_price * int(number_shares):
                db.execute("UPDATE users SET cash = :cash WHERE id = :user_id",
                           cash=remain_cash - check_price * int(number_shares), user_id=session["user_id"])
                db.execute("INSERT INTO history (userid, timestamp, action, symbol, stock, shares, price) VALUES (:userid, :timestamp, :action, :symbol, :stock, :shares, :price)",
                           userid=session["user_id"], timestamp=timestamp, action="buy", symbol=check_symbol, stock=stock_name, shares=int(number_shares), price=check_price)

                # add or update current number of shares held of that particular stock
                current = db.execute("SELECT COUNT(*) FROM portfolio WHERE id = :userid AND symbol = :symbol",
                                     userid=session["user_id"], symbol=check_symbol)

                if current[0]["COUNT(*)"] > 0:
                    current_shares = db.execute("SELECT shares FROM portfolio WHERE userid = :userid AND symbol = :symbol",
                                                userid=session["user_id"], symbol=check_symbol)
                    db.execute("UPDATE portfolio SET shares = :shares WHERE userid = :userid AND symbol = :symbol",
                               userid=session["user_id"], symbol=check_symbol, shares=current_shares[0]["shares"] + int(number_shares))
                else:
                    db.execute("INSERT INTO portfolio (userid, symbol, shares) VALUES (:userid, :symbol, :shares)",
                               userid=session["user_id"], symbol=check_symbol, shares=int(number_shares))

                return redirect("/")

            # render an apology if cash does not suffice to buy the stock
            else:
                return apology("Not enough cash to execute transation", 400)

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # extract all relevant columns from history table in database

    everything = db.execute("SELECT symbol, shares, action, timestamp, price FROM history")

    return render_template("history.html", everything=everything)


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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

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

        # lookup the price of the stock
        checked_price = lookup(request.form.get("symbol"))
        # return apology if stock symbol does not exist
        if not checked_price:
            return apology("Stock symbol does not exist", 400)
        # load quoted.html with the name, symbol and price of the stock
        else:
            return render_template("quoted.html", name=checked_price["name"], symbol=checked_price["symbol"], price=usd(checked_price["price"]))
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was added
        if not request.form.get("username"):
            return apology("username cannot be blank", 400)

        # Query database for username
        existing_un = db.execute("SELECT * FROM users WHERE username = :username",
                                 username=request.form.get("username"))

        # Ensure that username does not already exist
        if existing_un:
            return apology("username already exists", 400)

        # Ensure password was provided
        elif not request.form.get("password"):
            return apology("password must be provided", 400)

        # Ensure confirmation matches password
        elif not request.form.get("confirmation") or request.form.get("password") != request.form.get("confirmation"):
            return apology("the two password entries do not match", 400)

        # Hash the password to protect it and add username and password to the database
        add_row = db.execute("INSERT INTO users (username, hash) VALUES (:username, :password)",
                             username=request.form.get("username"),
                             password=generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8))

        # Login user automatically
        session["user_id"] = db.execute("SELECT id FROM users WHERE username = :username",
                                        username=request.form.get("username"))
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # check if number of shares entered is positive, not fractional and numeric
        number_shares = request.form.get("shares")

        try:
            int(number_shares)
        except ValueError:
            return apology("Positive, non-fractional number needs to be entered", 400)
        else:
            if int(float(number_shares)) < 0:
                return apology("Positive, non-fractional number needs to be entered", 400)

            # check price of stock
            check_price = lookup(request.form.get("symbol"))["price"]

            check_symbol = lookup(request.form.get("symbol"))["symbol"]

            stock_name = lookup(request.form.get("symbol"))["name"]

            # check how much cash the user currently has
            remain_cash = db.execute("SELECT cash FROM users WHERE id = :userid",
                                     userid=session["user_id"])

            remain_cash = remain_cash[0]["cash"]

            # convert timestamp of purchase from epoch to regular datetime format
            timestamp = datetime.datetime.now().strftime("%a, %d %b %Y %H:%M%p")

            # check how many shares are held of a particular stock
            number_shares_db = db.execute("SELECT shares FROM portfolio WHERE userid = :userid AND symbol = :symbol",
                                          userid=session["user_id"], symbol=check_symbol)

            # add information to portfolio table
            if number_shares_db[0]["shares"] >= int(number_shares):

                # if shares will be updated to 0, remove the row entirely from the portfolio table
                if (number_shares_db[0]["shares"] - int(number_shares)) == 0:

                    # delete entry in portfolio if 0 shares are now held of stock
                    db.execute("DELETE FROM portfolio WHERE symbol = :symbol AND id = :userid",
                               userid=session["user_id"], symbol=check_symbol)
                else:
                    # otherwise update the number of shares by current_shares - shares to be sold
                    db.execute("UPDATE portfolio SET shares = :shares WHERE id = :userid AND symbol = :symbol",
                               userid=session["user_id"], symbol=check_symbol, shares=number_shares_db[0]["shares"] - int(number_shares))

                # update user's cash
                db.execute("UPDATE users SET cash = :cash WHERE id = :user_id",
                           cash=remain_cash + check_price * int(number_shares), user_id=session["user_id"])

                # enter transaction to history table
                db.execute("INSERT INTO history (userid, timestamp, action, symbol, stock, shares, price) VALUES (:userid, :timestamp, :action, :symbol, :stock, :shares, :price)",
                           userid=session["user_id"], timestamp=timestamp, action="sell", symbol=check_symbol, stock=stock_name, shares=int(number_shares), price=check_price)

            else:
                return apology("You do not hold enough shares to execute this transaction")

            return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:

        # try whether there is any data in the table portfolio
        try:
            all_stocks = db.execute("SELECT symbol FROM portfolio")

        # if no data is available then show below string on sell.html page
        except:
            symbol_except = []
            symbol_except.append("No stocks currently held")

        # if stocks are held, show these on sell.html page
        else:
            list_all_stocks = []
            for key in all_stocks:
                part_stock = key["symbol"]
                list_all_stocks.append(part_stock)

        # then render the sell.html page with the above mentioned selection options
        if all_stocks[0]["symbol"] != None:
            return render_template("sell.html", symbol=list_all_stocks)
        else:
            return render_template("sell.html", symbol=symbol_except)


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
