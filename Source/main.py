from app import makeApp
import database
import logging

# http://127.0.0.1:8000

if __name__ == "__main__":
    
    logging.basicConfig(
        level=logging.INFO,
        format= "%(asctime)s - %(levelname)s - %(message)s"
    )

    database.run()

    App = makeApp()
    App.run(host="127.0.0.1", port=8000,debug=False)