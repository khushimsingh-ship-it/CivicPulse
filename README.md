# CivicPulse — Public Service Usage and Operations Management System

### A Web-Based Platform for Public Service Request Management

🌐 **Live Website:** https://civicpulse-moll.onrender.com

💻 **GitHub Repository:** https://github.com/khushimsingh-ship-it/CivicPulse

🚀 **Try the Live Demo:** [Click here to open CivicPulse](https://civicpulse-moll.onrender.com)

---

## 1. Project Overview

CivicPulse is a web-based Public Service Usage and Operations Management System developed to make public service request management more organized and efficient.

The application provides a centralized platform for recording service requests, tracking their status, assigning workers, monitoring workloads, and analyzing service-related information. It helps users manage requests in one place rather than relying on disconnected records or manual tracking.

The project demonstrates how web development, database management, and data visualization can be combined to create a practical public service management solution.

## 2. Problem Statement

Managing public service requests involves recording complaints or requests, assigning responsible workers, tracking progress, and reviewing service performance. Manual or disconnected processes can make these tasks difficult to organize and monitor.

CivicPulse addresses these challenges by providing a digital platform for managing service requests and reviewing operational information.

## 3. Project Objectives

- Digitize public service request management.
- Store service request records in a structured database.
- Track and update request statuses.
- Assign workers to service requests.
- Monitor worker assignments and workloads.
- Search and filter requests efficiently.
- Export records for reporting and analysis.
- Visualize service-related data using interactive charts.

## 4. Key Features

### Dashboard
Provides a central view of service requests and their recorded information.

### Service Request Management
Allows users to add and manage public service request records.

### Status Tracking
Supports updating the status of existing requests to monitor their progress.

### Worker Assignment
Allows service requests to be assigned to workers, including Rahul, Priya, Amit, and Sneha, or left unassigned.

### Workload Monitoring
Helps users review worker assignments and understand how requests are distributed.

### Search and Filtering
Makes it easier to locate relevant requests using available search and filter options.

### CSV Export
Allows service request records to be exported in CSV format for use in spreadsheet applications such as Microsoft Excel.

### Analytics Dashboard
Uses Plotly to display interactive charts based on recorded service data, supporting the review of service operations.

## 5. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Flask | Backend web framework |
| HTML | Web page structure |
| CSS | Styling and layout |
| SQLite | Database for service request records |
| Plotly | Interactive data visualization |
| Git | Version control |
| GitHub | Source code hosting |
| Render | Online deployment |

## 6. How CivicPulse Works

1. **Open the website:** Visit the live CivicPulse application.
2. **View the dashboard:** Review existing service request records.
3. **Add a request:** Enter the information required to register a new request.
4. **Store information:** The application saves request data in its SQLite database.
5. **Update requests:** Change request statuses and assign workers as needed.
6. **Search records:** Use the available search and filtering features to find requests.
7. **Review analytics:** Open the analytics page to explore interactive charts.
8. **Export records:** Download available request information as a CSV file.

## 7. System Architecture

CivicPulse uses a simple web application architecture:

- **Frontend:** HTML and CSS provide the user interface.
- **Backend:** Flask processes requests and manages application routes.
- **Database:** SQLite stores service request information.
- **Analytics:** Plotly generates interactive charts.
- **Deployment:** Render hosts the application online.

**Application workflow:**

User → Web Interface → Flask Backend → SQLite Database → Dashboard and Analytics

## 8. Live Website and Deployment

The CivicPulse application is deployed on Render and can be accessed through its primary public URL.

### 🌐 Live Demo

**https://civicpulse-moll.onrender.com**

Click the link to open the deployed application and explore its available features.

### Source Code

**https://github.com/khushimsingh-ship-it/CivicPulse**

The GitHub repository contains the project's source code and setup files.

*Note: On Render's free service, the website may take a little time to respond after a period of inactivity. SQLite data stored on a temporary filesystem may also be lost after restarts or redeployments unless persistent storage is configured.*

## 9. How to Run Locally

### Prerequisites
- Python
- Git
- Visual Studio Code or another code editor

### Step 1: Clone the repository

```bash
git clone https://github.com/khushimsingh-ship-it/CivicPulse.git
```

### Step 2: Open the project folder

```bash
cd CivicPulse
```

### Step 3: Create a virtual environment

```powershell
python -m venv .venv
```

### Step 4: Activate the environment

```powershell
.venv\Scripts\Activate.ps1
```

### Step 5: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Start the application

```bash
python app.py
```

### Step 7: Open it in your browser

http://127.0.0.1:5000

## 10. Benefits of the Project

- Centralizes public service request records.
- Simplifies request status updates.
- Supports organized worker assignments.
- Makes searching and exporting information easier.
- Provides visual insights into recorded service data.
- Demonstrates practical web development and database skills.
- Makes the application accessible through a web browser.

## 11. Future Scope

Possible future enhancements include:

- Secure authentication and role-based access.
- Notifications for new requests and status changes.
- Persistent cloud database storage.
- Geographic mapping of service requests.
- Request priority levels and deadline tracking.
- Advanced performance reports.
- Improved mobile responsiveness.

## 12. Conclusion

CivicPulse demonstrates a practical approach to public service request management by combining request registration, status tracking, worker assignment, search and filtering, CSV export, and interactive analytics in one web application.

The project applies Python, Flask, SQLite, HTML, CSS, and Plotly to develop a functional system that can be explored through its deployed website.

## Author

**Khushi Manoj Singh**

Third-Year B.Tech Computer Engineering Student

**Project Title:** CivicPulse — Public Service Usage and Operations Management System
