from google.cloud import aiplatform, storage
from google.oauth2 import service_account
import os
import logging
import urllib
import tempfile
import requests

log = logging.getLogger(__name__)

class GoogleCloudTrainer:
    """This class contains utility functions to interact with Google Cloud Platform, specifically for
    setting up bucket lifecycle rules, uploading training packages, and submitting Vertex AI jobs.
    It uses the Google Cloud Storage and Vertex AI libraries to perform these operations.
    """
    def __init__(self,service_account_json_name):
        
        self.google_client = storage.Client.from_service_account_json(service_account_json_name)
        self.credentials = service_account.Credentials.from_service_account_file(service_account_json_name)

    def set_bucket_lifecycle(self,bucket_name: str, max_age_days: int = 2):
        """this function sets the lifecycle rules for a Google Cloud Storage bucket to delete objects older than
        a specified number of days.

        Args:
            bucket_name (str): cloud cloud storage folder name
            max_age_days (int, optional): Defaults to 2.
        """

        bucket = self.google_client.bucket(bucket_name)

        bucket.lifecycle_rules = [
            {
                "action": {"type": "Delete"},
                "condition": {"age": max_age_days}
            }
        ]

        bucket.patch()

    def fetch_training_package(self):
        """This function finds the tar image of the last rl finance framework release"""

        try:
            html_response = requests.get(
                "https://api.github.com/repos/guillaumePoidatz/rl-finance-framework/releases"
            )

            # in case of positive response (code = 200)
            if html_response.status_code == 200:
                releases = html_response.json()

                if releases:
                    latest_release = releases[0]
                    tar_github_release_url = latest_release["tarball_url"]
                    log.info(
                        f"The release used for this training is: {latest_release['tag_name']} of the rl-finance-framework."
                    )
                else:
                    raise Exception("NO RELEASE FOUND")
            else:
                raise Exception(f"HTML ERROR: {html_response.status_code}")

        except Exception as e:
            log.error(f"ERROR: {e}")

        return tar_github_release_url

    def upload_training_package(
        self, training_package_url: str, bucket_name: str, destination_blob_name: str
    ):
        """This function uploads the training code to a Google Cloud Storage bucket.


        Args:
            training_package_url (str): the url of the training code to upload
            bucket_name (str): the name of the Google Cloud Storage bucket where the code will be uploaded
            destination_blob_name (str): the name of the blob in the bucket where the code will be uploaded

        Raises:
            RuntimeError: _description_
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                log.info(f"Downloading training package from {training_package_url}")
                tar_file_path = os.path.join(temp_dir, destination_blob_name)
                urllib.request.urlretrieve(training_package_url, tar_file_path)

                if os.path.getsize(tar_file_path) == 0:
                    raise RuntimeError("Downloaded file is empty")
                # Send on google cloud storage
                self.google_client.bucket(bucket_name).blob(
                    destination_blob_name
                ).upload_from_filename(tar_file_path)

                log.info(
                    f"code from {training_package_url} uploaded to {bucket_name}/{destination_blob_name}"
                )

            except Exception as e:
                log.error(f"Error during upload of the training package: {e}")

            finally:
                os.remove(tar_file_path)

    def submit_vertex_job(
        self,
        project_id: str,
        region: str,
        bucket_name: str,
        destination_blob_name: str,
        display_name: str,
        code_entry_point: str,
    ):
        """submit a Vertex AI job to train a reinforcement learning model on google cloud platform.

        Args:
            project_id (str): name of the project on google cloud storage (GCS)
            region (str): location of the datacenter
            bucket_name (str): folder containing the code on the GCS inside the project
            destination_blob_name (str): url github of the rl finance framework release tar
            display_name (str): name of the job run on vertex AI
            code_entry_point (str): file containing to run for initializing the training
        """
        aiplatform.init(project=project_id, location=region, staging_bucket=f"gs://{bucket_name}",credentials=self.credentials)

        python_package_gcs_uri = f"gs://{bucket_name}/{destination_blob_name}"
        container_uri = f"{region}-docker.pkg.dev/{project_id}/vertex-ai/rl-finance-framework-training:latest"

        bootstrap = f"""
        set -e
        which python3
        python3 -V
        pip --version
        gsutil cp "{python_package_gcs_uri}" ./trainer.tar.gz
        pip install --no-cache-dir ./trainer.tar.gz
        python3 -m {code_entry_point} \\
            --num-cpus-per-learner 5 \\
            --num-env-runners 6 \\
            --num_envs_per_env_runner 6 \\
            --num-gpus-per-learner 1 \\
            --num-learners 4 \\
            --rollout-fragment-length 1 \\
            --minibatch-size 1000
    """.strip()

        job = aiplatform.CustomContainerTrainingJob(
            display_name=display_name,
            container_uri=container_uri,
            command=["bash", "-lc"],
        )

        job.run(
            replica_count=1,
            machine_type="n1-standard-32",
            accelerator_type="NVIDIA_TESLA_T4",
            accelerator_count=4,
            args=[bootstrap],
        )
