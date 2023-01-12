import datetime
from flask import Blueprint, request, render_template, redirect, url_for, flash
from app.utils.calculator import CalculadorNutricional



calculator_blueprint = Blueprint('calculator', __name__)


@calculator_blueprint.route('/form_calculator')
def form_calculator():
    return render_template('form_calculator.html')
    

@calculator_blueprint.route('/calculate', methods=["POST"])
def calculate():
    data = request.form
    calculator = CalculadorNutricional()
    result = calculator.solucion(edad=int(data.get('age', 0)), peso=float(data.get('weight', -10)))
    if result.get('message', None):
        flash(result.get('message'))
        return redirect(url_for('calculator.form_calculator'))
    print(result)
    current_date = datetime.datetime.now()   

    return render_template('result.html', result=result, name=data.get('name', ''), current_date=current_date.strftime('%d / %m / %Y'), age=int(data.get('age', 0)), weight=float(data.get('weight', -10)))