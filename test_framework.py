from framework_pytest_aproach import *
import pytest
import time

class TestUsers:

    def test_create(self):
        """
            Description: Test user creation
        """
        user1 = Users(0, "a_name", "creation@email.com")
        user1.create()
        user1.cleanup()

    def test_retrieve(self):
        """
            Description: Test user retrieval
        """
        user1 = Users(0, "another_name", "another_email@gmail.com")
        user1.create()
        user1.retrieve()
        user1.cleanup()

    def test_update(self):
        """
            Description: Test user update
        """

        user1 = Users(0, "name_before_update", "email_before_update@outlook.com")
        user1.create()
        user1.email = "email_posted_for_user@outlook.com"
        user1.name = "name_after_update"
        user1.update()
        user1.cleanup()

    def test_semi_update(self):
        """
            Description: Test user semi-update
        """

        user1 = Users(0, "some_name", "email_before_patch@gmail.com")
        user1.create()
        user1.email = "email_patched_for_user@outlook.com"
        user1.name = "patched_name"
        user1.status = "inactive"
        user1.semi_update("email", "name", "status")
        user1.cleanup()

    def test_delete(self):
        """
            Description: Test user delete
        """
        user1 = Users(0, "name_delete", "deletion@gmail.com")
        user1.create()
        user1.delete()
        user1.cleanup()


    def test_negative_create(self):

        """
            Description: Test incorrect user create
        """

        user1 = Users(0, 'BBB', 'ambaamba@outlook.com', 'female', 'inactive')
        try:
            user1.create()
        except AssertionError:
            assert user1.error_field == 'email'
            assert user1.error_message == 'has already been taken'

        user1.cleanup()

    def test_try_create_user_with_existent_email(self):
        """Creation of one user with an existing email of another user"""

        user1 = Users(0, "name_of_user1", "email_of_user1@gmail.com")
        user2 = Users(0, "name_of_user2", "email_of_user1@gmail.com")
        try:
            user1.create()
            user2.create()
        except AssertionError:
            assert user2.error_field == 'email'
            assert user2.error_message == 'has already been taken'

        user1.cleanup()


class TestPosts:

    def test_create(self):
        """
            Description: Test post creation
        """
        time.sleep(3)
        user1 = Users(0, "a_name", "creation@email.com")
        user1.create()
        user1_id = user1.id
        post1 = Posts(0, user1_id)
        post1.create()
        user1.cleanup()

    def test_retrieve(self):
        """
            Description: Test post retrieval
        """
        time.sleep(3)
        user1 = Users(0, "another_name", "another_email@gmail.com")
        user1.create()
        user1_id = user1.id
        post1 = Posts(0, user1_id)
        post1.create()
        post1.retrieve()
        post1.cleanup() # merge si user1.cleanup()

    def test_update(self):
        """
            Description: Test post update
        """
        time.sleep(3)
        user1 = Users()
        user1.create()
        user1_id = user1.id
        post1 = Posts(0, user1_id, "title_before_update", "body_before_update")
        post1.create()
        post1.title = "title_after_update"
        post1.body = "body_after_update"
        post1.update()
        post1.cleanup()

    def test_semi_update(self): # # Problema, functionalitatea din Ex1_V2 trebuie modificata
        """
            Description: Test post semi-update
        """
        time.sleep(3)
        user1 = Users()
        user1.create()
        user1_id = user1.id
        post1 = Posts(0, user1_id)
        post1.create()
        post1.body = "body_patched"
        post1.semi_update("body")
        post1.cleanup()

    def test_delete(self):
        """
            Description: Test post delete
        """
        time.sleep(3)
        user1 = Users()
        user1.create()
        user1_id = user1.id
        post1 = Posts(0, user1_id)
        post1.create()
        post1.delete()
        post1.cleanup()

    def test_delete_unfound_id(self):
        """Deletion of an inexistent object of type post"""

        time.sleep(3)
        user1 = Users(0, "delete_unfound_id_name", "deleting@outlook.com")
        user1.create()
        user1_id = user1.id
        post1 = Posts(0, user1_id)
        post1.create()
        try:
            post1.delete(7583)
        except requests.exceptions.HTTPError:
            assert post1.error_message == 'Resource not found'

        post1.cleanup()

    def test_try_create_post_from_user_with_existent_email(self):

        """Creation of one post with a user with existing email of another user"""

        time.sleep(3)

        user1 = Users(0, "name_of_user1", "email_of_user1@gmail.com")
        user2 = Users(0, "name_of_user2", "email_of_user1@gmail.com")

        try:
            user1.create()
            user2.create()
        except AssertionError:
            assert user2.error_field == 'email'
            assert user2.error_message == 'has already been taken'

        user2_id = user2.id
        post1 = Posts(0, user2_id)

        try:
            post1.create()
        except AssertionError:
            assert post1.error_field == 'user'
            assert post1.error_message == 'must exist'

        user1.cleanup()

    def test_negative_create(self):

        """
            Description: Test incorrect post create
        """
        time.sleep(3)

        post1 = Posts(0, 60000)
        try:
            post1.create()
        except AssertionError:
            assert post1.error_field == 'user'
            assert post1.error_message == 'must exist'

        post1.cleanup()

    def test_delete_user_before_post(self):
        """Test if a post is deleted if the user (the user_id from post) related to it is deleted before"""

        time.sleep(3)

        user1 = Users(0, "user1_name", "user1_email@outlook.com")
        user1.create()
        user1_id = user1.id
        post1 = Posts(0, user1_id)
        post1.create()
        user1.delete()
        try:
            post1.retrieve()
        except AssertionError:
            pass

        # post1.cleanup() not necessary

class TestComments:

    def test_create(self):
        """
            Description: Test comments creation
        """
        time.sleep(3)
        user1 = Users(0, "somename1", "EMAIL1@outlook.com")
        user1.create()
        user1_id = user1.id
        post1 = Posts(0, user1_id)
        post1.create()
        post1_id = post1.id
        comment1 = Comments(0, post1_id)
        comment1.create()
        user1.cleanup()

    def test_retrieve(self):
        """
            Description: Test comments retrieval
        """
        time.sleep(3)
        user1 = Users(0, "somename2", "EMAIL2@outlook.com")
        user1.create()
        user1_id = user1.id
        post1 = Posts(0, user1_id)
        post1.create()
        post1_id = post1.id
        comment1 = Comments(0, post1_id)
        comment1.create()
        comment1.retrieve()
        comment1.cleanup() # merge si user1.cleanup()

    def test_update(self):
        """
            Description: Test comments update
        """
        time.sleep(3)
        user1 = Users(0, "comments_update_name", "comments_update_email@gmail.com")
        user1.create()
        user1_id = user1.id
        post1 = Posts(0, user1_id)
        post1.create()
        post1_id = post1.id
        comment1 = Comments(0, post1_id, "NUME1", "NUME1@gmail.com")
        comment1.create()
        comment1.name = "update_name"
        comment1.email = "update_email@email.com"
        comment1.update()
        comment1.cleanup()

    def test_semi_update(self): # Schimbat functionalitate in Ex1_V2
        """
            Description: Test comments semi-update
        """
        time.sleep(3)
        user1 = Users(0, "comments_patch_name", "comments_patch_email@gmail.com")
        user1.create()
        user1_id = user1.id
        post1 = Posts(0, user1_id)
        post1.create()
        post1_id = post1.id
        comment1 = Comments(0, post1_id, "NUME2", "NUME2@gmail.com")
        comment1.create()
        comment1.name = "name_patched"
        comment1.body = "body_patched"
        comment1.semi_update("name", "body")
        comment1.cleanup()

    def test_delete(self):
        """
            Description: Test comments delete
        """
        time.sleep(3)
        user1 = Users(0, "comments_delete_name", "comments_delete_email@gmail.com")
        user1.create()
        user1_id = user1.id
        post1 = Posts(0, user1_id)
        post1.create()
        post1_id = post1.id
        comment1 = Comments(0, post1_id, "NUME3", "NUME3@gmail.com")
        comment1.create()
        comment1.delete()
        comment1.cleanup()

    def test_negative_create(self):

        time.sleep(3)

        comment1 = Comments(0, 60000)
        try:
            comment1.create()
        except AssertionError:
            assert comment1.error_field == 'post'
            assert comment1.error_message == 'must exist'

        comment1.cleanup()

class TestTodos:

    def test_create(self):
        """
            Description: Test todos creation
        """
        time.sleep(3)
        user1 = Users(0, "somename2", "EMAIL2@outlook.com")
        user1.create()
        user1_id = user1.id
        todo1 = Todos(0, user1_id)
        todo1.create()
        user1.cleanup()

    def test_retrieve(self):
        """
            Description: Test todos retrieval
        """
        time.sleep(3)
        user1 = Users(0, "somename3", "EMAIL3@outlook.com")
        user1.create()
        user1_id = user1.id
        todo1 = Todos(0, user1_id)
        todo1.create()
        todo1.retrieve()
        todo1.cleanup() # merge si user1.cleanup()

    def test_update(self):
        """
            Description: Test todos update
        """
        time.sleep(3)
        user1 = Users(0, "somename4", "EMAIL4@outlook.com")
        user1.create()
        user1_id = user1.id
        todo1 = Todos(0, user1_id)
        todo1.create()
        todo1.title = "updated_title"
        todo1.due_on = "2025-12-28"
        todo1.update()
        todo1.cleanup()

    def test_semi_update(self): # Schimbat functionalitate in Ex1_V2
        """
            Description: Test todos semi-update
        """
        time.sleep(3)
        user1 = Users(0, "somename5", "EMAIL5@outlook.com")
        user1.create()
        user1_id = user1.id
        todo1 = Todos(0, user1_id)
        todo1.create()
        todo1.title = "patched_title"
        todo1.due_on = "2025-12-28"
        todo1.semi_update("title", "due_on")
        todo1.cleanup()

    def test_delete(self):
        """
            Description: Test todos delete
        """
        time.sleep(3)
        user1 = Users(0, "somename6", "EMAIL6@outlook.com")
        user1.create()
        user1_id = user1.id
        todo1 = Todos(0, user1_id)
        todo1.create()
        todo1.delete()
        todo1.cleanup()

    def test_negative_create(self):

        time.sleep(3)

        todo1 = Todos(0, 60000)
        try:
            todo1.create()
        except AssertionError:
            assert todo1.error_field == 'user'
            assert todo1.error_message == 'must exist'

        todo1.cleanup()
