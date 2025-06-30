# Dashboard

A simple local dashboard webapp, designed to fit on a tablet.

![](https://github.com/Egsagon/dashboard/blob/03668d4807589cfd02bdaeea28acd256b3e84005/demo.png)

## Installation

> ![WARNING]
> This project is configured for me only.
> You have to change stuff to make it work on your end.

- Clone the repo
- Install python dependencies: `pip install flask flask-socketio eventlet pyyaml`
- Some included modules require additional software:
    - cells/home/buttons/* & cells/keyboard/*: Requires AHK2
    - cells/home/mouse: Requires PyWinUSB
    - cells/home/stats/gpu & temp: Requires Nvidia SMI

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
