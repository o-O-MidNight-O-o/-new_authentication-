from flask import request
from flask import Flask , json
import hashlib
import authModel
from flask_restful import Api

app = Flask(__name__)
api = Api(app)

@app.route('/client',methods=['POST','GET'])
def client():
    if request.method=='POST':
        #verify the token
        #to do after we create fisrt credentials

        #get the client_id and secret from the client application
        client_id = request.form.get('client_id')
        client_secret_input = request.form.get('client_secret')
        is_admin = request.form.get('is_admin')

        #the client secret in the database is "hashed" with a one-way hash
        hash_object = hashlib.sha1(bytes(client_secret_input,'utf-8'))
        hashed_client_secret = hash_object.hexdigest()

        #make a call to the model to authenticate
        createResponse = authModel.create(client_id, hashed_client_secret, is_admin)
        return {'success' : createResponse}

    elif request.method == 'DELETE':
        #not yet implemented
        return {'success' : False}
    
    else:
        return {'success' : False}


# API Route for checking the client_id and client_secret
@app.route("/auth", methods=["POST"])
def auth():    
    # get the client_id and secret from the client application
    client_id = request.form.get("client_id")
    client_secret_input = request.form.get("client_secret")

    # the client secret in the database is "hashed" with a one-way hash
    hash_object = hashlib.sha1(bytes(client_secret_input, 'utf-8'))
    hashed_client_secret = hash_object.hexdigest()

    # make a call to the model to authenticate
    authentication = authModel.authenticate(client_id, hashed_client_secret)
    if authentication == False:
        return {'success': False}
    else: 
        return json.dumps(authentication)


# API route for verifying the token passed by API calls
@app.route("/verify", methods=["POST"])
def verify():
    # verify the token 
    authorizationHeader = request.headers.get('authorization')    
    token = authorizationHeader.replace("Bearer ","")
    verification = authModel.verify(token)
    return verification

@app.route("/logout", methods=["POST"])
def logout():
    token = request.form.get("token")
    status = authModel.blacklist(token)
    return {'success': status}

if __name__ == "__main__":
    app.run(debug=True)
