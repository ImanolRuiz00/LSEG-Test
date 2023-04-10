# -*- coding: utf-8 -*-
"""
@author: Imanol Ruiz

# localhost:5000
# Documentación Swagger: /swagger
"""

# Librerias necesarias
import config
import pandas as pd

from flask import Flask, jsonify
from datetime import datetime, timedelta
from flasgger import Swagger
from flask_restful import Api

# Instanciar la APP
app = Flask(__name__)

# Leer archivo CSV, agregando los headers
df = pd.read_csv('ListadoTest.csv', encoding="ISO-8859-1", header=None, names=['nombre','edad','pais'])
    
# Header de la documentación Swagger
template = {
  "swagger": "2.0",
  "info": {
    "title": "Swagger Test - LSEG",
    "description": """Se cuenta con un archivo archivo CSV, ruta local, con nombres, edades y país de nacimiento.
                      El desarrollo:
                          
    + Regresa una lista de los nombres ordenados por edad.
    + Genera un resumen de personas por lugar de nacimiento.
    + Genera un listado de nombres con fechas de nacimiento calculada en base a la edad.""",
    "version": "Test 3.0",
    "contact": {
      "name": "LSEG",
      "url": "https://www.lseg.com/en" }
    }
  }

# Swagger config
app.config['SWAGGER'] = {
    'title': 'LSEG API',
    'uiversion': 3,
    "specs_route": "/swagger"
}
swagger = Swagger(app, template = template)
app.config.from_object(config.Config)
api = Api(app)

# Ruta principal
@app.route('/')
def ping():
    return jsonify('Test London Stock Excgange Group - LSEG')

# Ruta para obtener nombres ordenados por edad
@app.route('/nombres_ordenados')
def get_nombres_ordenados():
    """
    Endpoint para obtener una lista de los nombres ordenados según la edad.
    ---
    tags:
        - Servicios Rest
    parameters:
        - in: Path
          name: /ListadoTest.csv
          required: true
          description: Archivo con datos a tratar.
    responses:
      200:
        description: Lista de nombres ordenados por edad.
        schema:
          type: array
          items:
            type: string
            example: Imanol Ruiz
    """
    # Ordenar nombres por edad y convertir a lista
    nombres_ordenados = df.sort_values(by='edad')['nombre'].tolist()
    
    # Retornar lista como respuesta en formato JSON
    return jsonify("Nombres Ordenados:", nombres_ordenados)


# Ruta para generar resumen por lugar de nacimiento
@app.route('/resumen_por_pais')
def get_resumen_por_pais():
    """
    Endpoint para generar una lista del resumen de personas por lugar de nacimiento.
    ---
    tags:
        - Servicios Rest
    parameters:
        - in: /ListadoTest.csv/
          name: ListadoTest
          required: true
          description: Archivo con datos a tratar.
    responses:
      200:
        description: Lista del resumen de personas por lugar de nacimiento.
        schema:
          type: array
          items:
            type: object
            properties:
              Pais:
                type: string
                example: Mexico
              Personas:
                type: integer
                example: 3
    """
    # Generar resumen por país de nacimiento
    resumen_por_pais = df.groupby('pais')['nombre'].count().reset_index()
    resumen_por_pais.columns = ['Pais', 'Cantidad de personas']
    resumen_por_pais2 = resumen_por_pais[['Pais', 'Cantidad de personas']].apply(tuple, axis=1).tolist()
    
    # Retornar resumen como respuesta en formato JSON
    return jsonify("Resumen por Pais:",resumen_por_pais2)
    # return resumen_por_pais2.to_json(orient='records')


# Ruta para generar listado de nombres con fechas de nacimiento calculadas en base a la edad
@app.route('/nombres_fechas_nacimiento')
def get_nombres_fechas_nacimiento():
    """
    Endpoint para generar una lista de nombres con fechas de nacimiento calculada según la edad.
    ---
    tags:
        - Servicios Rest
    parameters:
        - in: Path
          name: /ListadoTest.csv
          required: true
          description: Archivo con datos a tratar.
        - in: Date
          name: Fecha-Año
          description: Año actual.
          required: true
          schema:
              type: string
              format: date-time
    responses:
      200:
        description: Lista de nombres con fechas de nacimiento calculada según la edad y la fecha actual.
        schema:
          type: array
          items:
            type: object
            properties:
                Nombre:
                    type: string
                    example: Imanol Ruiz
                _Fecha Nacimiento:
                    type: integer
                    example: 2000
    """
    # Generar lista de nombres con fechas de nacimiento calculadas segun la edad
    hoy = datetime.today()
    df['fecha_nacimiento'] = df['edad'].apply(lambda x: hoy - timedelta(days=365.25*x)).dt.year
    #listado_nombres_fechas = df[['nombre', 'fecha_nacimiento']].to_dict(orient='records')
    listado_nombres_fechas = df[['nombre', 'fecha_nacimiento']].values.tolist()
    
    # Retornar listado como respuesta en formato JSON
    return jsonify("Nombres con fecha de nacimiento:", listado_nombres_fechas)

# Inicializar servidor
if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = 5000, debug=True)
