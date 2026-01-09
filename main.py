from flask import Flask, render_template , request,redirect, url_for

app = Flask(__name__)

cars = [
    {'id': 1, 'brand': 'Toyota', 'model': 'Corolla', 'year': 2020, 'price': 1500000},
    {'id': 2, 'brand': 'Honda', 'model': 'Civic', 'year': 2019, 'price': 1200000},
    {'id': 3, 'brand': 'Ford', 'model': 'Mustang', 'year': 2021, 'price': 3500000}
]

@app.route('/')
def index():
  return render_template('index.html', title="Home Page", cars=cars)

@app.route('/cars')
def show_cars():
  return render_template('car/cars.html', title="Car Page", cars=cars)

@app.route('/car/new_car', methods=['GET', 'POST'])
def new_car():
    if request.method == 'POST':
        brand = request.form['brand']
        model = request.form['model']
        year = int(request.form['year'])
        price = int(request.form['price'])

        new_id = cars[-1]['id'] + 1

        car = {
            'id': new_id,
            'brand': brand,
            'model': model,
            'year': year,
            'price': price
        }
        cars.append(car)

        return redirect(url_for('show_cars'))

    return render_template('car/new_car.html', title="New Car Page")