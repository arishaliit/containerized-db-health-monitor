# 🧠 Containerized Database Health Monitor with CI/CD

This project provides a robust, portable, and automated solution for monitoring the health and performance of a PostgreSQL database. It demonstrates practical usage of containerization, shell scripting, Python programming, and CI/CD practices via GitHub Actions.

---

## 🌟 Project Goal

Create a self-contained monitoring system that:

- ✅ Proactively validates database health  
- ⚠️ Detects operational issues early  
- 💡 Supports system stability in production environments

---

## ✨ Key Features

- **Containerized Database**  
  Spins up an isolated PostgreSQL instance using Docker Compose for consistent testing and development.

- **Python-Based Health Checks**  
  A Python script (`monitor.py`) performs:
  - Connection verification  
  - Row count checks (e.g., `users` table)  
  - Timestamp check of last log entry  
  - NULL value checks in critical columns

- **Automated Orchestration**  
  `run_monitor.sh`:
  - Starts containers  
  - Waits until DB is healthy  
  - Runs health checks  
  - Shuts down containers cleanly

- **CI/CD Integration (GitHub Actions)**  
  Automates daily and per-push health checks via `.github/workflows/main.yml`

- **Clear Logging**  
  All results output clearly with success, warning, or error flags

---

## 🛠️ Technologies Used

| Technology        | Purpose                                         |
|------------------|-------------------------------------------------|
| **Python**        | Core monitoring logic (`psycopg2-binary`)       |
| **PostgreSQL**    | Target database                                 |
| **Docker**        | Containerization of services                    |
| **Docker Compose**| Multi-container orchestration                   |
| **Shell Scripting**| Local automation of health check execution     |
| **GitHub Actions**| CI/CD workflow automation                       |
| **SQL**           | Schema definition and query logic               |

---

## 🚀 Getting Started

### 🔧 Prerequisites

- **Docker Desktop / Engine**  
  [Download Docker](https://www.docker.com/products/docker-desktop)  
  > Enable WSL 2 integration if using Windows

- **Python**  
  [Download Python](https://www.python.org/downloads/)  
  > ✅ Add Python to `PATH` during install

- **Git / Git Bash**  
  [Download Git](https://git-scm.com/downloads)  
  > Use Git Bash on Windows for terminal consistency

---

### ⚙️ Installation & Setup

```bash
git clone https://github.com/arishaliit/containerized-db-health-monitor.git
cd containerized-db-health-monitor
chmod +x run_monitor.sh
.
├── .github/
│   └── workflows/
│       └── main.yml          # GitHub Actions workflow
├── db/
│   └── init.sql              # SQL script for DB schema + dummy data
├── monitor.py                # Python script for DB health checks
├── run_monitor.sh            # Shell script for orchestration
├── Dockerfile                # Defines monitor container build
├── docker-compose.yml        # Services: db + monitor
└── README.md                 # Project documentation
```

### 🏃 Local Usage
To run locally:
- Ensure Docker Desktop is running
- From the project root, run:
```
./run_monitor.sh
```
