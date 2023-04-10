# -*- coding: utf-8 -*-
"""
@author: Imanol Ruiz
"""

import pandas as pd
from datetime import datetime, timedelta

# Leer archivo csv y agregar headers para su identificación
df = pd.read_csv('ListadoTest.csv', encoding="ISO-8859-1", header=None, names=['nombre','edad','pais'])

# Ordenar nombres por edad
nombres_ordenados = df.sort_values(by='edad')['nombre'].tolist()

# Resumen de personas por lugar de nacimiento
resumen_por_pais = df.groupby('pais')['nombre'].count().reset_index()
resumen_por_pais.columns = ['Pais', 'Cantidad de personas']

# Nombres con fechas de nacimiento calculadas en base a la edad
hoy = datetime.today()
df['fecha_nacimiento'] = df['edad'].apply(lambda x: hoy - timedelta(days=365.25*x)).dt.year
listado_nombres_fechas = df[['nombre', 'fecha_nacimiento']].values.tolist()

# Imprimir resultados
print('Nombres ordenados por edad:', nombres_ordenados)
print('Resumen por país de nacimiento:\n', resumen_por_pais)
print('Listado de nombres con fechas de nacimiento calculadas en base a la edad:', listado_nombres_fechas)

