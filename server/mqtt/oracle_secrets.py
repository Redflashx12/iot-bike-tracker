import os

import oci
import base64

secret_ocid = os.environ.get("oracle.secret_ocid")


def retrieve_ttn_api_key(stage="CURRENT"):
    config = oci.config.from_file("~/.oci/config", "DEFAULT")
    secret_client = oci.secrets.SecretsClient(config)

    try:
        secret_bundle = secret_client.get_secret_bundle(secret_ocid, stage=stage)
        return base64.b64decode(secret_bundle.data.secret_bundle_content.content).decode('utf-8')
    except oci.exceptions.ServiceError as e:
        print("Error retrieving secret: {}".format(e))
        return None
