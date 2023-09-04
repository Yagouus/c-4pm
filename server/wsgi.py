from server.init import init_app
import logging

application = init_app()

if __name__ == "__main__":
    logging.basicConfig(filename='error.log', level=logging.DEBUG)
    application.run(host='10.10.59.220', port='8000')
