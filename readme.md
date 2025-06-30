# Dashboard

A simple local dashboard webapp, designed to fit on a tablet.

## Installation

- Clone the repo
- Install python dependencies: `pip install flask flask-socketio eventlet pyyaml`
- Some included modules require additional software:
    - cells/home/buttons/* & cells/keyboard/*:
        - Requires AHK 3+
    - cells/home/mouse
        - `pip install pywinusb`
- Create a SSL certificate inside /cert/.

## Starting up

- Run `python run.py` from the repo directory
- On your external device, open `https://<your-pr-ip>:8808`.

Additionally, this script was designed to be ran from the Windows Task Scheduler:
Create a new task with a `Start a program` action:
- Program: `path to pythonw.exe` (Usually in appdata/local/programs)
- Arguments: `run.py --server` (Option will dump logs to `app.log`)
- Start in: The repository path
- Start manually the task and/or set in to run on user logon

## TODO
- Transform like button

## License

> Licensed under GPL3. See the `LICENSE` file.

This repository includes code from `Font Awesome` and `socket.io`.