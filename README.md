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

### Create .env file using env.sample as sample

You will need an Open AI API key and a Gemini api key

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

### Execute the generate company brochure app (with Gradio UI):

```bash
cd brochure
python3 app.py
```

### Execute the dutch teacher app (with Gradio UI):

```bash
cd dutch-teacher
python3 app.py
```

### Execute the holiday pricing app (with Gradio UI)(using simple tools):

```bash
cd holiday-price
python3 app.py
```
