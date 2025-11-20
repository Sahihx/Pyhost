# Python Host for Termux

Lightweight Python hosting environment for Android (Termux) with a simple mobile-friendly web interface.

---

## Features

* Run multiple Python scripts concurrently.
* Start, stop, and view logs for each job.
* Monitor CPU and RAM usage.
* TLS-secured web interface.
* Multi-language support (English / Arabic).
* Persistent job state.
* Background execution with wake-lock.

---

## Requirements

* Termux (or Linux with Python 3)
* Python 3 and pip

---

## Installation

```bash
chmod +x setup.sh
./setup.sh
```

* Select your preferred language on first run.
* The server runs in the background with TLS enabled.

---

## Access

Open your browser:

```
https://localhost:8443
```

* Submit Python code, manage jobs, and view logs.
