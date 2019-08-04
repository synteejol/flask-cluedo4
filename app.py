from flask import Flask, Response, redirect, url_for, request, session, abort, render_template
#from flask_login import LoginManager, UserMixin,  login_required, login_user, logout_user

import pandas as pd
from flask_table import Table, Col

app = Flask(__name__)

# config
app.config.update(
    DEBUG=True,
    SECRET_KEY='secret_xxx'
)

# # flask-login
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = "login"
#
#
# # silly user model
# class User(UserMixin):
#
#     def __init__(self, id):
#         self.id = id
#         self.name = "squadra" + str(id)
#         self.password = self.name + "_secret"
#         self.enigma = 0
#
#
#
#     def __repr__(self):
#         #return [str.self.id, self.name, self.password, str.self.enigma]
#         return "%d/%s/%s/%d" % (self.id, self.name, self.password, self.enigma)
#
#
#
# # create some users with ids 1 to 20
# users = [User(id) for id in range(1, 21) ]

#print (users[1].enigma)


# Declare your table
class ItemTable(Table):
    name = Col('Name')
    enigma = Col('Enigma')

# Get some objects
class Item(object):
    def __init__(self, name, psswd_sq, enigma):
        self.name = name
        self.enigma = enigma
        self.psswd_sq = psswd_sq
items = [Item('squadra1', 'psswd1','0'),
         Item('squadra2', 'psswd2','0'),
         Item('squadra3', 'psswd3','0'),
         Item('squadra4', 'psswd4', '0'),
         Item('squadra5', 'psswd5', '0'),
         Item('squadra6', 'psswd6', '0'),
         Item('squadra7', 'psswd7', '0'),
         Item('squadra8', 'psswd8', '0'),
         Item('squadra9', 'psswd9', '0'),
         Item('squadra10', 'psswd10', '0'),
         Item('squadra11', 'psswd11', '0'),
         Item('squadra12', 'psswd12', '0'),
         Item('squadra13', 'psswd13', '0'),
         Item('squadra14', 'psswd14', '0'),
         Item('squadra15', 'psswd15', '0'),
         Item('squadra16', 'psswd16', '0'),
         Item('squadra17', 'psswd17', '0'),
         Item('squadra18', 'psswd18', '0'),
         Item('squadra19', 'psswd19', '0'),
         Item('squadra20', 'psswd20', '0'),
         Item('squadra21', 'psswd21', '0')
         ]
# Or, equivalently, some dicts
# items = [dict(name='Name1', description='Description1'),
#          dict(name='Name2', description='Description2'),
#          dict(name='Name3', description='Description3')]

# Or, more likely, load items from your database with something like
#items = ItemModel.query.all()

# Populate the table
table = ItemTable(items)
print(items[0].name)

url2 = "https://docs.google.com/spreadsheets/d/1Ctwd5GOLggDZgRA3I5irQewttQw-a6XCqGHsmYDnnqE/export?format=csv"
# s=requests.get(url).content
data = pd.read_csv(url2)

data.set_index(['Nome Squadra'], inplace=True)
data.index.name = None



# some protected url
# @app.route('/hello/world')
# @login_required
# def home():
#     if not session.get('logged_in'): #== False  | users[session.get('i')].enigma < 1:
#         return render_template('login.html')
#     else:#if users[session.get('i')].enigma == 1:
#         i=session.get('i')
#
#         return Response("Hello World! "+session.get('username')+" "+str(users[session.get('i')].enigma))
@app.route('/tabella')
def tab():
    return Response(session.get('username')+"  ")

# somewhere to login
@app.route("/", methods=["GET", "POST"])
def login():
    session['logged_in'] = False

    #data['Enigma' + '2'][int(id) - 1] = "x"
    if request.method == 'POST':
        if request.form['action'] == 'tabella':
            return redirect(url_for('show_tables'))
        session['username'] = request.form['username']
        password = request.form['password_sq']
        id = session['username'].split('squadra')[1]
        if password == items[int(id)-1].psswd_sq and session['username'] == items[int(id)-1].name :


            session['i'] = int(id)
            items[int(id)-1].name=request.form['username']
            items[int(id)-1].enigma = "2"
            
            data['Enigma'+'2'][int(id)-1]="x"

            session['logged_in'] = True
            session['id_prev']=int(id)
            #print("id " + id)
            if request.form['action'] == 'Submit':
                return redirect(url_for('enigma2'))

            #return redirect(request.args.get("next"))

        else:

            return abort(401)
    else:
        # return Response('''
        # <form action="" method="post">
        #     <p><input type=text name=username>
        #     <p><input type=password name=password>
        #     <p><input type=submit value=Login>
        # </form>
        # ''')
        return render_template('login.html')

@app.route("/Enigma2", methods=["GET", "POST"])

def enigma2():
    if not session.get('logged_in'):
        return abort(401)
    else:

        session['logged_in_2'] = False
        if request.method == 'POST':
            if request.form['action'] == 'tabella':
                return redirect(url_for('show_tables'))
            session['username'] = request.form['username']
            password = request.form['password_sq']
            id = session['username'].split('squadra')[1]


            if password == items[int(id) - 1].psswd_sq and session['username'] == items[int(id) - 1].name and int(session['id_prev']) == int(id):
                session['i'] = int(id)
                items[int(id) - 1].name = request.form['username']

                session['logged_in_2'] = True

                print(int(items[int(id) - 1].enigma) )
                if int(items[int(id) - 1].enigma) == 2:
                    items[int(id) - 1].enigma = "3"

                data['Enigma' + '3'][int(id)-1] = "x"
                if request.form['action'] == 'Submit':
                    return redirect(url_for('enigma3'))
                # return redirect(request.args.get("next"))
            else:

                return abort(401)
        else:
            # return Response('''
            # <form action="" method="post">
            #     <p><input type=text name=username>
            #     <p><input type=password name=password>
            #     <p><input type=submit value=Login>
            # </form>
            # ''')
            return render_template('Enigma2.html')

@app.route("/Enigma2/Enigma3", methods=["GET", "POST"])
#@login_required
def enigma3():
    if not session.get('logged_in_2'):
        return abort(401)
    else:

        session['logged_in_3'] = False
        if request.method == 'POST':
            if request.form['action'] == 'tabella':
                return redirect(url_for('show_tables'))

            session['username'] = request.form['username']
            password = request.form['password_sq']
            id = session['username'].split('squadra')[1]
            if password == items[int(id) - 1].psswd_sq and session['username'] == items[int(id) - 1].name and int(session['id_prev']) == int(id):
                session['i'] = int(id)
                items[int(id) - 1].name = request.form['username']
               # items[int(id) - 1].enigma = "1"

                session['logged_in_3'] = True
                session['id_prev'] = int(id)
                if int(items[int(id) - 1].enigma) == 3:
                    items[int(id) - 1].enigma = "4"
                data['Enigma' + '4'][int(id)-1] = "x"
                if request.form['action'] == 'Submit':
                    return redirect(url_for('enigma4'))
                # return redirect(request.args.get("next"))
            else:

                return abort(401)
        else:
            # return Response('''
            # <form action="" method="post">
            #     <p><input type=text name=username>
            #     <p><input type=password name=password>
            #     <p><input type=submit value=Login>
            # </form>
            # ''')
            return render_template('Enigma3.html')




@app.route("/Enigma2/Enigma3/Enigma4", methods=["GET", "POST"])
#@login_required
def enigma4():
    if not session.get('logged_in_3'):
        return abort(401)
    else:

        session['logged_in_4'] = False
        if request.method == 'POST':
            if request.form['action'] == 'tabella':
                return redirect(url_for('show_tables'))
            session['username'] = request.form['username']
            password = request.form['password_sq']
            id = session['username'].split('squadra')[1]
            if password == items[int(id) - 1].psswd_sq and session['username'] == items[int(id) - 1].name and int(session['id_prev']) == int(id):

                session['i'] = int(id)
                items[int(id) - 1].name = request.form['username']



                session['logged_in_4'] = True
                session['id_prev'] = int(id)
                if int(items[int(id) - 1].enigma) == 4:
                    items[int(id) - 1].enigma = "5"
                data['Enigma' + '5'][int(id)-1] = "x"
                if request.form['action'] == 'Submit':
                    return redirect(url_for('enigma5'))
                # return redirect(request.args.get("next"))
            else:

                return abort(401)
        else:
            # return Response('''
            # <form action="" method="post">
            #     <p><input type=text name=username>
            #     <p><input type=password name=password>
            #     <p><input type=submit value=Login>
            # </form>
            # ''')
            return render_template('Enigma4.html')


@app.route("/Enigma2/Enigma3/Enigma4/Enigma5", methods=["GET", "POST"])
#@login_required
def enigma5():
    if not session.get('logged_in_4'):
        return abort(401)
    else:

        session['logged_in_5'] = False
        if request.method == 'POST':
            if request.form['action'] == 'tabella':
                return redirect(url_for('show_tables'))
            session['username'] = request.form['username']
            password = request.form['password_sq']
            id = session['username'].split('squadra')[1]
            if password == items[int(id) - 1].psswd_sq and session['username'] == items[int(id) - 1].name and int(session['id_prev']) == int(id):

                session['i'] = int(id)
                items[int(id) - 1].name = request.form['username']

                session['logged_in_5'] = True
                session['id_prev'] = int(id)
                print ("id "+id)
                if int(items[int(id) - 1].enigma) == 5:
                    items[int(id) - 1].enigma = "6"
                data['Enigma' + '6'][int(id)-1] = "x"
                if request.form['action'] == 'Submit':
                    return redirect(url_for('enigma6'))
                # return redirect(request.args.get("next"))
            else:

                return abort(401)
        else:
            # return Response('''
            # <form action="" method="post">
            #     <p><input type=text name=username>
            #     <p><input type=password name=password>
            #     <p><input type=submit value=Login>
            # </form>
            # ''')
            return render_template('Enigma5.html')


@app.route("/Enigma2/Enigma3/Enigma4/Enigma5/Enigma6", methods=["GET", "POST"])
#@login_required
def enigma6():
    if not session.get('logged_in_5'):
        return abort(401)
    else:

        session['logged_in_6'] = False
        if request.method == 'POST':
            if request.form['action'] == 'tabella':
                return redirect(url_for('show_tables'))
            session['username'] = request.form['username']
            password = request.form['password_sq']
            id = session['username'].split('squadra')[1]
            if password == items[int(id) - 1].psswd_sq and session['username'] == items[int(id) - 1].name and int(session['id_prev']) == int(id):

                session['i'] = int(id)
                items[int(id) - 1].name = request.form['username']

                session['logged_in_6'] = True
                session['id_prev'] = int(id)
                if int(items[int(id) - 1].enigma) == 6:
                    items[int(id) - 1].enigma = "7"
                data['Enigma' + '7'][int(id)-1] = "x"
                if request.form['action'] == 'Submit':
                    return redirect(url_for('enigma7'))
                # return redirect(request.args.get("next"))
            else:

                return abort(401)
        else:
            # return Response('''
            # <form action="" method="post">
            #     <p><input type=text name=username>
            #     <p><input type=password name=password>
            #     <p><input type=submit value=Login>
            # </form>
            # ''')
            return render_template('Enigma6.html')

@app.route("/Enigma2/Enigma3/Enigma4/Enigma5/Enigma6/Enigma7", methods=["GET", "POST"])
#@login_required
def enigma7():
    if not session.get('logged_in_6'):
        return abort(401)
    else:
        if request.method == 'POST':
            if request.form['action'] == 'tabella':
                return redirect(url_for('show_tables'))
        return render_template('Enigma7.html')

# somewhere to logout
# @app.route("/logout")
# @login_required
# def logout():
#     logout_user()
#     return Response('<p>Logged out</p>')


# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')


# callback to reload the user object
# @login_manager.user_loader
# def load_user(userid):
#     return User(userid)

@app.route("/showtable")
def show_tables():

    # url2 = "https://docs.google.com/spreadsheets/d/1Ctwd5GOLggDZgRA3I5irQewttQw-a6XCqGHsmYDnnqE/export?format=csv"
    # # s=requests.get(url).content
    # data = pd.read_csv(url2)
    #
    # data.set_index(['Nome Squadra'], inplace=True)
    # data.index.name = None

    #data['Personaggio' + session['username'].split('squadra')[1]][session['i']] = "ahahhah"
    return render_template('view.html', tables=[data.to_html(classes='tab_cluedo')],
                           # , males.to_html(classes='male')],
                           titles=['na', 'Situazione squadre'])


@app.route("/tab")
def tabella():
    return Response(table.__html__())
if __name__ == "__main__":

    app.run()