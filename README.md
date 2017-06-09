# Google Maps + Fusiontable

>**Disclaimer:** This is just an experiment and there is no user authentication or authorization on the app itself. This is also not a production-ready project.

## Install + Configuration

In order to get started, you need a add two secrets to your `settings.py`:

- ``GOOGLE_API_KEY``: A Google API Key with the Maps API enabled
- ``GOOGLE_SERVICE_ACCOUNT_JSON_PATH``: Path to a JSON-file containing the secrets for a Google Service Account which has
write access to your FusionTable document.

Then, setup and start your local copy using the following commands:

```bash
$ virtualenv .ve
$ . .ve/bin/activate
$ pip install -r requirements.txt
$ ./manage.py migrate
$ ./manage.py runserver
```

The project will now be running on `http://127.0.0.1:8000/`.
