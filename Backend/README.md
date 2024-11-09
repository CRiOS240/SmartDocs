
# Running Backend




## Generating API Key

Signin at [googleaistudio](https://aistudio.google.com/apikey) and get an api key


## Running the project

Make sure to have virtualenv

```bash
  pip install virtualenv
```
Change directory to backend
```bash
  cd backend
```

Create an virtualenv

```bash
  virtualenv env
```

Activate the env (Windows)

```bash
  .\venv\Scripts\activate.bat
```
Install the packages

```bash
  pip install -r requirements.txt
```

Run the backend

```bash
  python gemini_inference.py
```
