from google.cloud import storage

sc_audionews_bucket = os.getenv('SC_AUDIONEWS_BUCKET')
sc = storage.Client()


def check_file_exists(art_filename):
    bucket = sc.bucket(sc_audionews_bucket)
    return storage.Blob(bucket=bucket, name=art_filename).exists(sc)
