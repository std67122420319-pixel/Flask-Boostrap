from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os

app = Flask(__name__)
app.secret_key = b'hhijjohghdyuyujopi'

DATA_FILE = 'cars_data.json'

def load_cars():
  if os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
      return json.load(f)
  else:
    return [
      {'id':1, 'brand': 'Toyata', 'model': 'Yaris Ative', 'year': 2024, 'price': 620000},
      {'id':2, 'brand': 'Toyata', 'model': 'Yaris Cross', 'year': 2025, 'price': 850000},
      {'id':3, 'brand': 'Mitsubishi', 'model': 'X-Force', 'year': 2025, 'price': 860000}
    ]

def save_cars(cars_data):
  with open(DATA_FILE, 'w', encoding='utf-8') as f:
    json.dump(cars_data, f, ensure_ascii=False, indent=2)

cars = load_cars()

@app.route('/')
def index():
  return render_template('index.html',
                         title='Home Page')

@app.route('/cars')
def show_cars():
  return render_template('car/cars.html',
                         title='Cars Page',
                         cars=cars)

@app.route('/cars/new', methods=['GET', 'POST'])
def new_car():
  if request.method == 'POST':      # กด submit
    try:
      brand = request.form.get('brand', '').strip()
      model = request.form.get('model', '').strip()
      year_str = request.form.get('year', '').strip()
      price_str = request.form.get('price', '').strip()
      
      # ตรวจสอบค่าว่าง
      if not brand or not model or not year_str or not price_str:
        flash('โปรดกรอกข้อมูลทั้งหมด', 'danger')
        return redirect(url_for('new_car'))
      
      year = int(year_str)
      price = int(price_str)
    except ValueError:
      flash('ปีและราคาต้องเป็นตัวเลขเท่านั้น', 'danger')
      return redirect(url_for('new_car'))

    length = len(cars)
    if length>0:
      id = cars[length-1]['id'] + 1
    else:
      id = 1

    car = {'id':id, 'brand': brand, 'model': model, 'year': year, 'price': price}

    cars.append(car)
    save_cars(cars)
    flash('Add new car successfully', 'success')

    return redirect(url_for('show_cars'))


  return render_template('car/new_car.html',
                         title='New Car Page')

@app.route('/cars/<int:id>/delete')
def delete_car(id):
  for car in cars:
    if id == car['id']:
      cars.remove(car)
      save_cars(cars)
      flash('Delete car successfully', 'success')
      break
  
  return redirect(url_for('show_cars'))

@app.route('/cars/<int:id>/edit', methods=['GET', 'POST'])
def edit_car(id):
  car = None
  for c in cars:
    if c['id'] == id:
      car = c
      break
  
  if car is None:
    flash('Car not found', 'danger')
    return redirect(url_for('show_cars'))
  
  if request.method == 'POST':
    try:
      brand = request.form.get('brand', '').strip()
      model = request.form.get('model', '').strip()
      year_str = request.form.get('year', '').strip()
      price_str = request.form.get('price', '').strip()
      
      # ตรวจสอบค่าว่าง
      if not brand or not model or not year_str or not price_str:
        flash('โปรดกรอกข้อมูลทั้งหมด', 'danger')
        return redirect(url_for('edit_car', id=id))
      
      car['brand'] = brand
      car['model'] = model
      car['year'] = int(year_str)
      car['price'] = int(price_str)
    except ValueError:
      flash('ปีและราคาต้องเป็นตัวเลขเท่านั้น', 'danger')
      return redirect(url_for('edit_car', id=id))
    
    save_cars(cars)
    flash('Edit car successfully', 'success')
    
    return redirect(url_for('show_cars'))
  
  return render_template('car/edit_car.html',
                         title='Edit Car Page',
                         car=car)

@app.route('/cars/search')
def search_cars():
  search_query = request.args.get('search', '').lower()
  
  if search_query == '':
    filtered_cars = cars
  else:
    filtered_cars = [
      car for car in cars 
      if search_query in car['brand'].lower() or search_query in car['model'].lower()
    ]
  
  return render_template('car/cars_list.html', cars=filtered_cars)

if __name__ == '__main__':
  app.run(debug=True)