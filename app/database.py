from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import boto3
from botocore.exceptions import ClientError
from datetime import datetime, timedelta
import json
import logging

# Get S3 credentials from environment variables
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
S3_BUCKET = os.getenv('S3_BUCKET')
S3_DB_PATH = os.getenv('S3_DB_PATH', 'words.db')
BACKUP_INFO_FILE = 'last_backup_info.json'

# Create SQLAlchemy engine first
SQLALCHEMY_DATABASE_URL = "sqlite:///local_words.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Initialize S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

def should_backup():
    try:
        if os.path.exists(BACKUP_INFO_FILE):
            with open(BACKUP_INFO_FILE, 'r') as f:
                backup_info = json.load(f)
                last_backup = datetime.fromisoformat(backup_info['last_backup'])
                return datetime.now() - last_backup > timedelta(days=1)
        return True
    except:
        return True

def update_backup_timestamp():
    with open(BACKUP_INFO_FILE, 'w') as f:
        json.dump({'last_backup': datetime.now().isoformat()}, f)

def download_db_from_s3():
    if not S3_BUCKET:
        logging.warning("S3_BUCKET not configured. Skipping database download.")
        return
    
    try:
        s3_client.download_file(S3_BUCKET, S3_DB_PATH, 'local_words.db')
        logging.info("Database downloaded successfully from S3")
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            # Database doesn't exist in S3 yet, create a new one
            logging.info("No database found in S3. Creating new local database.")
            Base.metadata.create_all(bind=engine)
            # Upload the new database to S3
            try:
                s3_client.upload_file('local_words.db', S3_BUCKET, S3_DB_PATH)
                logging.info("New database uploaded to S3")
            except ClientError as upload_error:
                logging.error(f"Failed to upload new database to S3: {str(upload_error)}")
        else:
            raise e

def upload_db_to_s3():
    if should_backup():
        try:
            s3_client.upload_file('local_words.db', S3_BUCKET, S3_DB_PATH)
            update_backup_timestamp()
        except ClientError as e:
            raise e

# Download the database from S3 at startup
download_db_from_s3()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine) 