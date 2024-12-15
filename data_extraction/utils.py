import os
from google.cloud import secretmanager, vision

def get_google_credentials_from_secret(secret_id, project_id):
    """
    Fetch the Google Application Credentials JSON from Google Secret Manager.
    """
    client = secretmanager.SecretManagerServiceClient()
    secret_name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(name=secret_name)

    # The payload contains the secret in bytes
    secret_payload = response.payload.data.decode("UTF-8")

    # Write the secret to a temporary file
    temp_cred_path = "/tmp/google_credentials.json"
    with open(temp_cred_path, "w") as cred_file:
        cred_file.write(secret_payload)

    return temp_cred_path