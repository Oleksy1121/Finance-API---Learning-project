# Finance API - Learning Project

REST API for financial data management built with FastAPI and PostgreSQL.

## 📋 Description

This project was created as a learning exercise to understand REST API development, database integration, and modern Python web frameworks. The API manages financial data including clients, transactions, and generates various financial reports with proper data validation and security practices.

## 🚀 Tech Stack

- **FastAPI** - Modern, fast web framework for building APIs
- **PostgreSQL** - Relational database for data storage
- **SQLAlchemy** - SQL toolkit and ORM for database operations
- **pandas** - Data analysis and manipulation
- **Pydantic** - Data validation using Python type hints

## ✨ Features

- 📊 Client management with filtering capabilities
- 💰 Transaction tracking and analysis
- 📈 Monthly financial reports (revenue vs costs with balance)
- 🏆 TOP clients ranking by revenue
- 🔒 Parameterized SQL queries for injection protection
- ✅ Input validation with Pydantic Query
- 📚 Auto-generated interactive API documentation (Swagger UI)

## 🔧 API Endpoints

### Clients
| Method | Endpoint | Description | Query Params |
|--------|----------|-------------|--------------|
| GET | `/clients` | List all clients | `city` (optional), `limit` (1-1000, default: 100) |
| GET | `/clients/{client_id}` | Get specific client details | - |
| GET | `/clients/{client_id}/transactions` | Get client's transactions | `status` (Paid/Unpaid, optional) |

### Reports
| Method | Endpoint | Description | Query Params |
|--------|----------|-------------|--------------|
| GET | `/top_clients` | TOP clients by revenue | `limit` (1-100, default: 10) |
| GET | `/reports/monthly` | Monthly financial summary | `year` (2020-2030, default: 2024) |

### General
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API welcome message |

## 📦 Installation

### Prerequisites
- Python 3.8+
- PostgreSQL 12+

### Setup

1. **Clone the repository:**
```bash
git clone https://github.com/your-username/finance-api-learning.git
cd finance-api-learning
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure database:**
   - Create PostgreSQL database named `finanse_test`
   - Update connection details in `finanse.py` if needed
   - Set up required tables: `klienci`, `transakcje`, `kategorie`

5. **Run the API:**
```bash
uvicorn finanse:app --reload
```

6. **Access the API:**
   - API: `http://localhost:8000`
   - Interactive docs: `http://localhost:8000/docs`
   - Alternative docs: `http://localhost:8000/redoc`

## 📊 Database Schema

The project uses PostgreSQL with three main tables:

- **klienci** (clients): Client information including name, NIP, city
- **transakcje** (transactions): Financial transactions with amounts, dates, status
- **kategorie** (categories): Transaction categories (REVENUE/COST types)

## 💡 Example Usage

### Get TOP 5 clients by revenue:
```bash
curl http://localhost:8000/top_clients?limit=5
```

### Get clients from Warsaw:
```bash
curl http://localhost:8000/clients?city=Warszawa
```

### Get unpaid transactions for client #5:
```bash
curl http://localhost:8000/clients/5/transactions?status=Unpaid
```

### Get monthly report for 2024:
```bash
curl http://localhost:8000/reports/monthly?year=2024
```

## 🎯 Learning Goals

Through this project, I learned:
- ✅ REST API design principles and best practices
- ✅ FastAPI framework features (routing, validation, documentation)
- ✅ SQL query optimization with pandas integration
- ✅ Parameterized queries (`:param` syntax) for SQL injection prevention
- ✅ Input validation using Pydantic Query with constraints (ge, le)
- ✅ Error handling with proper HTTP status codes
- ✅ Database connection management with SQLAlchemy
- ✅ API documentation with OpenAPI/Swagger

## 🔐 Security Features

- **Parameterized SQL queries**: All user inputs use `:param` syntax to prevent SQL injection
- **Input validation**: Pydantic Query validates all parameters (ranges, types)
- **Error handling**: Proper HTTP status codes (404, 422) for different error scenarios
- **SQL text() wrapper**: SQLAlchemy text() for safe query execution

## 📈 Key Technical Decisions

### Why parameterized queries?
Instead of f-strings, I use `:param` syntax with SQLAlchemy's `text()` function to safely pass user input to SQL queries, preventing injection attacks.

### Why pandas for data retrieval?
pandas provides excellent DataFrame operations and easy conversion to JSON format for API responses, plus powerful data manipulation capabilities.

### Why Pydantic Query?
Automatic validation of query parameters reduces boilerplate code and ensures data integrity before database queries.

## 🚀 Future Improvements

- [ ] Add JWT authentication for protected endpoints
- [ ] Implement user management system
- [ ] Add data export functionality (Excel/CSV)
- [ ] Write unit tests with pytest
- [ ] Add pagination for large result sets
- [ ] Deploy to cloud platform (Railway/Render)
- [ ] Add caching layer (Redis) for frequently accessed reports
- [ ] Implement rate limiting
- [ ] Add logging and monitoring

## 🛠️ Development

### Project structure:
```
finance-api-learning/
├── finanse.py              # Main API application
├── 01-finanse.ipynb        # Data analysis notebook
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

### Running in development mode:
```bash
uvicorn finanse:app --reload --host 0.0.0.0 --port 8000
```

## 📝 Notes

- This is a **learning project** created to practice FastAPI and database integration
- Database credentials are currently hardcoded - in production, use environment variables
- The project includes a Jupyter notebook (`01-finanse.ipynb`) with data analysis examples

## 👤 Author

**Marcin** - Aspiring Python Developer

Learning focus: Backend development, FastAPI, PostgreSQL, Data Analysis

## 📄 License

This project is created for educational purposes. Feel free to use it as a learning resource.

---

**Built with ❤️ while learning FastAPI and PostgreSQL**