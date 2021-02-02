"""create app and config logging for GCP App Engine."""
print("Creating app in main...")
import google.cloud.logging

print("Importing ezra...")
from ezra import create_app

print("Setting up GCP logging...")
client = google.cloud.logging.Client()
client.get_default_handler()
client.setup_logging()

print("Creating app...")
app = create_app()
