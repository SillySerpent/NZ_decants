import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from webpage import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host='localhost', port=5000, threaded=False, debug=True)
