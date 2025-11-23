from fastapi import FastAPI, Query, HTTPException
from sqlalchemy import create_engine, text
import pandas as pd

USER = 'marcin'
PASSWORD = '1234'
HOST = 'localhost'
PORT = 5432
DATABASE = 'finanse_test'

connection_url = f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'
engine = create_engine(connection_url)

app = FastAPI()

@app.get('/')
def route():
    return {'Hello': 'This is test api for gathering finance data'}

@app.get('/top_clients')
def get_top_clients(limit: int = Query(default=10, ge=1, le=100)):
    """TOP CLIENTS BY THE REVENUE"""

    query = """
    SELECT
        c.name,
        c.nip,
        c.city,
        SUM(t.cost_brutto) AS total_amount,
        COUNT(*) AS transactions,
        ROUND(AVG(t.cost_brutto), 2) AS average_transaction_amount

    FROM klienci c
    JOIN transakcje t ON c.client_id = t.client_id
    JOIN kategorie k ON t.category_id = k.category_id
    WHERE k.type = 'REVENUE'
    GROUP BY c.name, c.nip, c.city
    ORDER BY total_amount DESC
    LIMIT :limit
    """

    df = pd.read_sql(text(query), engine, params={'limit': limit})
    return df.to_dict('records')


@app.get('/clients')
def get_clients(city: str = None,
                limit: int = Query(default=100, ge=1, le=1000)):
    
    query = f"""
    SELECT *
    FROM klienci
    WHERE 1=1
    """

    if city:
        query += " AND city = :city"

    query += ' LIMIT :limit'

    df = pd.read_sql(text(query), engine, params={'city': city, 'limit': limit})
    return df.to_dict('records')


@app.get('/clients/{client_id}')
def get_client(client_id: int):
    query = """
    SELECT *
    FROM klienci
    WHERE client_id = :client_id
    """

    df = pd.read_sql(text(query), engine, params={'client_id': client_id})
    if len(df) == 0:
        raise HTTPException(status_code=404, detail=f'Client with client_id = {client_id} not exists.')
    return df.to_dict('records')


@app.get('/clients/{client_id}/transactions')
def get_transactions(client_id: int, status: str = None):

    params = {'client_id': client_id}

    query = """
    SELECT *
    FROM transakcje
    WHERE client_id = :client_id
    """

    if status:
        if status in ('Paid', 'Unpaid'):
            query += ' AND status = :status'
            params['status'] = status
        else:
            raise HTTPException(status_code=404, detail="Wrong status selected. You need to select 'Paid' or 'Unpaid'")

    df = pd.read_sql(text(query), engine, params=params)
    return df.to_dict('records')


@app.get('/reports/monthly')
def get_monthly_report(year: int = Query(default=2024, ge=2020, le=2030)):

    params = {'year': year}

    query = """
    SELECT 
        EXTRACT(YEAR FROM t.date) AS year,
        EXTRACT(MONTH FROM t.date) AS month,

        SUM(CASE WHEN k.type = 'REVENUE' THEN t.cost_netto ELSE 0 END) AS total_revenue_netto,
        SUM(CASE WHEN k.type = 'REVENUE' THEN t.cost_brutto ELSE 0 END) AS total_revenue_brutto,
        SUM(CASE WHEN k.type = 'REVENUE' THEN t.cost_vat ELSE 0 END) AS total_revenue_vat,

        SUM(CASE WHEN k.type = 'COST' THEN t.cost_netto ELSE 0 END) AS total_cost_netto,
        SUM(CASE WHEN k.type = 'COST' THEN t.cost_brutto ELSE 0 END) AS total_cost_brutto,
        SUM(CASE WHEN k.type = 'COST' THEN t.cost_vat ELSE 0 END) AS total_cost_vat,

        SUM(CASE WHEN k.type = 'REVENUE' THEN t.cost_brutto ELSE 0 END) - 
        SUM(CASE WHEN k.type = 'COST' THEN t.cost_brutto ELSE 0 END) AS balance_brutto

    FROM transakcje t
    JOIN kategorie k ON t.category_id = k.category_id
    WHERE EXTRACT(YEAR FROM t.date) = :year
    GROUP BY year, month
    """

    df = pd.read_sql(text(query), engine, params=params)
    return df.to_dict('records')