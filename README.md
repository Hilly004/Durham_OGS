Durham Optical Ground Station (OGS)

Durham OGS is a browser-based control system for an optical ground station. It provides controls and status information for the telescope mount, dome, camera, weather station, satellite tracking and observatory safety.

Safety: This software controls physical observatory equipment. Check all connection settings, clearances and safety limits before commanding the mount or dome.

Project structure

Durham_OGS/
├── backend/              # FastAPI/Python hardware control
│   └── main.py           # Backend entry point
└── frontend/ogs-gui/     # React/Vite user interface

The frontend communicates with the backend using /api/... requests.

Hardware support

The current codebase includes support for:

TenMicron telescope mount over TCP/IP

AstroHaven dome over TCP/IP

ZWO camera using pyzwoasi

Weather monitor over a serial connection

Installation

Backend

cd Durham_OGS/backend
python3.13 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install "fastapi[standard]" sqlalchemy pyserial numpy pillow pyzwoasi pymodbus

Frontend

cd Durham_OGS/frontend/ogs-gui
npm install

Running the application

Run the backend in one terminal:

cd Durham_OGS/backend
source .venv/bin/activate
uvicorn main:app --host 127.0.0.1 --port 8000 --reload

Run the frontend in another terminal:

cd Durham_OGS/frontend/ogs-gui
npm run dev

Open the address shown by Vite, normally:

http://localhost:5173/

The backend API runs at:

http://127.0.0.1:8000/

API documentation is available at:

http://127.0.0.1:8000/docs

First-time setup

Open Settings before connecting hardware and check:

Observatory latitude, longitude and elevation

Mount IP address and port

Dome IP address and port

Weather serial port and baud rate

Safety limits such as wind speed and humidity

Settings are stored in:

backend/durham_ogs.db

Do not assume the default IP addresses or ports match your equipment.

Main pages

Dashboard

Shows the overall state of the observatory and connected equipment.

Mount

Connect to the telescope mount, view position, slew, nudge and park the telescope.

Dome

Connect to the dome, check its status and operate the dome controls.

Camera

Connect to the ZWO camera, use live view and capture images.

Weather

View weather measurements and safety information.

Tracking

Manage satellite/TLE information and control satellite tracking.

Settings

Configure observatory, connection and safety settings.

Recommended startup order

Start the backend.

Start the frontend.

Check Settings.

Connect the weather station.

Connect the dome.

Connect the mount.

Connect the camera.

Confirm the displayed status matches the real hardware before moving equipment.

Common problems

ModuleNotFoundError: Controllers or Hardware

Run the backend from the backend directory:

cd Durham_OGS/backend
uvicorn main:app --host 127.0.0.1 --port 8000 --reload

Frontend cannot reach the backend

Make sure the backend is running on:

127.0.0.1:8000

Weather station will not connect

On macOS, list serial devices with:

ls /dev/cu.*

Then select the correct device in Settings.

ZWO camera is not detected

Check that the camera is connected, the ZWO SDK/driver is installed and pyzwoasi is installed in the active Python environment.

Building and testing

Frontend build:

cd Durham_OGS/frontend/ogs-gui
npm run build

Backend tests:

cd Durham_OGS/backend
pytest

Some tests may interact with real hardware, so review them before running them on a live observatory system.

Development note

This project is still under development. The frontend and backend currently run as separate processes, and backend dependencies are not yet fully declared in pyproject.toml.