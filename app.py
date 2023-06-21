import gzip
from flask import Flask
from flask import render_template,send_file
from flask import request
import os
import mimetypes

def compress(filename):
    with open(filename, 'rb') as f:
        data = f.read()
    compressed_data = gzip.compress(data)
    with open(filename + '.gz', 'wb') as f:
        f.write(compressed_data)

def decompress(filename):
    with open(filename, 'rb') as f:
        compressed_data = f.read()
    decompress_data = gzip.decompress(compressed_data)
    with open(filename[:-3], 'wb') as f:
        f.write(decompress_data)

app = Flask(__name__)
# Define the FILE_UPLOADS key in the configuration
app.config["FILE_UPLOADS"] = os.path.join(app.root_path, "uploads")


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/compress", methods=["GET", "POST"])
def compress():
    if request.method == "GET":
        return render_template("compress.html", check=0)

    else:
        up_file = request.files["file"]

        if len(up_file.filename) > 0:
            filename = up_file.filename
            up_file.save(os.path.join(app.config["FILE_UPLOADS"], filename))
            compressed_data = gzip.compress(up_file.read())
            with open(filename + '.gz', 'wb') as f:
                f.write(compressed_data)

            return render_template("compress.html", check=1)

        else:
            print("ERROR")
            return render_template("compress.html", check=-1)

@app.route("/decompress", methods=["GET", "POST"])
def decompress():
    if request.method == "GET":
        return render_template("decompress.html", check=0)

    else:
        up_file = request.files["file"]

        if len(up_file.filename) > 0:
            filename = up_file.filename
            decompress_data = gzip.decompress(up_file.read())
            with open(filename[:-3], 'wb') as f:
                f.write(decompress_data)

            return render_template("decompress.html", check=1)

        else:
            print("ERROR")
            return render_template("decompress.html", check=-1)

@app.route("/download")

def download_file():

    def is_valid_file_type(ftype):
        if mimetypes.guess_type(ftype)[0] is not None:
            return True
        else:
            return False

    filename = request.args.get("filename")
    ftype = request.args.get("ftype")

    if not is_valid_file_type(ftype):
        raise ValueError("Invalid file type")

    if filename is None or ftype is None:
        raise ValueError("Invalid filename or file type")

    path = "downloads/" + filename + ftype
    return send_file(path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)