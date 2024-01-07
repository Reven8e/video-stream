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

2. **Set Up the Database:**
   Import the SQL schema into your PostgreSQL database using the provided `schema.sql` file.

3. **Install Python Dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

4. **Generate High-Resolution Video (1080p):**
   ```bash
   ffmpeg -i {movie name}.mp4 \
   -c:v libx264 -profile:v high -level 4.0 -b:v 5000k \
   -c:a aac -b:a 192k \
   -s 1920x1080 \
   -start_number 0 \
   -hls_time 10 \
   -hls_list_size 0 \
   -f hls static/{video directory path}/high/output.m3u8
   ```

5. **Generate Low-Resolution Video (144p):**
   ```bash
   ffmpeg -i {movie name}.mp4 \
   -c:v libx264 -profile:v baseline -level 3.0 -b:v 95k \
   -c:a aac -b:a 64k \
   -s 256x144 \
   -start_number 0 \
   -hls_time 10 \
   -hls_list_size 0 \
   -f hls static/{video directory path}/low/output.m3u8
   ```

6. **Create Master Playlist (master.m3u8):**
   In the `static/{video directory path}` directory, create a `master.m3u8` file with the following content:
   ```
   #EXTM3U
   #EXT-X-STREAM-INF:BANDWIDTH=4500000,AVERAGE-BANDWIDTH=4250000,RESOLUTION=1920x1080,CODECS="avc1.640028,mp4a.40.2"
   static/{video directory path}/high/output.m3u8
   #EXT-X-STREAM-INF:BANDWIDTH=500000,AVERAGE-BANDWIDTH=500000,RESOLUTION=256x144,CODECS="avc1.42001E,mp4a.40.2"
   static/{video directory path}/low/output.m3u8
   ```

7. **Update Movies Table:**
   Insert relevant information about your video into the `movies` table, including the movie title, path (`static/{video directory path}/master.m3u8`), and thumbnail URL.

---
## Usage

1. **Start the Application:**
   ```bash
   python app.py
   ```

2. **Register a New User:**
   Go to `http://127.0.0.1:5000/register` to create an account.

3. **Login:**
   Visit `http://127.0.0.1:5000/login` and enter your credentials.

4. **Access the Movies Webapp:**
   Navigate to `http://127.0.0.1:5000/videostream/available_movies`, select a movie, get an access code, and the app will redirect you to the streaming endpoint.

5. **Watch Together/Stream Endpoint:**
   Share the URL `http://127.0.0.1:5000/videostream/watch/{access_code}` with others to watch together.

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

- `/tests/unittest_code_manage.py` - Tests the CodeManage module.
- `/tests/unittest_dbms.py` - Tests the DBMS module.
- `/tests/unittest_flask_app.py` - Tests the Flask WebApp.
