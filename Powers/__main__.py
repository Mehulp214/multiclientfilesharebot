import uvloop
from Powers.core import app

if __name__ == "__main__":
    app.run(app.startup())