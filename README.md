# face_recognition
There are 2 apis for Face Enrollment & Face Recognition:
1. Face Enrollment api endpoint: /api/v1/face_enrollment
2. Face Recognition api endpoint: /api/v1/face_detect

## How to deploy:
1. Clone the git repo:
    >> git clone https://github.com/ihpolash/face_recognition.git

2. Create venv for the project & activate the environment:
    >> "virtualenv /opt/env" or "python3 -m venv env"
    >> source /opt/env/bin/activate

3. Install all the dependencies:
    >> pip3 install -r requirements.txt

4. Before starting the Django development server, you can check your Django project for potential problems:
    >> cd face_recognition/
    >> python manage.py check

5. Make Gunicorn configuration:
    #### Create config directory
    >> mkdir -pv config/gunicorn/
    #### Next, open a development configuration file, config/gunicorn/dev.py, and add the following:
        """Gunicorn *development* config file"""
        # Django WSGI application path in pattern MODULE_NAME:VARIABLE_NAME
        wsgi_app = "face_detect.wsgi:application"
        # The granularity of Error log outputs
        loglevel = "debug"
        # The number of worker processes for handling requests
        workers = 2
        # The socket to bind
        bind = "0.0.0.0:8000"
        # Restart workers when code changes (development only!)
        reload = True
        # Write access and error info to /var/log
        accesslog = errorlog = "/var/log/gunicorn/dev.log"
        # Redirect stdout/stderr to log file
        capture_output = True
        # PID file so you can easily fetch process ID
        pidfile = "/var/run/gunicorn/dev.pid"
        # Daemonize the Gunicorn process (detach & enter background)
        daemon = True
    #### Next, make sure that log and PID directories exist for the values set in the Gunicorn configuration file above:
        >> sudo mkdir -pv /var/{log,run}/gunicorn/
    #### With that out of the way, you can start Gunicorn using the -c flag to point to a configuration file from your project root:
        >> gunicorn -c config/gunicorn/dev.py
    #### Just as before, you can now monitor the output file to see the output logged by Gunicorn:
        >> tail -f /var/log/gunicorn/dev.log

