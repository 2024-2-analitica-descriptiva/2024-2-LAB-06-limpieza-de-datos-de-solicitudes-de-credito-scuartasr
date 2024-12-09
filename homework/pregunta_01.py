"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""

import pandas as pd
import unicodedata
import re
from datetime import datetime
import os

#### ========================================================
#### ========================================================
#### ========================================================

def lectura_datos(ruta: str) -> pd.DataFrame:
    """
    Esta función lee los datos que se encuentran ubicados dentro
    de un archivo CSV
    """

    df = pd.read_csv(
        ruta,
        sep = ';',
        encoding='utf-8',
        header=0,
    )

    columnas = df.columns

    return df.loc[:, columnas[1: ]]

#### ========================================================
#### ========================================================
#### ========================================================

def niveles_variable(df: pd.DataFrame, columna: str):
    """
    Esta variable devuelve los niveles de una columna de un marco
    de datos.
    """

    # for columna in df.columns:
    # print(str(columna) + ':')
    # print(df[columna].unique())
    # print("------------------------")

    return df[columna].unique()

#### ========================================================
#### ========================================================
#### ========================================================

def eliminacion_nulos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Esta función recibe un marco de datos y elimina aquellos
    registros que sean nulos
    """

    return df.dropna()

#### ========================================================
#### ========================================================
#### ========================================================

def eliminacion_espacios(texto: str) -> str:
    """
    Esta función elimnina el exceso de espacios en blanco que puedan
    tener los campos de un marco de datos.
    """

    palabras = texto.split()
    limpio = "".join(palabras)

    return limpio

#### ========================================================
#### ========================================================
#### ========================================================

def minusculas(texto: str) -> str:
    """
    Esta función convierte todo el texto en minúsculas
    """

    return str(texto).lower()

#### ========================================================
#### ========================================================
#### ========================================================

def eliminacion_puntuacion(texto: str) -> pd.DataFrame:
    """
    Esta función elimina cualquier caracter diferente a una letra o número
    """

    texto_limpio = re.sub(r'[^a-zA-Z0-9\s]', '', texto)

    return texto_limpio

#### ========================================================
#### ========================================================
#### ========================================================

def caracteres_simples(texto: str) -> str:
    """
    Esta función elimina los caracteres especiales y los reemplaza
    por su versión 'simple'. Por ejemplo, 'ü' se conviernte en 'u'
    y 'á' se convierte en 'a'
    """

    texto_normalizado = unicodedata.normalize('NFD', texto)
    texto_sin_acentos = ''.join(c for c in texto_normalizado if unicodedata.category(c) != 'Mn')
    
    return texto_sin_acentos


#### ========================================================
#### ========================================================
#### ========================================================

def correcion_fecha(fecha: str) -> pd.DataFrame:
    """
    Esta función estandariza el formato de las fechas dentro de un marco
    de datos. Para ello, identifica si la fecha está en formato
    YYYY/MM/DD o DD/MM/YYYY para realizar la respectiva corrección.

    Args:
        df: Marco de datos
        fecha: Columna que contiene las fechas
    """


    try:
        return datetime.strptime(fecha, "%Y/%m/%d")  # Intentar YYYY/MM/DD
    except ValueError:
        return datetime.strptime(fecha, "%d/%m/%Y")  # Intentar DD/MM/YYYY

#### ========================================================
#### ========================================================
#### ========================================================

def correccion_barrio(df: pd.DataFrame, barrio: str) -> pd.DataFrame:
    """
    Realiza varias correcciones de interés a una columna de un marco
    de datos de pandas

    Args:
        df: Marco de datos de pandas
        barrio: Columna

    Returns:
        Marco de datos corregido
    """
    df[barrio] = df[barrio].str.lower()
    df[barrio] = df[barrio].str.replace("_", " ")
    df[barrio] = df[barrio].str.replace("-", " ")

    return df

#### ========================================================
#### ========================================================
#### ========================================================

def correcciones_categoricas(
        df: pd.DataFrame, columna: str
) -> pd.DataFrame:
    """
    Esta función realiza correcciones comunes a variables categóricas,
    tales como: llevar todos los valores a minúsculas, eliminar algunos
    signos y remover espacios.

    Args:
        df: Marco de datos sobre el que se realizará la corrección
        columna: Columna a la que se aplicará la corrección
    """

    df[columna] = df[columna].str.lower()
    df[columna] = df[columna].str.replace("-", " ")
    df[columna] = df[columna].str.replace("_", " ")
    df[columna] = df[columna].str.replace(",", "")
    df[columna] = df[columna].str.strip()
    
    return df

#### ========================================================
#### ========================================================
#### ========================================================

def correcion_precios(
        df: pd.DataFrame, monto: str
) -> pd.DataFrame:
    """
    Se realiza la uniformización de una columna que tiene valores
    monetarios, de manera que quede únicamente como entero

    Args:
        df: Marco de datos de Pandas
        monto: Columna donde se tiene información sobre montos monetarios

    Return:
        Marco de datos de pandas corregido
    """

    df[monto] = df[monto].str.replace("$", "")
    df[monto] = df[monto].str.replace(".00", "")
    df[monto] = df[monto].str.replace(".0", "")
    df[monto] = df[monto].str.replace(",", "")
    df[monto] = df[monto].str.strip()

    return df

#### ========================================================
#### ========================================================
#### ========================================================

def guardado(df: pd.DataFrame, carpeta: str, archivo: str):
    """
    Esta carpeta guarda un elemento entregado dentro de un carpeta
    con cierto nombre de archivo.
    """

    if not os.path.exists(carpeta):
        os.makedirs(carpeta)

    ruta_archivo = os.path.join(carpeta, archivo)

    df.to_csv(ruta_archivo, index = False, sep=';')

    print('Se ha guardado en ' + ruta_archivo)


#### ========================================================
#### ========================================================
#### ========================================================

def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    -- La base tiene 225 barrios distinto corregidos

    """

    # Lectura de los datos
    ruta = './files/input/solicitudes_de_credito.csv'
    df = lectura_datos(ruta)

    # Eliminación de filas con registros nulos
    df.drop_duplicates(inplace=True)
    df = eliminacion_nulos(df)

    # Corrección de las fechas
    #df = correcion_fecha(df, 'fecha_de_beneficio')
    # df = correccion_dates(df, 'fecha_de_beneficio') # 795
    df['fecha_de_beneficio'] = df['fecha_de_beneficio'].apply(correcion_fecha)

    # Correccion de la columna barrio

    df = correccion_barrio(df, 'barrio')


    # Correcciones comunes para variables categóricas
    corregibles_object = [
        'sexo', 'tipo_de_emprendimiento', 'idea_negocio',
        'línea_credito'
    ]



    for columna in corregibles_object:
        df = correcciones_categoricas(df=df, columna=columna)
    
    # Corrección de los precios
    df = correcion_precios(df, 'monto_del_credito')

    # Nueva eliminación de duplicados
    df = df.drop_duplicates()

    folder = './files/output'
    archivo = 'solicitudes_de_credito.csv'
    guardado(df, folder, archivo)

    return df

if __name__ == '__main__':
    
    pregunta_01()
    

