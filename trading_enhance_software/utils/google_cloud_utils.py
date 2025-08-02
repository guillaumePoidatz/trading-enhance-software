from google.cloud import aiplatform, storage
from google.oauth2 import service_account
import os
import logging

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

    def upload_training_package(self,local_dir:str, bucket_name:str, destination_blob_name:str):
        """This function uploads the training code to a Google Cloud Storage bucket. The local needs to follow the following structure:
        

        Args:
            local_dir (str): the directory of the training code to upload
            bucket_name (str): the name of the Google Cloud Storage bucket where the code will be uploaded
            destination_blob_name (str): the name of the blob in the bucket where the code will be uploaded
        """
        os.system(f"tar -czf trainer.tar.gz -C {local_dir} .")

        # Envoyer sur GCS
        self.google_client.bucket(bucket_name).blob(destination_blob_name).upload_from_filename("trainer.tar.gz")
        log.info(f"code {local_dir} uploaded to {bucket_name}/{destination_blob_name}")
        
    def submit_vertex_job(
            self,
            project_id:str,
            region:str, 
            bucket_name:str,
            trainer_path_gcs:str,
            display_name:str,
            code_enty_point:str,
            ):
        """ submit a Vertex AI job to train a reinforcement learning model on google cloud platform.

        Args:
            project_id (str): _description_
            region (str): _description_
            bucket_name (str): _description_
            trainer_path_gcs (str): _description_
            display_name (str): _description_
            code_enty_point (str): _description_
        """
        aiplatform.init(project=project_id, location=region, staging_bucket=f"gs://{bucket_name}",credentials=self.credentials)

        job = aiplatform.CustomPythonPackageTrainingJob(
            display_name=display_name,
            python_package_gcs_uri=f"gs://{bucket_name}/{trainer_path_gcs}",
            python_module_name=code_enty_point,
            container_uri="us-docker.pkg.dev/vertex-ai/training/pytorch-gpu.1-13:latest",  # pre config docker image
        )

        job.run(
            replica_count=1,
            #machine_type="n1-standard-8",
            #accelerator_type="NVIDIA_TESLA_T4",
            accelerator_count=1,
            args=[]
        )
