import yaml
import requests
from flask import (
    Flask,
    Response,
    abort,
    send_from_directory as send,
    render_template as render,
)
from urllib.parse import urlparse
from util.byte_converter import get_printable_size as size

app = Flask(__name__)


@app.route("/s/<path:path>")
def send_static_files():
    return send("static", path)


@app.route("/index/")
def index():
    url = "https://updates.signal.org/desktop/"
    latest = []
    apk = requests.get(
        "https://updates.signal.org/android/latest.json").json()
    win = yaml.safe_load(
        requests.get("https://updates.signal.org/desktop/latest.yml").content)
    mac = yaml.safe_load(
        requests.get(
            "https://updates.signal.org/desktop/latest-mac.yml").content)

    latest.append({
        "head": "Signal for Android",
        "name": urlparse(apk['url']).path.split('/')[2],
        "version": apk['versionName'],
        "sha256sum": apk['sha256sum'],
        "url": apk['url'],
        "detour": "/apk/" + urlparse(apk['url']).path.split('/')[2]
    })

    latest.append({
        "head": "Signal for Windows",
        "name": win['path'],
        "version": win['version'],
        "sha512": win['sha512'],
        "releaseDate": win['releaseDate'],
        "size": size(int(win['files'][0]['size'])),
        "url": url + win['path'],
        "detour": "/win/" + win['path']
    })
    latest.append({
        "head": "Signal for Mac",
        "name": mac['files'][1]['url'],
        "version": mac['version'],
        "sha512": mac['files'][1]['sha512'],
        "releaseDate": mac['releaseDate'],
        "size": size(int(mac['files'][1]['size'])),
        "url": url + mac['files'][1]['url'],
        "detour": "/mac/" + mac['files'][1]['url']
    })

    return render("index.html", latest=latest)


# import mimetypes mimetypes.MimeTypes().guess_type(filename)[0]
# android : https://updates.signal.org/android/latest.json

@app.route("/apk/", methods=["GET"])
@app.route("/apk/<name>", methods=["GET"])
def get_signal_apk(name=None):
    if not name:
        return abort(404)
    url = requests.get(
        "https://updates.signal.org/android/latest.json").json()["url"]
    res = requests.get(url)
    return Response(
        res.content,
        status=res.status_code,
        mimetype="application/vnd.android.package-archive",
    )


# 'application/x-msdownload'
# windows : https://updates.signal.org/desktop/latest.yml

@app.route("/win/", methods=["GET"])
@app.route("/win/<name>", methods=["GET"])
def get_signal_win(name=None):
    if not name:
        return abort(404)
    url = "https://updates.signal.org/desktop/"
    stream = yaml.safe_load(
        requests.get("https://updates.signal.org/desktop/latest.yml").content)
    win_url = url + str(stream["files"][0]["url"])
    res = requests.get(win_url)
    return Response(res.content,
                    status=res.status_code,
                    mimetype="application/x-msdownload")


# 'application/x-apple-diskimage'
# mac : https://updates.signal.org/desktop/latest-mac.yml
@app.route("/mac/", methods=["GET"])
@app.route("/mac/<name>", methods=["GET"])
def get_signal_mac(name=None):
    if not name:
        return abort(404)
    url = "https://updates.signal.org/desktop/"
    stream = yaml.safe_load(
        requests.get(
            "https://updates.signal.org/desktop/latest-mac.yml").content)
    mac_url = url + str(stream["files"][1]["url"])
    res = requests.get(mac_url)
    return Response(res.content,
                    status=res.status_code,
                    mimetype="application/x-apple-diskimage")


# if __name__ == "__main__":
#     app.run()
