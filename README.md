# Video Stream (שח״ם סייבר)

## Introduction

This project enables users to watch videos synchronously using Flask SocketIO, HLS (HTTP Live Streaming), and Python. It's designed to create a shared viewing experience, allowing multiple users to watch the same video content simultaneously with real-time synchronization.

---
### Prerequisites

Before you begin, ensure you have the following installed:
- An internet connection
- Python 3.XX
- PIP
- FFMPEG
- A HLS-supported web browser
- A PostgreSQL database

---
### Installation

1. **Clone the Git Repository:**
   ```bash
   git clone https://github.com/Reven8e/video-stream
   ```

2. **Create ``.env`` File**:
   ```
   FLASK_SECRET=''
   PSQL_USER=''
   PSQL_PASSWORD=''
   PSQL_HOST=''
   PSQL_DB=''
   ```

3. **Set Up the Database:**
   Import the SQL schema into your PostgreSQL database using the provided `schema.sql` file.

4. **Start setup:**
   ```bash
   python setup.py
   ```

5. **Update Movies Table:**
   Insert relevant information about your video into the `movies` table, including the movie title, path (`static/<video directory path>/master.m3u8`), and thumbnail URL. Use SQL query provided by Step number 3.

---
## Usage

1. **Start the Application:**
   ```bash
   python app.py
   ```

2. **Register a New User:** Go to http://127.0.0.1:5000/register to create an account.

   CURL Example:
   ```bash
   curl -X POST http://127.0.0.1:5000/register -d "username=<username>&password1=<password1>&password2=<password2>" 
   ```


3. **Login:** Visit http://127.0.0.1:5000/login and enter your credentials.

   CURL Example:
   ```bash
   curl -X POST http://127.0.0.1:5000/login -d "username=<username>&password=<password>"
   ```


4. **Access the Movies Webapp:** Navigate to http://127.0.0.1:5000/videostream/available_movies, select a movie, get an access code, and the app will redirect you to the streaming endpoint.

   CURL Example:
   ```bash
   curl -X GET http://127.0.0.1:5000/videostream/available_movies
   ```


5. **Watch Together / Stream Endpoint:** Share the URL http://127.0.0.1:5000/videostream/watch/<access_code> with others to watch together.

   CURL Example:
   ```bash
   curl -X GET http://127.0.0.1:5000/videostream/watch/<access_code>
   ```

---
## Code Overview

- `/src` - Contains Python modules.
- `/src/__init__.py` - Initializes the Flask app.
- `/src/Auth.py` - Manages authentication.
- `/src/CodeManage.py` - Manages access codes.
- `/src/DBMS.py` - Handles database operations.
- `/src/Movies.py` - Manages video streaming.
- `/src/SocketEvents.py` - Manages SocketIO events.
- `src/static` - Stores video files, CSS, and images.
- `src/templates` - Contains Flask HTML templates.

---
## Project Structure

**SQL Schema Diagram**:
![Alt text](https://i.ibb.co/fSXrsz3/Screenshot-2024-01-07-at-14-33-49.png)

**Flask WebApp Diagram:**
![Flask WebApp Diagram](https://i.ibb.co/rxMDqhY/ZLJDRjim3-Bxx-ANHqi-RQ77-Nq-O-j-CDs27-Oe-TWj-WC7-AZCF5f-WIHpf-ODU-V9-Sgf4-NO0j1q-KYFtxyzvqe19t6e-R83.png)

**User Journey Map:**
![User Journey Map](https://i.ibb.co/3WxpsY2/Copy-of-Customer-Journey-Map.png)

---
## Testing

- `/tests/unittest_settings.json` - Configure parameters for testing such as username, movie_id, etc...
- `/tests/unittest_code_manage.py` - Tests the CodeManage module.
- `/tests/unittest_dbms.py` - Tests the DBMS module.
- `/tests/unittest_flask_app.py` - Tests the Flask WebApp.
