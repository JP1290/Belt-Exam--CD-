from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.dealz_model import Dealz



@app.route('/dashboard') #Get request for 127.0.0.1:5000
def dashboard():
    return render_template('dealz.html', dealz = Dealz.get_dealz_from_user(), user_id = session['user_id'], first_name = session['users'])

@app.route('/new')
def new():
    return render_template('/sellcar.html')

@app.route('/create', methods = ['POST'])
def sell():
    if not Dealz.validate_dealz(request.form):
        return redirect('/new')
    data = {
        'price': request.form['price'],
        'model': request.form['model'],
        'make': request.form['make'],
        'year': request.form['year'],
        'description': request.form['description'],
        'id': session['user_id']
    }
    Dealz.save_dealz(data)
    return redirect('/dashboard')

@app.route('/show/<int:id>')
def this_deal(id):
    data = {
        'id': id
    }
    return render_template('specific_dealz.html', dealz = Dealz.get_dealz_by_user_id(data), first_name = session['user'])

@app.route('/edit/<int:id>')
def edit(id):
    session['idk'] = id
    data = {
        'id': id
    }
    return render_template('editdealz.html', dealz = Dealz.get_dealz_by_user_id(data))

@app.route('/editing', methods = ['POST'])
def edit_method():
    if not Dealz.validate_dealz(request.form):
        return redirect('/edit/' + str(session['idk']))
    data = {
        'price': request.form['price'],
        'model': request.form['model'],
        'make': request.form['make'],
        'year': request.form['year'],
        'description': request.form['description'],
        'id': session['idk']
    }
    Dealz.update_dealz(data)
    return redirect('/dashboard')

@app.route('/delete/<int:id>')
def delete_deal(id):
    deal_id = {
        'id': id
    }
    Dealz.delete_dealz(deal_id)
    return redirect('/dashboard')

@app.route('/sold/<int:id>')
def sold(id):
    deal_id = {
        'id': id
    }
    Dealz.delete_dealz(deal_id)
    return redirect('/dashboard')