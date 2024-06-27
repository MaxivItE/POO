from flask import Flask, render_template, request
from datetime import datetime


app = Flask(__name__)
app.config.from_pyfile('config.py')

from Models import data_base
from Models import Sucursal, Paquete, Transporte


@app.route('/')
def index():
    return render_template('index.html', sucursales = Sucursal.query.all())

@app.route('/despachante/<int:id_sucursal>', methods = ['GET','POST'])
def despachante(id_sucursal):
    print("ESTOY EN DESPACHANTE")
    return render_template('despachante.html', id_sucursal = id_sucursal)

@app.route('/registro_paquete/<int:id_sucursal>', methods = ['GET','POST'])
def registrar_paquete(id_sucursal):
    if request.method == 'POST':
        paquetes = Paquete.query.all()
        numeroenvio = paquetes[-1].numeroenvio + 20
        nuevo_paquete = Paquete(numeroenvio = numeroenvio, peso = request.form['peso_paquete'], nomdestinatario = request.form['nombre_destinatario'], dirdestinatario = request.form['direccion_destinatario'], entregado = False, observaciones = "", idsucursal = id_sucursal, idtransporte = 0, idrepartidor = 0)
        data_base.session.add(nuevo_paquete)
        data_base.session.commit()
        mensaje = "El paquete se registró con exito"
        return render_template('despachante.html', id_sucursal = id_sucursal, mensaje = mensaje)
    else:
        return render_template('registrar_paquete.html')

@app.route('/salida_transporte/<int:id_sucursal>', methods = ['GET','POST'])
def salida_transporte(id_sucursal):
    return render_template('salida_transporte.html', sucursales = Sucursal.query.all())

@app.route('/registrar_salida_transporte/<int:id_sucursal>', methods = ['GET','POST'])
def registrar_salida_transporte(id_sucursal):
    sucursal = Sucursal.query.get_or_404(id_sucursal)
    return render_template('registrar_salida_transporte.html', sucursal = sucursal, paquetes = Paquete.query.all())

@app.route('/registrar_transporte/<int:id_sucursal>', methods=['GET', 'POST'])
def registrar_transporte(id_sucursal):
    sucursal = Sucursal.query.get_or_404(id_sucursal)
    paquetes = Paquete.query.all()
    if request.method == 'POST':
        paquetes_seleccionados = request.form.getlist('paquetes_seleccionados')
        if not paquetes_seleccionados:
            error_seleccion = "Marque como mínimo un paquete"
            return render_template('registrar_salida_transporte.html', sucursal = sucursal, paquetes = paquetes, error_seleccion = error_seleccion)
        else:
            transportes = Transporte.query.all()
            numerotransporte = transportes[-1].numerotransporte + 1
            fecha_actual = datetime.now()
            fecha = str(fecha_actual.strftime('%Y-%m-%d '))
            hora = str(fecha_actual.strftime("%H:%M"))
            nuevo_transporte = Transporte(numerotransporte = numerotransporte, fechahorasalida = fecha + hora, fechahorallegada = 0, idsucursal = id_sucursal)
            data_base.session.add(nuevo_transporte)
            data_base.session.commit()
            mensaje = "El transporte se registró con exito"
            return render_template('despachante.html', id_sucursal = id_sucursal, mensaje = mensaje)
            
@app.route('/llegada_transporte/<int:id_sucursal>', methods = ['GET','POST'])
def llegada_transporte(id_sucursal):
    transportes = Transporte.query.all()
    return render_template('llegada_transporte.html', sucursal = Sucursal.query.get_or_404(id_sucursal), transportes = transportes)


@app.route('/registrar_llegada_transporte/<int:id_sucursal>', methods = ['GET','POST'])
def registrar_llegada_transporte(id_sucursal):
    if request.method == 'POST':
        transportes_seleccionados = request.form.getlist('transportes_seleccionados')
        if not transportes_seleccionados:
            sucursal = Sucursal.query.get_or_404(id_sucursal)
            error_seleccion = "Marque como mínimo un trasnporte"
            return render_template('llegada_transporte.html',  sucursal = sucursal, transportes = Transporte.query.all(), error_seleccion = error_seleccion)
        else:
            for id_transporte in transportes_seleccionados:
                transporte_actual = Transporte.query.filter_by(id = id_transporte).first()
                fecha_actual = datetime.now()
                fecha = str(fecha_actual.strftime('%Y-%m-%d '))
                hora = str(fecha_actual.strftime("%H:%M"))
                transporte_actual.fechahorallegada = fecha + hora
                data_base.session.commit()
                mensaje = "El horario de salida del transporte se registró con exito"
                return render_template('despachante.html', id_sucursal = id_sucursal, mensaje = mensaje)
    else:
        return render_template('registrar_llegada_transporte.html')

if __name__ == '__main__':
    app.run(debug = True)