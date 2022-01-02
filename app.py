import os
import zipfile
from os.path import basename
from time import sleep
from log_settings import logger
from flask import Response, Flask, send_from_directory

__author__ = ["Thirumal"]
__email__ = "m.thirumal@hotmail.com"

app = Flask(__name__)


def read_log():
    """creates logger information"""
    with open('logs/app.log') as f:
        while True:
            yield f.read()
            sleep(1)


@app.route("/stream-log", methods=['GET'])
def stream_log():
    logger.debug("Accessing log streaming!!!")
    return Response(read_log(), mimetype="text/plain", content_type="text/event-stream")


# Archive log as zip and Download and delete
@app.route("/download-log", methods=['GET'])
def download_log():
    logger.debug("Download log is requested")
    # create a ZipFile object
    with zipfile.ZipFile('log.zip', 'w') as zipObj:
        # Iterate over all the files in directory
        for folderName, subfolders, filenames in os.walk("logs"):
            for filename in filenames:
                # create complete filepath of file in directory
                file_path = os.path.join(folderName, filename)
                # Add file to zip
                zipObj.write(file_path, basename(file_path))
    # TODO delete the log zip file
    return send_from_directory(os.getcwd(), "log.zip", as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
