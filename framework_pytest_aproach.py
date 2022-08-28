import requests
import random
import json

users = "https://gorest.co.in/public/v2/users"
posts = "https://gorest.co.in/public/v2/posts"
comments = "https://gorest.co.in/public/v2/comments"
todos = "https://gorest.co.in/public/v2/todos"

api_urls = [users, posts, comments, todos]

tok = '3211851a79084b29fb93a85047caf8873f37ea803a3df632be03fb54be5762a0'

headers = {"Authorization": "Bearer " + tok}


class Base:

    entities_created = []

    def __init__(self):
        # self.error_message = None
        # self.error_field = None
        self.id = ''
        self.api = ''

    def retrieve_all(self, endpoint=''):  # sunt paginate, impropriu spus all
        """ Retrieve data for all endpoints, just 10 objects (a page) for each. """

        if endpoint == '':
            for api_url in api_urls:
                response = requests.get(url=api_url, headers=headers)
                print(str(api_url))
                print(response.json())
                print(response.status_code)
                print("######################")
        else:
            if endpoint == 'users':
                self.api = api_urls[0]

            elif endpoint == 'posts':
                self.api = api_urls[1]

            elif endpoint == 'comments':
                self.api = api_urls[2]

            elif endpoint == 'todos':
                self.api = api_urls[3]

            response = requests.get(url=self.api, headers=headers)
            print(str(self.api))
            print(response.json())
            print(response.status_code)
            print("######################")

    def retrieve(self, ID=''):
        """ Retrieve data for a specific endpoint and id.
        :return: Response data
        """

        global response

        if ID == "":
            self.api = self.api + '/' + str(self.id)
        else:
            self.api = self.api + '/' + str(ID)

        try:
            print(self.api)
            response = requests.get(url=self.api, headers=headers)
            response.raise_for_status()
            print(response.json())
            print(response.status_code)

            response_data = json.loads(response.text) # VEZI AICI
            return response_data # SI AICI

        except requests.exceptions.HTTPError:
            if response.status_code == 404:
                print("There is no such id!\nEND OF LINE")

            assert False

    def verifying_action(self, action, api_url, payload):
        """ Verify using try catch if an object exists in the api when using update or semi-update. """
        global response, status_code, object_response

        if action == "update":

            try:
                response = requests.put(url=api_url, json=payload, headers=headers)
                object_response = response.json()
                status_code = response.status_code
                print(object_response)
                print(status_code)
                self.stat = response.status_code
                response.raise_for_status()
            except requests.exceptions.HTTPError:
                if response.status_code == 404:
                    print("There is no such id!\nEND OF LINE")
                elif response.status_code == 422:
                    print(f"ERROR!!!"
                          f"\nStatus Code: {status_code}\n"
                          f"Message: {object_response}")

                assert False

        elif action == "semi-update":

            try:
                response = requests.patch(url=api_url, json=payload, headers=headers)
                object_response = response.json()
                status_code = response.status_code
                print(object_response)
                print(status_code)
                self.stat = response.status_code
                response.raise_for_status()
            except requests.exceptions.HTTPError:
                if response.status_code == 404:
                    print("There is no such id!\nEND OF LINE")
                elif response.status_code == 422:
                    print(f"ERROR!!!"
                          f"\nStatus Code: {status_code}\n"
                          f"Message: {object_response}")

                assert False

    def cleanup(self):
        """ Deletes every single recent object created. """
        entities_created = self.entities_created
        for entity in reversed(entities_created):
            print(entity)
            entity.delete()  # object type
            entities_created.remove(entity)

    def delete(self, ID=""):
        """ Deletes an object based on its id. """
        if ID == "":
            if self.api[-1].isdigit():
                pass # ASTA e pt cand se da si retrieve inainte de cleanup
            else:
                self.api = self.api + '/' + str(self.id)  # ASTA e pt cand se da cleanup fara retrieve inainte
        else:
            self.api = self.api + '/' + str(ID)
        print(self.api)
        response = requests.delete(self.api, headers=headers)
        print(response.status_code)
        print(response.text)


class Users(Base):

    def __init__(self, id=5009, name="zzz", email="kkahholoohllglllg@outlook.com", gender="female", status="active"):
        self.api = users
        self.stat = None
        self.id = id
        self.name = name
        self.email = email
        self.gender = gender
        self.status = status
        self.error_field = ''
        self.error_message = ''

    def set_payload(self):
        """ Sets a specific payload based on __init__ attributes.
            :return: users_payload
        """
        users_payload = {
            "name": self.name,
            "email": self.email,
            "gender": self.gender,
            "status": self.status
        }
        return users_payload

    def check_and_post(self, users_payload):
        """ Verifying method for create method in class Users. Checks if an object has been created properly
            and POST it into the api.
        """
        global response, status_code, object_response
        api_url = self.api
        try:
            response = requests.post(url=api_url, json=users_payload, headers=headers)
            object_response = response.json()
            status_code = response.status_code
            print(api_url)
            print(response.json())
            print(response.status_code)
            self.stat = response.status_code
            response.raise_for_status()

            req = requests.get(url=api_url, headers=headers)
            data = req.json()
            self.id = data[0]["id"] # saves and replaces the autogenerated id

            load = self  # self -> clasa curenta ca obiect
            self.entities_created.append(load)
            print(self.entities_created)

        except requests.exceptions.HTTPError:
            if response.status_code == 422:
                data = response.json()
                self.error_field = data[0]["field"]
                self.error_message = data[0]["message"]
                if self.error_field == "email" and self.error_message == "has already been taken":
                    print(f"ERROR!!!"
                          f"\nStatus Code: {status_code}\n"
                          f"Message: {object_response}")
                    # print("Changing email...")
                    # self.email = "defaultmail" + str(int(random.uniform(0, 10000))) + "@default.com"
                    # users_payload["email"] = self.email

            elif response.status_code == 404:
                print("Error")

            assert False

    def create(self):
        """ Creates an object.
            It's calling set_payload method and check_and_post.
        """

        users_payload = self.set_payload()
        self.check_and_post(users_payload)

    def creation_status(self):
        """ Verify the status of the create method. """
        if self.stat == 201:
            print("Object created successfully!")
        else:
            print("Error -> Check code: ", self.stat)

    def update(self):
        """ Does PUT into the api based on the api_url and the payload. """

        api_url = self.api + '/' + str(self.id)

        users_payload = self.set_payload()

        self.verifying_action("update", api_url, users_payload)

    def semi_update(self, *args):
        """ Does PATCH into the api based on the api_url and the payload. """

        api_url = self.api + '/' + str(self.id)

        users_payload = self.set_payload()
        for arg in args:
            print("Key included in PATCH: ")
            print(arg)

        patched_payload = {key: value for key, value in users_payload.items() if key in args}

        self.verifying_action("semi-update", api_url, patched_payload)


class Posts(Base):

    def __init__(self, id=90000, user_id=8000, title="somejffjthfdddhgfing", body="ssffaaffflfsssss"):
        self.api = posts
        self.stat = None
        self.id = id
        self.user_id = user_id
        self.title = title
        self.body = body
        self.error_field = ''
        self.error_message = ''

    def set_payload(self):
        posts_payload = {
            "user_id": self.user_id,
            "title": self.title,
            "body": self.body
        }
        return posts_payload

    def check_and_post(self, posts_payload):
        """ Verifying method for create method in class Posts. Checks if an object has been created properly
            and POST it into the api.
        """
        global response, status_code, object_response
        api_url = self.api
        try:
            response = requests.post(url=api_url, json=posts_payload, headers=headers)
            object_response = response.json()
            status_code = response.status_code
            print(api_url)
            print(response.json())
            print(response.status_code)
            self.stat = response.status_code
            response.raise_for_status()

            req = requests.get(url=api_url, headers=headers)
            data = req.json()
            self.id = data[0]["id"]

            load = self  # self -> clasa curenta ca obiect
            self.entities_created.append(load)
            print(self.entities_created)

        except requests.exceptions.HTTPError:
            if response.status_code == 422:
                data = response.json()
                self.error_field = data[0]["field"]
                self.error_message = data[0]["message"]
                if self.error_field == "user" and self.error_message == "must exist":
                    print(f"ERROR!!!"
                          f"\nStatus Code: {status_code}\n"
                          f"Message: {object_response}")

            elif response.status_code == 404:
                print("Error")

            assert False

    def create(self):

        posts_payload = self.set_payload()
        self.check_and_post(posts_payload)

    def creation_status(self):
        if self.stat == 201:
            print("Object created successfully!")
        else:
            print("Error -> Check code: ", self.stat)

    def update(self):

        api_url = self.api + '/' + str(self.id)

        posts_payload = self.set_payload()

        self.verifying_action("update", api_url, posts_payload)

    def semi_update(self, *args):

        api_url = self.api + '/' + str(self.id)

        posts_payload = self.set_payload()

        for arg in args:
            print("Key included in PATCH: ")
            print(arg)

        patched_payload = {key: value for key, value in posts_payload.items() if key in args}

        self.verifying_action("semi-update", api_url, patched_payload)


class Comments(Base):

    def __init__(self, id=1840, post_id=5000, name="EsSSa", email="esSSa@outlook.com", body="uuuuuffeeuu"):
        self.api = comments
        self.stat = None
        self.id = id
        self.post_id = post_id
        self.name = name
        self.email = email
        self.body = body
        self.error_field = ''
        self.error_message = ''

    def set_payload(self):
        comments_payload = {
            "post_id": self.post_id,
            "name": self.name,
            "email": self.email,
            "body": self.body
        }
        return comments_payload

    def check_and_post(self, comments_payload):
        """ Verifying method for create method in class Comments. Checks if an object has been created properly
            and POST it into the api.
        """
        global response, status_code, object_response
        api_url = self.api

        try:
            response = requests.post(url=api_url, json=comments_payload, headers=headers)
            object_response = response.json()
            status_code = response.status_code
            print(api_url)
            print(response.json())
            print(response.status_code)
            self.stat = response.status_code
            response.raise_for_status()

            req = requests.get(url=api_url, headers=headers)
            data = req.json()
            self.id = data[0]["id"]

            load = self  # self -> clasa curenta ca obiect
            self.entities_created.append(load)
            print(self.entities_created)

        except requests.exceptions.HTTPError:
            if response.status_code == 422:
                data = response.json()
                self.error_field = data[0]["field"]
                self.error_message = data[0]["message"]
                if self.error_field == "post" and self.error_message == "must exist":
                    print(f"ERROR!!!"
                          f"\nStatus Code: {status_code}\n"
                          f"Message: {object_response}")

            elif response.status_code == 404:
                print("Error")

            assert False

    def create(self):

        comments_payload = self.set_payload()
        self.check_and_post(comments_payload)

    def creation_status(self):
        if self.stat == 201:
            print("Object created successfully!")
        else:
            print("Error -> Check code: ", self.stat)

    def update(self):

        api_url = self.api + '/' + str(self.id)

        comments_payload = self.set_payload()

        self.verifying_action("update", api_url, comments_payload)


    def semi_update(self, *args):

        api_url = self.api + '/' + str(self.id)

        comments_payload = self.set_payload()

        for arg in args:
            print("Key included in PATCH: ")
            print(arg)

        patched_payload = {key: value for key, value in comments_payload.items() if key in args}

        self.verifying_action("semi-update", api_url, patched_payload)


class Todos(Base):

    def __init__(self, id=1794, user_id=7000, title="random_title", due_on="2022-09-24", status="completed"):
        self.api = todos
        self.stat = None
        self.id = id
        self.user_id = user_id
        self.title = title + str(int(random.uniform(0, 10000)))
        self.due_on = due_on
        self.status = status
        self.error_field = ''
        self.error_message = ''

    def set_payload(self):

        todos_payload = {
            "user_id": self.user_id,
            "title": self.title,
            "due_on": self.due_on,
            "status": self.status
        }
        return todos_payload

    def check_and_post(self, todos_payload):
        """ Verifying method for create method in class Todos. Checks if an object has been created properly
            and POST it into the api.
        """
        global response, status_code, object_response
        api_url = self.api

        try:

            response = requests.post(url=api_url, json=todos_payload, headers=headers)
            object_response = response.json()
            status_code = response.status_code
            print(api_url)
            print(response.json())
            print(response.status_code)
            self.stat = response.status_code
            response.raise_for_status()

            req = requests.get(url=api_url, headers=headers)
            data = req.json()
            self.id = data[0]["id"]

            load = self  # self -> clasa curenta ca obiect
            self.entities_created.append(load)
            print(self.entities_created)

        except requests.exceptions.HTTPError:
            if response.status_code == 422:
                data = response.json()
                self.error_field = data[0]["field"]
                self.error_message = data[0]["message"]
                if self.error_field == "user" and self.error_message == "must exist":
                    print(f"ERROR!!!"
                          f"\nStatus Code: {status_code}\n"
                          f"Message: {object_response}")

            elif response.status_code == 404:
                print("Error")

            assert False

    def create(self):

        todos_payload = self.set_payload()
        self.check_and_post(todos_payload)

    def creation_status(self):
        if self.stat == 201:
            print("Object created successfully!")
        else:
            print("Error -> Check code: ", self.stat)

    def update(self):

        api_url = self.api + '/' + str(self.id)

        todos_payload = self.set_payload()

        self.verifying_action("update", api_url, todos_payload)

    def semi_update(self, *args):

        api_url = self.api + '/' + str(self.id)

        todos_payload = self.set_payload()

        for arg in args:
            print("Key included in PATCH: ")
            print(arg)

        patched_payload = {key: value for key, value in todos_payload.items() if key in args}

        self.verifying_action("semi-update", api_url, patched_payload)
