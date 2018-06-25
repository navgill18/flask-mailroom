import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session

from model import Donation, Donor 

app = Flask(__name__)

@app.route('/')
def home():
    return redirect(url_for('all'))

@app.route('/donations/')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)

@app.route('/new/', methods = ['GET', 'POST'])
def new():
	if request.method == 'POST':
		current_donor = False
		new_donor = None
		donation = float(request.form['donation'])
		donor = request.form['donor']
		for donor_name in Donor:
			if donor_name.name.strip() == donor.strip():
				current_donor = True
				new_donor = donor_name
		if not current_donor:
			new_donor = Donor(name = donor)
			new_donor.save()
		new_donation = Donation(donor = new_donor, value = donation)
		new_donation.save()
		return redirect(url_for('all'))
	else:
		return render_template('new.jinja2')

@app.route('/<d_name>/')
def specific(d_name):
	donations = Donation.select()
	return render_template('specific.jinja2', donor_name = d_name, donations = donations)

@app.route('/find/', methods = ['GET'])
def find():
	d_name = request.args.get('name', None)
	if d_name is None:
		return render_template('find.jinja2')
	else:
		return redirect(url_for('specific', d_name = d_name))



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)

