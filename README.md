# baari-mikko
Code for Rasberry Pi 4B 4gb

The script should control 9 pumps that will deliver the liquids to the drink glass.
Pumps are controlled with 5 power control units.
HQ camera for face recognition.

## Development

### Setting up environment

1. Setup Python virtualenv
```bash
python3 -m venv venv
```

2. Activate virtualenv
```bash
. venv/bin/activate
```

3. Install required packages
```bash
pip install -r requirements.txt
```

### Database

Project depends on PostgreSQL database. Dump file test1.pgsql included.

### Running dev server

1. Activate virtualenv
```bash
. venv/bin/activate
```

2. Run server
```bash
flask run
```

## Usage

### Initial setup

Register root user running code below and follow instructions
```bash
python facecam.py
```
