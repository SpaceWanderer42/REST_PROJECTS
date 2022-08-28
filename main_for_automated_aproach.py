from framework_automated_aproach import *

users = Users()
posts = Posts()
comments = Comments()
todos = Todos()
base = Base()
# apis = [users, posts, comments, todos]

print("Type which action: [retrieve, create, create and retrieve, update, semi-update, delete, cleanup]")
action = input()


if action == "retrieve":
    print("Do you want to retrieve all? [y/n]")  # nu o sa fie all pt ca sunt paginate api-urile
    decision = input()
    if decision == "y":
        base.retrieve_all()
    else:
        print("Type which API: [users, posts, comments, todos]")
        api = input()
        print("Specify the ID you want: \nTo retrieve the whole page, just leave blank and press enter if no specific ID")
        ID = input()

        if api == 'users':
            if ID=='':
                base.retrieve_all('users')
            else:
                users.retrieve(ID)

        elif api == 'posts':
            if ID=='':
                base.retrieve_all('posts')
            else:
                posts.retrieve(ID)

        elif api == 'comments':
            if ID=='':
                base.retrieve_all('comments')
            else:
                comments.retrieve(ID)

        elif api == 'todos':
            if ID=='':
                base.retrieve_all('todos')
            else:
                todos.retrieve(ID)

# if action == "retrieve":
#     print("Do you want to retrieve all? [y/n]")  # nu o sa fie all pt ca sunt paginate api-urile
#     decision = input()
#     if decision == "y":
#         base.retrieve_all()
#     else:
#         print("Type which API: [users, posts, comments, todos]")
#         api = input()
#
#         if api == 'users':
#
#             print("Do you want a specified ID? [y/n] : ")
#             res = input()
#             specified_id = False
#             if res == 'y':
#                 specified_id = True
#             base.retrieve('users', specified_id)
#
#         elif api == 'posts':
#
#             print("Do you want a specified ID? [y/n] : ")
#             res = input()
#             specified_id = False
#             if res == 'y':
#                 specified_id = True
#             base.retrieve('posts', specified_id)
#
#         elif api == 'comments':
#
#             print("Do you want a specified ID? [y/n] : ")
#             res = input()
#             specified_id = False
#             if res == 'y':
#                 specified_id = True
#             base.retrieve('comments', specified_id)
#
#         elif api == 'todos':
#
#             print("Do you want a specified ID? [y/n] : ")
#             res = input()
#             specified_id = False
#             if res == 'y':
#                 specified_id = True
#             base.retrieve('todos', specified_id)

elif action == 'create':
    print("Type which API: [users, posts, comments, todos]")
    api = input()

    if api == 'users':

        users.create()
        users.creation_status()

    elif api == 'posts':

        posts.create()
        posts.creation_status()

    elif api == 'comments':

        comments.create()
        comments.creation_status()

    elif api == 'todos':

        todos.create()
        todos.creation_status()


elif action == 'update':
    print("Type which API: [users, posts, comments, todos]")
    api = input()

    if api == 'users':

        users.update()

    elif api == 'posts':

        posts.update()

    elif api == 'comments':

        comments.update()

    elif api == 'todos':

        todos.update()


elif action == 'semi-update':
    print("Type which API: [users, posts, comments, todos]")
    api = input()

    if api == "users":

        users.semi_update("gender")

    elif api == "posts":
        posts.semi_update("title")

    elif api == "comments":
        comments.semi_update("name", "body")

    elif api == "todos":
        todos.semi_update("title")


elif action == 'delete':
    print("Type which API: [users, posts, comments, todos]")
    api = input()
    print("Specify ID: ")
    ID = input()
    if api == 'users':
        users.delete(ID)
    elif api == 'posts':
        posts.delete(ID)
    elif api == 'comments':
        comments.delete(ID)
    elif api == 'todos':
        todos.delete(ID)

elif action == 'cleanup':

    bla1 = Users(0, "apaca", "alabala@bla.co", "male", "active")
    bla2 = Posts(0, 0, "ehehee", "hahahaa")
    bla3 = Comments(0, 0, "hfhdg", "hhff@kdkd.co", "jjj")
    bla4 = Todos(0, 0, "caramba", "2022-10-30", 'completed')

    bla1.create()
    bla2.create()
    bla3.create()
    bla4.create()

    # users.create()
    # posts.create()
    # users.create()
    # comments.create()
    # todos.create()
    # todos.create()
    # users.create()
    # comments.create()
    # posts.create()

    base.cleanup()

elif action == 'create and retrieve':

    user1 = Users(0, "apaca", "alabala@bla.co", "male", "active")
    user1.create()
    user1.retrieve()
