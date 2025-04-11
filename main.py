from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
import uuid
import os
from dotenv import load_dotenv
from models import Client, ClientCreate, Lawyer, LawyerCreate, Case, CaseCreate, Receipt, ReceiptCreate
from psycopg2.extras import register_uuid
import psycopg2
register_uuid()
load_dotenv()

app = FastAPI(title="Quick Justice API", description="API for law firm case management")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Database connection
def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "caso3"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
        cursor_factory=RealDictCursor
    )
    return conn

#Endpoints clients
@app.post("/clients/", response_model=Client)
def create_client(client: ClientCreate):
    conn = get_db_connection()
    cur = conn.cursor()
    client_id = uuid.uuid4()
    try:
        cur.execute(
            """
            INSERT INTO clients (id, names, lastname, document_type, document_number, email, phone)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING *
            """,
            (client_id, client.names, client.lastname, client.document_type, 
             client.document_number, client.email, client.phone)
        )
        new_client = cur.fetchone()
        conn.commit()
        return new_client
    except psycopg2.IntegrityError as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Client with this document already exists")
    finally:
        cur.close()
        conn.close()

@app.get("/clients/", response_model=List[Client])
def read_all_clients():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM clients ORDER BY lastname, names")
        clients = cur.fetchall()
        return clients
    finally:
        cur.close()
        conn.close()

@app.get("/clients/{client_id}", response_model=Client)
def read_client(client_id: str):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM clients WHERE id = %s", (client_id,))
        client = cur.fetchone()
        if client is None:
            raise HTTPException(status_code=404, detail="Client not found")
        return client
    finally:
        cur.close()
        conn.close()

@app.get("/lawyers/", response_model=List[Lawyer])
def read_all_lawyers():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM lawyers ORDER BY lastnames, names")
        lawyers = cur.fetchall()
        return lawyers
    finally:
        cur.close()
        conn.close()

#Endpoints Lawyer
@app.post("/lawyers/", response_model=Lawyer)
def create_lawyer(lawyer: LawyerCreate):
    conn = get_db_connection()
    cur = conn.cursor()
    lawyer_id = uuid.uuid4()
    try:
        cur.execute(
            """
            INSERT INTO lawyers (id, names, lastnames, field, email)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING *
            """,
            (lawyer_id, lawyer.names, lawyer.lastnames, lawyer.field, lawyer.email)
        )
        new_lawyer = cur.fetchone()
        conn.commit()
        return new_lawyer
    except psycopg2.IntegrityError as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Lawyer with this email already exists")
    finally:
        cur.close()
        conn.close()

@app.get("/lawyers/{lawyer_id}", response_model=Lawyer)
def read_lawyer(lawyer_id: str):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM lawyers WHERE id = %s", (lawyer_id,))
        lawyer = cur.fetchone()
        if lawyer is None:
            raise HTTPException(status_code=404, detail="Lawyer not found")
        return lawyer
    finally:
        cur.close()
        conn.close()

#Endpoints case
@app.post("/cases/", response_model=Case)
def create_case(case: CaseCreate):
    conn = get_db_connection()
    cur = conn.cursor()
    case_id = uuid.uuid4()
    try:
        cur.execute("SELECT 1 FROM lawyers WHERE id = %s", (case.lawyer_id,))
        if not cur.fetchone():
            raise HTTPException(status_code=404, detail="Lawyer not found")
        
        cur.execute("SELECT 1 FROM clients WHERE id = %s", (case.client_id,))
        if not cur.fetchone():
            raise HTTPException(status_code=404, detail="Client not found")
        
        cur.execute(
            """
            INSERT INTO cases (id, lawyer_id, client_id, title, description, state, priority)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING *
            """,
            (case_id, case.lawyer_id, case.client_id, case.title, 
             case.description, case.state, case.priority)
        )
        new_case = cur.fetchone()
        
        cur.execute(
            "UPDATE lawyers SET num_cases = num_cases + 1 WHERE id = %s",
            (case.lawyer_id,)
        )
        
        conn.commit()
        return new_case
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()

@app.get("/cases/", response_model=List[Case])
def read_all_cases():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT c.*, 
                   cl.names as client_names, cl.lastname as client_lastname,
                   l.names as lawyer_names, l.lastnames as lawyer_lastnames
            FROM cases c
            JOIN clients cl ON c.client_id = cl.id
            JOIN lawyers l ON c.lawyer_id = l.id
            ORDER BY c.date_created DESC
        """)
        cases = cur.fetchall()
        return cases
    finally:
        cur.close()
        conn.close()

@app.get("/cases/{case_id}", response_model=Case)
def read_case(case_id: str):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM cases WHERE id = %s", (case_id,))
        case = cur.fetchone()
        if case is None:
            raise HTTPException(status_code=404, detail="Case not found")
        return case
    finally:
        cur.close()
        conn.close()

#Endpoints receipts
@app.post("/receipts/", response_model=Receipt)
def create_receipt(receipt: ReceiptCreate):
    conn = get_db_connection()
    cur = conn.cursor()
    receipt_id = uuid.uuid4()
    try:
        cur.execute("SELECT 1 FROM cases WHERE id = %s", (receipt.case_id,))
        if not cur.fetchone():
            raise HTTPException(status_code=404, detail="Case not found")
        
        cur.execute(
            """
            INSERT INTO receipts (id, case_id, amount, ruc_enterprise, ruc_client)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING *
            """,
            (receipt_id, receipt.case_id, receipt.amount, 
             receipt.ruc_enterprise, receipt.ruc_client)
        )
        new_receipt = cur.fetchone()
        conn.commit()
        return new_receipt
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()

@app.get("/receipts/{receipt_id}", response_model=Receipt)
def read_receipt(receipt_id: str):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM receipts WHERE id = %s", (receipt_id,))
        receipt = cur.fetchone()
        if receipt is None:
            raise HTTPException(status_code=404, detail="Receipt not found")
        return receipt
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)