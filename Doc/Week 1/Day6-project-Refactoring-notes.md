So today I'm going to clean up the refactoring project and build the front-end for the UI.

First, I built the front-end for the UI, using only HTML, CSS, and JavaScript. HTML for web components, CSS for web styling, and JavaScript for the front-end logic and intermediaries that go to the back-end.

Next, I finished refactoring the Fast API for the back-end. In the back-end, there will be just an app folder, within which app will contain main.py for the back-end pointer, a routes folder for the requests that call the service and the responses used, a service folder to handle the schema logic, a schema for the HTTP get or post methods in /redact, and finally, we have a utils folder because this is where only reusable functions are located, in this case, handling null values, as the Fast API only has documentation for handling errors with mismatched data types, invalid JSON, and missing fields.

So now I'm going to connect the JavaScript-based front-end to the Python-based back-end of the Fast API, so I'll first need to enable CORS. Because if run in Python, Fast API has port :8000 and using a live server or browser only opens port :5000, so now the two points are different so it requires CORS to access certain API origins. So now we do another refactoring in main.py to enable CORS for Back-End and activate the virtual environment by typing 'python -m venv venv'. Next we have to connect the Front-End logic using Javascript and the Back-End logic using Python. To run it, we have to change the directory to Back-End by typing 'cd Back-End', and type again 'uvicorn app.main:app --reload' for localhost which only runs for web or Fast API Python because we just enabled CORS or can type 'uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload' if you want to use IPv4. And remember, if you want to use IPv4, you have to set Windows Defender Firewall to Advanced Settings or you can use cmd to access Administration. type
[
New-NetFirewallRule `
DisplayName "Rule name" `
Direction Inbound `
Protocol TCP `
LocalPort "Port number" `
Action "Action"
]

Note that ports 5500 and 8000 must be specified. Therefore, you must create two firewall rules: one for port 5500 and one for port 8000.
