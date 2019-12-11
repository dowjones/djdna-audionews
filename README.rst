Dow Jones DNA Audio News Website
###################################

Overview
=========

Sample Web Application in Flask, that renders a set of random articles from the public BigQuery news sample, and when reading the particular article, allows to listen an audio version.

The application is a Bootstrap template that implemets few front-end and back-end endpoints within the same file (app.py), and uses some external files emmulating the use of external services.

* **App**: Starting point, defines the Flask routes for front-end and back-end functionalities
* **news_storage**: Provides the news search functionality. For this case, the public BigQuery news sample is used.
* **news_repo**: Contains the methods that work as an interface to a Cloud Storage environment where the generated audio files are stored.
* **news_tts**: Methods to interact with a Text-To-Speech service. This can be easily reconfigured to use the services offered by the common Cloud providers.

Requirements
=============

This example uses Google Cloud Platform (GCP) Speech-To-Text Service. To ensure this sample application works correctly, ensure to `create a service account <https://cloud.google.com/iam/docs/creating-managing-service-accounts>`_, `generate the service account key <https://cloud.google.com/iam/docs/creating-managing-service-account-keys>`_, and then `enable the roles <https://cloud.google.com/iam/docs/granting-roles-to-service-accounts>`_ **BigQuery Data Viewer**, **BigQuery Job User** and **Storage Object Viewer**.

Save the JSON file containing the service account credentials to a path visible by the application, and create the environment variable **GOOGLE_APPLICATION_CREDENTIALS**. Also, set a variable containing the Google Cloud Storage (GCS) bucket name, called **SC_AUDIONEWS_BUCKET**.

.. code-block:: 

    export GOOGLE_APPLICATION_CREDENTIALS='/path/to/credentials.json'
    export SC_AUDIONEWS_BUCKET='my-audio-files'
