# Dinner Seating Management – Backend

Backend server for managing seating arrangements for a dinner / event.  
The system is written in **Python** and was originally designed as a **microservices architecture**, with a clear separation between:

- **API Gateway** – HTTP interface for the frontend  
- **Business Logic Service** – core domain logic  
- **Database Gateway Service** – data access and integration with MongoDB  

Due to practical constraints (especially integration with **local label printers**), the current deployment runs **locally on a single machine**, but the **three-layer separation** is fully preserved in the codebase.

---

## Table of Contents

- [Architecture Overview](#architecture-overview)  
- [Tech Stack](#tech-stack)  
- [Requirements](#requirements)  
- [Project Structure](#project-structure)  
- [Configuration](#configuration)  
- [Getting Started](#getting-started)  
  - [1. Clone the repository](#1-clone-the-repository)  
  - [2. Create and activate virtual environment](#2-create-and-activate-virtual-environment)  
  - [3. Install dependencies](#3-install-dependencies)  
  - [4. Configure environment variables](#4-configure-environment-variables)  
  - [5. Run the services](#5-run-the-services)  
- [API Reference](#api-reference)  
  - [Auth & Users](#auth--users)  
  - [Guests (People)](#guests-people)  
  - [Tables](#tables)  
  - [Labels](#labels)  
- [Development Notes](#development-notes)  
- [Future Improvements](#future-improvements)  

---

## Architecture Overview

The backend server is responsible for:

- Managing **guests (people)** and their primary details  
- Managing **tables** in the event hall, including:
  - Position in the hall  
  - Shape (square / round / rectangle / special)  
  - Number of seats  
  - Gender side (men / women / mixed, if used)  
  - Rotation (for rendering on the frontend)  
- Managing **users and permissions** with JWT-based authentication  
- Communicating with a **MongoDB** database for persistence  
- Printing **LABEL stickers** for each seated participant  

### Logical Layers

Even though the system currently runs locally, it is structured as three distinct layers:

1. **API Layer (API Gateway)**  
   - Exposes REST endpoints to the React/Vite frontend  
   - Handles HTTP, authentication, and request/response mapping  

2. **Business Logic Layer**  
   - Contains the core domain logic (seating rules, validations, etc.)  
   - Orchestrates calls between API and Database Gateway  
   - Validates input and enforces business rules  

3. **Database Gateway Layer**  
   - Responsible for all communication with **MongoDB** (local or Atlas)  
   - Encapsulates queries and data access patterns  

Each layer:

- **Calls only the layer below it** to fetch or persist data  
- **Exposes functions to the layer above it** to pass data and operations upward  

Originally, each layer was intended to be deployed as a **separate microservice**, communicating via **ZeroMQ (REQ/REP)**.  
In the current phase, the services are run as **local Python processes**, but the structure allows an easy transition to true microservices if required.

---

## Tech Stack

| Area       | Technology                                                |
|-----------|-----------------------------------------------------------|
| Language  | Python (3.10+ recommended)                                |
| Backend   | Custom Python services (e.g. FastAPI / Flask – update if needed) |
| Database  | MongoDB (local instance or MongoDB Atlas)                 |
| Messaging | ZeroMQ (REQ/REP) between logical services                 |
| Auth      | JWT (JSON Web Tokens)                                     |
| Frontend  | React + Vite (separate project, not part of this repo)   |
| Printing  | Local LABEL printers (connected to the host OS)          |

---

## Requirements

> Adjust versions if needed based on your actual environment.

| Component          | Version / Recommendation          |
|--------------------|-----------------------------------|
| Python             | 3.10 or later                     |
| pip                | Latest stable version             |
| MongoDB            | 5.x / 6.x (local or Atlas)        |
| Node.js (frontend) | 18+ (for the React/Vite client)   |
| npm / pnpm / yarn  | Latest                            |
| OS                 | Windows 10/11 or Linux            |

---

## Project Structure

> Example structure – update paths/names if your folders differ.

```text
backend/
  api_gateway/
    main.py
    routers/
    models/
  business_logic/
    main.py
    services/
  db_gateway/
    main.py
    repositories/
  common/
    config/
    schemas/
  requirements.txt
  README.md
```

- `api_gateway/` – exposes HTTP endpoints, handles requests, returns JSON responses  
- `business_logic/` – core logic for seating, validations, CSV imports, etc.  
- `db_gateway/` – data access layer for MongoDB  
- `common/` – shared schemas, config utilities, and helpers  

---

## Configuration

Configuration is typically provided via environment variables (or a `.env` file).  

Suggested variables:

```env
# General
APP_ENV=development
APP_PORT=8000

# MongoDB
MONGO_URI=mongodb://localhost:27017
MONGO_DB_NAME=dinner_management

# JWT
JWT_SECRET=your-secret-key
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60

# ZeroMQ (if you separate processes)
ZMQ_API_GATEWAY_ENDPOINT=tcp://127.0.0.1:5555
ZMQ_BUSINESS_LOGIC_ENDPOINT=tcp://127.0.0.1:5556
ZMQ_DB_GATEWAY_ENDPOINT=tcp://127.0.0.1:5557

# Printing / labels (if needed)
LABEL_PRINTER_HOST=localhost
LABEL_PRINTER_PORT=9001
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/<your-user>/<your-repo>.git
cd <your-repo>/backend
```

### 2. Create and activate virtual environment

```bash
python -m venv venv
# Windows
venv\Scriptsctivate
# Linux / Mac
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the `backend` folder (or configure environment variables in your OS) according to the [Configuration](#configuration) section.

Make sure MongoDB is running and accessible using `MONGO_URI`.

### 5. Run the services

> Adjust commands according to how you actually run each layer.

Run the **Database Gateway**:

```bash
cd db_gateway
python main.py
```

Run the **Business Logic Service**:

```bash
cd ../business_logic
python main.py
```

Run the **API Gateway** (HTTP server):

```bash
cd ../api_gateway
python main.py
```

The API Gateway will usually listen on something like:

```text
http://localhost:8000
```

Update the port or host if your configuration is different.

---

## API Reference

> The tables below describe the main API endpoints.  
> Update paths, request bodies, and responses according to your actual implementation.

### Auth & Users

| Method | Path          | Description                     | Request Body (JSON)                           | Response (200)                                        |
|--------|---------------|---------------------------------|-----------------------------------------------|-------------------------------------------------------|
| POST   | `/auth/login` | Log in and receive JWT token    | `{ "username": "admin", "password": "..." }`  | `{ "access_token": "...", "token_type": "bearer" }`   |
| GET    | `/users/me`   | Get current user profile        | _JWT in Authorization header_                 | User details                                          |
| GET    | `/users`      | List all users (admin only)     | _JWT_                                         | `[{ ...user... }, ...]`                               |
| POST   | `/users`      | Create a new user               | `{ "username": "...", "password": "...", "role": "admin|user" }` | Created user object                  |

---

### Guests (People)

| Method | Path                 | Description                            | Request Body (JSON)                                         | Response (200)                     |
|--------|----------------------|----------------------------------------|-------------------------------------------------------------|------------------------------------|
| GET    | `/people`            | List all guests                        | —                                                           | `[{ ...person... }, ...]`          |
| POST   | `/people`            | Create a single guest                  | `{ "first_name": "...", "last_name": "...", ... }`          | Created person                     |
| POST   | `/people/import-csv` | Import guests from a CSV file          | _Multipart form-data with CSV file_                         | Import report (created/updated)    |
| GET    | `/people/{id}`       | Get guest by ID                        | —                                                           | Person object                      |
| PUT    | `/people/{id}`       | Update guest                           | Partial or full person fields                               | Updated person                     |
| DELETE | `/people/{id}`       | Soft delete / deactivate a guest (opt) | —                                                           | Status message                     |

---

### Tables

| Method | Path              | Description                              | Request Body (JSON)                                                                                                                   | Response (200)                          |
|--------|-------------------|------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------|
| GET    | `/tables`         | List all tables                          | —                                                                                                                                     | `[{ ...table... }, ...]`                |
| POST   | `/tables`         | Create a new table                       | `{ "name": "...", "shape": "square|round|rectangle|bima", "capacity": 12, "gender": "men|women|mixed", "x": 0, "y": 0, "rotation": 0 }` | Created table                           |
| GET    | `/tables/{id}`    | Get table by ID                          | —                                                                                                                                     | Table object                            |
| PUT    | `/tables/{id}`    | Update table data or position            | Any editable table fields                                                                                                             | Updated table                           |
| DELETE | `/tables/{id}`    | Delete table (if allowed – no occupants) | —                                                                                                                                     | Status message                          |
| GET    | `/tables/layout`  | Get full hall layout (all tables & seats)| —                                                                                                                                     | Layout structure used by the frontend   |

---

### Labels

| Method | Path                | Description                                    | Request Body (JSON)                                              | Response (200)             |
|--------|---------------------|------------------------------------------------|------------------------------------------------------------------|----------------------------|
| POST   | `/labels/print`     | Print labels for selected guests / a table     | e.g. `{ "table_id": "...", "people_ids": ["...", "..."] }`       | Status / print job result  |
| POST   | `/labels/print/all` | Print labels for all seated participants       | — or filter parameters                                           | Status / print job result  |

---

## Development Notes

- The codebase is organized by **layers** (API, Business Logic, Database Gateway) to keep a clean separation of concerns.  
- Communication between layers is done via:
  - Direct function calls (in the local version)  
  - **ZeroMQ** patterns (REQ/REP) in the microservices design  
- All database access is encapsulated inside the **Database Gateway**.  
- Logging and error handling can be centralized (for example, via a shared logger in `common/`).  

---

## Future Improvements

- Deploy each layer as a **separate microservice** (e.g. Docker containers) and use ZeroMQ or HTTP for inter-service communication.  
- Add CI/CD pipelines for automated testing and deployment.  
- Expose OpenAPI/Swagger documentation for the API Gateway.  
- Improve configuration management (e.g. dedicated config service or secrets manager).  
