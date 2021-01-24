"""create app and config logging for GCP App Engine."""
import google.cloud.logging

from ezra import create_app

client = google.cloud.logging.Client()
client.get_default_handler()
client.setup_logging()

print('Creating app in main...')
app = create_app()
