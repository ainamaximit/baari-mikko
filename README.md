# baari-mikko
Code for Rasberry pi 4B 4gb 

The script should control 9 pumps that will deliver the liquids to the drink glass
Pumps are controlled with 4 power control units
HD camera for face recognition

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

### Running dev server

1. Activate virtualenv
```bash
. venv/bin/activate
```

2. Run server
```bash
flask app.py
```