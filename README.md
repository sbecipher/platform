# Sbecipher Platform
**Enterprise Institutional Portfolio & Order Management System**

Sbecipher is a modern, high-performance web application designed for quantitative portfolio managers and institutional traders. It was rebuilt from a legacy C# WinForms monolith (AlphaDesk) into a highly scalable Python and React stack.

## Architecture

* **Backend**: FastAPI (Python 3.10+), SQLAlchemy (PostgreSQL), Pandas (Vectorized Modeling Engine).
* **Frontend**: React 19, Vite, Zustand (State Management), React Router, TanStack Table (Virtualization), FlexLayout-React (Dockable Windows).
* **Real-time Data**: FastAPI WebSockets communicating with a custom `useWebSocket` React hook.
* **Security**: Google OAuth via `@react-oauth/google` with JSON Web Token (JWT) verification and Role-Based Access Control (RBAC).

## Features

- **Dockable Multi-Monitor UI**: Utilize `flexlayout-react` to drag and snap your Holdings Grid, Order Ticket, and Trade Blotter across screens.
- **Real-Time Market Data**: WebSockets stream live LSEG tick data directly into a virtualized TanStack table, flashing cells dynamically based on price direction.
- **Pre-Trade Compliance Engine**: A mathematical rules engine evaluating orders against the live IBOR portfolio snapshot to prevent single-stock concentration breaches prior to routing.
- **Vectorized Rebalancing**: Target weights are computed against the active portfolio using pandas to calculate exact drift and whole-share buy/sell order recommendations.
- **Role-Based Portals**: Delineated `AdminPortal` for adjusting compliance caps and FIX connections, versus a `UserPortal` and `LPStudio` for daily performance tracking.

## Getting Started

### Prerequisites
- [Node.js](https://nodejs.org/en/) (v18+)
- [Python](https://www.python.org/downloads/) (v3.10+)
- PostgreSQL (Optional: Currently mocked with in-memory execution)

### 1. Running via Docker Compose (Recommended)

The easiest way to spin up the entire application stack (PostgreSQL Database, FastAPI Backend, and Nginx/React Frontend) is via Docker Compose.

```bash
# From the root directory
docker-compose up -d --build
```
- **Frontend** will be available at: `http://localhost:8080`
- **Backend API** will be available at: `http://localhost:8000`
- **PostgreSQL** will be exposed on port `5432`

---

### 2. Running Locally (Development Mode)

If you prefer to run the services individually for active development:

#### Backend (FastAPI)

Navigate to the project root and install the python dependencies defined in `pyproject.toml`.

```bash
# It is highly recommended to use a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .

# Optional (Install dev dependencies)
pip install -e ".[dev]"

# Start the FastAPI Server
uvicorn scp_core.api.main:app --reload --port 8000
```
The backend API will be available at `http://localhost:8000`. You can view the Swagger UI documentation at `http://localhost:8000/docs`.

### 3. Running the Frontend (React / Vite)

Open a new terminal window and navigate to the `frontend` directory.

```bash
cd frontend

# Install NPM packages
npm install

# Start the Vite development server
npm run dev
```
The frontend will be available at `http://localhost:5173` (or whichever port Vite allocates).

### 4. Authentication
The application is guarded by Google OAuth. To access the platform:
1. Ensure your Google OAuth Client ID is injected in `frontend/src/App.jsx` inside the `<GoogleOAuthProvider clientId="...">` component.
2. Sign in with a valid Google account.
3. *Note*: To access the `Admin Portal`, your authenticated Google account email must contain the word `"admin"` for the Proof of Concept RBAC rules to grant you the `ADMIN` role. Otherwise, you will be routed to the standard `User Portal`.

---

*Built by the Sbecipher Engineering Team.*
