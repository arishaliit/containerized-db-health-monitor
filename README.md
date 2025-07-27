Containerized Database Health Monitor with CI/CD
This project provides a robust and automated solution for monitoring the health and basic performance of a PostgreSQL database. It demonstrates a practical application of containerization, shell scripting, Python programming, and continuous integration/continuous deployment (CI/CD) practices using GitHub Actions.

🌟 Project Goal
The primary goal of this project is to create a portable and automated system that can proactively check the operational status and key metrics of a database. This ensures early detection of potential issues, contributing to system stability and reliability in critical environments.

✨ Key Features
Containerized Database: Utilizes Docker Compose to spin up an isolated PostgreSQL database instance for testing and development, ensuring a consistent environment.

Python-Based Health Checks: A Python script connects to the database and performs a series of essential health checks, including:

Basic connection verification.

Table row count checks (e.g., users table).

Timestamp of the last log entry.

Basic data integrity checks (e.g., checking for NULL values in critical columns).

Automated Orchestration: A shell script (run_monitor.sh) orchestrates the entire process, from starting the database to executing the monitoring script, and gracefully shutting down containers. It includes a robust waiting mechanism to ensure the database is ready before checks begin.

CI/CD Integration (GitHub Actions): An automated workflow on GitHub Actions triggers the health checks on every push to the main branch and on a daily schedule, providing continuous validation of the monitoring system and the database's health.

Clear Logging: Provides informative console output for each check, indicating success, warnings, or errors.

🛠️ Technologies Used
Python: For the core monitoring logic and database interaction (psycopg2-binary).

PostgreSQL: The target database for health monitoring.

Docker: For containerizing both the database and the Python monitoring application.

Docker Compose: For defining and running multi-container Docker applications.

Shell Scripting (Bash): For local orchestration and automation of the Docker Compose commands.

GitHub Actions: For implementing automated CI/CD workflows to run the health checks.

SQL: For database schema definition and health check queries.

🚀 Getting Started
Follow these steps to set up and run the project on your local machine.

Prerequisites
Ensure you have the following installed on your system:

Docker Desktop (for Windows/macOS) or Docker Engine (for Linux):

Download Docker Desktop

Ensure Docker Desktop is running and WSL 2 integration is enabled for your Linux distribution if on Windows.

Python:

Download Python

Important: During installation, check the box to "Add Python to PATH".

Git for Windows (Includes Git Bash) / Git (for macOS/Linux):

Download Git

On Windows, use Git Bash as your terminal for this project for consistent command execution.

Installation & Setup
Clone the Repository:

git clone https://github.com/YOUR_GITHUB_USERNAME/containerized-db-health-monitor.git
cd containerized-db-health-monitor

(Replace YOUR_GITHUB_USERNAME with your actual GitHub username).

Make the Orchestration Script Executable:

chmod +x run_monitor.sh

Project Structure
.
├── .github/
│   └── workflows/
│       └── main.yml        # GitHub Actions workflow for automated checks
├── db/
│   └── init.sql            # SQL script to initialize DB schema and dummy data
├── monitor.py              # Python script for database health checks
├── run_monitor.sh          # Shell script to orchestrate local execution
├── Dockerfile              # Defines how the 'monitor' container is built
├── docker-compose.yml      # Defines the 'db' and 'monitor' services
└── README.md               # Project documentation

🏃 Local Usage
To run the database health monitor on your local machine:

Ensure Docker Desktop is running.

Execute the main script from your project root directory:

./run_monitor.sh

This script will:

Stop and remove any previous containers and the db_data volume to ensure a clean database initialization.

Build the monitor Docker image (if not cached).

Start the db (PostgreSQL) and monitor containers.

Wait for the db container to become healthy.

Execute the monitor.py script inside the monitor container.

Display the health check results in your terminal.

Stop and remove both containers upon completion.

🔄 CI/CD with GitHub Actions
This project integrates with GitHub Actions to automate the health checks.

Workflow File: .github/workflows/main.yml

Triggers: The workflow runs automatically on:

Every push to the main branch.

A daily schedule (midnight UTC).

Process: The GitHub Actions runner sets up a Docker environment, starts the database and monitor containers, runs the health checks, and reports the outcome.

You can view the results of these automated runs under the "Actions" tab in this GitHub repository.

📐 System Design / Architecture
graph TD
    subgraph Local Machine / GitHub Actions Runner
        A[run_monitor.sh] --> B(docker-compose.yml)
        B --> C[Dockerfile (Build Monitor Image)]
        B --> D(PostgreSQL DB Container)
        B --> E(Python Monitor Container)
        E -- Connects to --> D
        E -- Outputs --> F[Terminal / GitHub Actions Logs]
    end

The docker-compose.yml defines two services: db (PostgreSQL) and monitor (Python script).

The monitor service builds its image from the Dockerfile, ensuring all Python dependencies are included.

depends_on: service_healthy in docker-compose.yml ensures the monitor container only starts after the db container's health check passes.

The run_monitor.sh script orchestrates this locally, while the .github/workflows/main.yml script automates it on GitHub.


Feel free to explore the code and adapt it to your needs!
