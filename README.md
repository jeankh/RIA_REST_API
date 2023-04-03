# Setting up the API Environment

To set up the environment for running the API, follow the steps below:

# Install Python3 Virtual Environment

```bash
sudo apt install python3-venv
```
# Create and Activate a Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate  //-> changement de terminale + lancement de activate
```
# Install Required Libraries

```bash
pip install -r requirements.txt
```
# Running the API

```bash
python3 run.py
```

By following the above steps, you will have set up the environment to run the API. After running the API, you can test it with the appropriate HTTP requests.

To stop the API press Ctrl+C 
