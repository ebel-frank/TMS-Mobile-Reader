import pyrebase

# Do not modify this configurations
firebaseConfig = {
    "apiKey": "AIzaSyD1EZFXiy4gIEIf5RfvfWkGMhpe79XZg7o",
    "authDomain": "tms-database-a792a.firebaseapp.com",
    "projectId": "tms-database-a792a",
    "storageBucket": "tms-database-a792a.appspot.com",
    "messagingSenderId": "946602354504",
    "appId": "1:946602354504:web:d96c56c43ff06e175bf57d",
    "measurementId": "G-QN2NNRZTEE",
    "databaseURL": "https://tms-database-a792a-default-rtdb.firebaseio.com/"
}


class FirebaseDatabase:
    def __init__(self):
        self.firebase = pyrebase.initialize_app(firebaseConfig)
        pass

    def sign_in(self, email, password):
        auth = self.firebase.auth()
        database = self.firebase.database()
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            data = database.child("Users").child(user['localId']).get()
            return {"email": email, "username": data.val().get("username")}
        except Exception as e:
            return str(e).split("message\": \"")[1].split("\",")[0]

    def sign_up(self, username, email, password):
        auth = self.firebase.auth()
        database = self.firebase.database()
        data = {"username": username,
                "email": email,
                "password": password}
        try:
            user = auth.create_user_with_email_and_password(email, password)
            database.child("Users").child(user['localId']).set(data)
            auth.send_email_verification(user['idToken'])
            return True
        except Exception as e:
            return str(e).split("message\": \"")[1].split("\",")[0]

    def reset_password(self, email):
        auth = self.firebase.auth()
        try:
            auth.send_password_reset_email(email)
            return True
        except Exception as e:
            return str(e).split("message\": \"")[1].split("\",")[0]

    def get_cloud_files(self):
        """
        :return: a list of all the files on the cloud
        """
        database = self.firebase.database()
        files = []
        try:
            cloud_files = database.child("Files").get()
            for file in cloud_files.each():
                files.append(file.val())
            return files
        except Exception as e:
            print(str(e))
            # return str(e).split("message\": \"")[1].split("\",")[0]

    def download(self, cloud_path, local_path, filename):
        """
        :param cloud_path: the file path on the firebase storage
        :param local_path: the download location
        :param filename: the name of the file to be saved as
        """
        storage = self.firebase.storage()
        try:
            storage.child(cloud_path).download(local_path, filename)
            return True
        except Exception as e:
            return str(e).split("message\": \"")[1].split("\",")[0]


# if __name__ == "__main__":
#     test = FirebaseDatabase()
#     test.download("/100level/chm111/chm111.txt", "", "chm_handout.txt")
