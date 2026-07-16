So today I initialized Fast API in my project.

First, I had to install the library with 'pip install fastapi'.
Second, I had to install the library with 'pip install uvicorn'.
And finally, I created a requirements.txt file in case members need to install the library, so type 'pip install -r requirements.txt'.
How do I run Fast API? Just type 'uvicorn app.main:app --reload' or if you're accessing via IPv4, just type 'uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload'. It's in the root file.
