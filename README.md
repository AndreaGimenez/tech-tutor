## Setup

### Create the virtual environment:
```bash
python3 -m venv venv
```

### Activate the virtual environment:
```bash
source venv/bin/activate
```

### Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Applications

### Execute the tech tutor app (with Streamlit UI):
```bash
cd tech-tutor
streamlit run app.py
```

### Execute the ask a model app (with Gradio UI):
```bash
cd ask-a-model
python3 app.py
```
