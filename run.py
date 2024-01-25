from localShop import app
from flask import session
import ssl

context = ssl.SSLContext()
context.load_cert_chain('./certs/isys2160.project.crt', './certs/isys2160.project.key')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug = True, ssl_context=context)
