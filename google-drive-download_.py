import requests
import os
import sys

def download_file_from_google_drive(fileid, destination):
    def get_confirm_token(response):
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value

        return None

    def save_response_content(response, destination):
        CHUNK_SIZE = 32768

        with open(destination, "wb") as f:
            for chunk in response.iter_content(CHUNK_SIZE):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)

    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : fileid }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : fileid, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)    


if __name__ == "__main__":
        print " Starting Download"
        # TAKE ID FROM SHAREABLE LINK
        file_id = sys.argv[1]
        #file_id="0B3y_msrWZaXLT1BZdVdycDY5TEE"
        # DESTINATION FILE ON YOUR DISK
        cwd = os.getcwd()
        path = sys.argv[2]
        try:
            os.mkdir(path)
        except :
            pass 
        fileName= sys.argv[3]
        destination=cwd+"/"+path+fileName
        download_file_from_google_drive(file_id, destination)
        print "Download completed"

