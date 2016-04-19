#Feature Request App

This app allows you to create feature requests and prioritize them on a per-client basis.

# Running
To get an instance of this app up and running, follow these steps (Linux/MacOS):

1. Create a new virtual environment (python3)
` virtualenv -p \`which python3\` venv `
2. Enter the virtual environment
` source venv/bin/activate `
3. Install dependencies
` pip install -r requirements.txt `
4. Start the Flask app server
` python3 app.py `
5. Visit the /init url of the running app to initialize the database.
http://127.0.0.1:5000/init (by default)
6. You should be redirected to the root of the app. If not, visit http://127.0.0.1:5000/ to create feature requests.
