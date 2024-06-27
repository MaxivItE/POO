from __main__ import app
from flask_sqlalchemy import SQLAlchemy

data_base = SQLAlchemy(app)

class Sucursal(data_base.Model):
    __tablename__ = 'sucursal'
    id = data_base.Column(data_base.Integer,primary_key = True)
    numero = data_base.Column(data_base.Integer,nullable = False)
    provincia = data_base.Column(data_base.String(20),nullable = False)
    localidad = data_base.Column(data_base.String(20),nullable = False)
    direccion = data_base.Column(data_base.String(50),nullable = False)

class Paquete(data_base.Model):
    __tablename__ = 'paquete'
    id = data_base.Column(data_base.Integer, primary_key = True)
    numeroenvio = data_base.Column(data_base.Integer, nullable = False)
    peso = data_base.Column(data_base.Float, nullable = False)
    nomdestinatario = data_base.Column(data_base.String(30), nullable = False)
    dirdestinatario = data_base.Column(data_base.String(50),nullable = False)
    entregado = data_base.Column(data_base.Boolean, nullable = False)
    observaciones = data_base.Column(data_base.String(100),nullable = False)
    idsucursal = data_base.Column(data_base.Integer, data_base.ForeignKey('sucursal.id'))
    idtransporte = data_base.Column(data_base.Integer, data_base.ForeignKey('repartidor.id'))
    idrepartidor = data_base.Column(data_base.Integer, data_base.ForeignKey('transporte.id'))

class Repartidor(data_base.Model):
    __tablaname__ = 'repartidor'
    id = data_base.Column(data_base.Integer, primary_key = True)
    numero = data_base.Column(data_base.Integer,nullable = False)
    nombre = data_base.Column(data_base.String(30), nullable = False)
    dni = data_base.Column(data_base.String(8), nullable = False)
    idsucursal = data_base.Column(data_base.Integer, data_base.ForeignKey('sucursal.id'))

class Transporte(data_base.Model):
    __tablaname__ = 'transporte'
    id = data_base.Column(data_base.Integer, primary_key = True)
    numerotransporte = data_base.Column(data_base.Integer, primary_key = True)
    fechahorasalida = data_base.Column(data_base.String(16), nullable = False)
    fechahorallegada = data_base.Column(data_base.String(16), nullable = False)
    idsucursal = data_base.Column(data_base.Integer, data_base.ForeignKey('sucursal.id'))