from datetime import datetime,timedelta
import os
class authPayload(dict):

    def __init__(self, id, client_id, is_admin):

        # EXPIRESSECONDS = int(os.getenv(3000))

        # set the id of the object from Postgres
        self.id = id

        #  The client id (like the user id)
        self.sub = client_id

        self.is_admin = is_admin

        # set the expiry attrbute
        self.exp = datetime.utcnow() + timedelta(seconds=3000)