--Create Lawyers table
CREATE TABLE lawyers (
    id UUID PRIMARY KEY,
    names VARCHAR(100) NOT NULL,
    lastnames VARCHAR(100) NOT NULL,
    num_cases INTEGER DEFAULT 0,
    field VARCHAR(100),
    available BOOLEAN DEFAULT TRUE,
    email VARCHAR(100) UNIQUE
);

--Create Clients table
CREATE TABLE clients (
    id UUID PRIMARY KEY,
    names VARCHAR(100) NOT NULL,
    lastname VARCHAR(100) NOT NULL,
    document_type VARCHAR(20) NOT NULL,
    document_number VARCHAR(20) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(20),
    UNIQUE (document_type, document_number)
);

--Create Cases table
CREATE TABLE cases (
    id UUID PRIMARY KEY,
    lawyer_id UUID REFERENCES lawyers(id),
    client_id UUID REFERENCES clients(id),
    title VARCHAR(200) NOT NULL,
    description TEXT,
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_updated TIMESTAMP,
    state VARCHAR(50) NOT NULL,
    priority INTEGER DEFAULT 3,
    search_vector TSVECTOR,
    FOREIGN KEY (lawyer_id) REFERENCES lawyers(id),
    FOREIGN KEY (client_id) REFERENCES clients(id)
);

--Create Receipts table
CREATE TABLE receipts (
    id UUID PRIMARY KEY,
    case_id UUID REFERENCES cases(id),
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    amount DECIMAL(10, 2) NOT NULL,
    ruc_enterprise VARCHAR(20),
    ruc_client VARCHAR(20),
    file_path VARCHAR(255),
    FOREIGN KEY (case_id) REFERENCES cases(id)
);

--Create Cases_Documents table
CREATE TABLE cases_documents (
    id UUID PRIMARY KEY,
    case_id UUID REFERENCES cases(id),
    file_path VARCHAR(255) NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (case_id) REFERENCES cases(id)
);

--Create indexes for optimization
CREATE INDEX idx_cases_search_vector ON cases USING GIN(search_vector);
CREATE INDEX idx_receipts_case_id ON receipts USING HASH(case_id);
CREATE INDEX idx_cases_client_id ON cases(client_id);
CREATE INDEX idx_cases_lawyer_id ON cases(lawyer_id);