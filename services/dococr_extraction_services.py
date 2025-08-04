from google.api_core.client_options import ClientOptions
from google.cloud import documentai
import os
from dotenv import load_dotenv

load_dotenv()

class GoogleDocOcr:

    os.environ['GOOGLE_APPLICATION_CREDENTIALS']=os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    
    def __init__(self,project_id,processor_id):
        self.project_id=project_id
        self.processor_id=processor_id
        self.location='us'


    def documentai_(self,path,mime_type):

        pdf_bytes = path 

        PROJECT_ID = self.project_id
        LOCATION = self.location
        PROCESSOR_ID = self.processor_id
        MIME_TYPE = mime_type
        docai_client = documentai.DocumentProcessorServiceClient(
            client_options=ClientOptions(api_endpoint=f"{LOCATION}-documentai.googleapis.com")
        )

        RESOURCE_NAME = docai_client.processor_path(PROJECT_ID, LOCATION, PROCESSOR_ID)

        raw_document = documentai.RawDocument(content=pdf_bytes, mime_type=MIME_TYPE)

        request = documentai.ProcessRequest(name=RESOURCE_NAME, raw_document=raw_document)
        result = docai_client.process_document(request=request)

        document_object = result.document
        
        return{"status_code":200,"message":" extract using documentai","data":document_object.text}
    