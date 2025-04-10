import requests
import pandas as pd
from io import BytesIO
from datetime import datetime
import logging
import os
from sqlalchemy import create_engine
import mysql.connector

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("fetch_and_store")

# Database configuration
DATABASE_URL = 'postgresql://admin:3qLTiZnH1cgX7a5InAryAgqqMVFXXy9d@dpg-cvlvv3u3jp1c738rf1og-a/data_excel'



def fetch_excel_data() -> pd.DataFrame:
    """Fetch and process the Excel data from Osinergmin.

    Returns:
        pd.DataFrame: DataFrame containing fuel price data

    Raises:
        Exception: If any error occurs during fetching or processing
    """
    url = "https://www.osinergmin.gob.pe/seccion/centro_documental/hidrocarburos/SCOP/SCOP-DOCS/2025/Registro-precios/Ultimos-Precios-Registrados-EVPC.xlsx"

    try:
        logger.info(f"Fetching data from {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        df = pd.read_excel(BytesIO(response.content))

        # Handle potential missing columns
        if 'FCHA_REGISTRO' not in df.columns:
            logger.error("Column 'FCHA_REGISTRO' not found in Excel file")
            raise ValueError("Formato de archivo Excel no válido: columna 'FCHA_REGISTRO' no encontrada")

        # Convert date column to standard format
        df['FCHA_REGISTRO'] = pd.to_datetime(df['FCHA_REGISTRO'], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')

        # Replace NaN values with None for proper database storage
        df = df.where(pd.notnull(df), None)

        logger.info(f"Successfully fetched {len(df)} records")
        return df

    except Exception as e:
        logger.error(f"Error fetching Excel data: {str(e)}")
        raise

def store_data(df: pd.DataFrame):
    """Store the processed data in the database.

    Args:
        df (pd.DataFrame): Processed DataFrame to store

    Raises:
        Exception: If any error occurs during database operations
    """
    try:
        # Alternativa usando mysql-connector
        connection = mysql.connector.connect(
            host="bh7114.banahosting.com",
            port=3306,
            user="fcqngeyc_adminApp",
            password="emkappprecios12",
            database="fcqngeyc_dataPricingApp",
            charset="utf8mb4"
        )
        cursor = connection.cursor()
        
        # Verificar si la tabla existe, si no crearla
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS fuel_prices (
            FCHA_REGISTRO DATETIME,
            DEPARTAMENTO VARCHAR(255),
            PROVINCIA VARCHAR(255),
            DISTRITO VARCHAR(255),
            PRODUCTO VARCHAR(255),
            PRECIO DECIMAL(10,2),
            ESTABLECIMIENTO VARCHAR(255),
            DIRECCION VARCHAR(255),
            UBIGEO VARCHAR(255),
            LATITUD DECIMAL(10,6),
            LONGITUD DECIMAL(10,6)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """)
        
        # Seleccionar solo las columnas que existen en la tabla
        required_columns = ['FCHA_REGISTRO', 'DEPARTAMENTO', 'PROVINCIA', 'DISTRITO', 
                           'PRODUCTO', 'PRECIO', 'ESTABLECIMIENTO', 'DIRECCION', 
                           'UBIGEO', 'LATITUD', 'LONGITUD']
        
        # Filtrar columnas del DataFrame
        df = df[[col for col in required_columns if col in df.columns]]
        
        # Convertir DataFrame a lista de tuplas para insertar
        data = [tuple(x) for x in df.values]
        columns = ", ".join(df.columns)
        placeholders = ", ".join(["%s"] * len(df.columns))
        
        query = f"INSERT INTO fuel_prices ({columns}) VALUES ({placeholders})"
        cursor.executemany(query, data)
        connection.commit()
        
        logger.info(f"Successfully stored {len(df)} records in database")
        cursor.close()
        connection.close()
    except Exception as e:
        logger.error(f"Error storing data: {str(e)}")
        raise

def main():
    """Main function to fetch and store data"""
    try:
        df = fetch_excel_data()
        store_data(df)
    except Exception as e:
        logger.error(f"Error in main function: {str(e)}")
        raise

if __name__ == "__main__":
    main()