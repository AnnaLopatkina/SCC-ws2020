from serviceManager import app


@app.route('/api/studies', methods=['GET'])
def get_studies():

    return 'Hello World!'
