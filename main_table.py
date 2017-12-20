__author__ = 'harshini bonam'


pref_rating_keys = ["HighlyRecommend", "StronglyLike", "Like", "SomewhatLike", "NoComment", "SomewhatDislike", "Dislike", "StronglyDislike", "Hate", ""]
pref_rating_values = [[1.0,0,0,0,0],[0.8,0.2,0,0,0],[0.6,0.3,0.1,0,0],[0.5,0.4,0.1,0,0],[0,0.3,0.4,0.3,0],[0,0,0.2,0.6,0.2],[0,0,0.1,0.4,0.5],[0,0,0,0.2,0.8],[0,0,0,0,1.0], [0,0,0,0,0]]
pref_rating = dict(zip(iter(pref_rating_keys), iter(pref_rating_values)))
pref_values = {'Hate': 1, 'StronglyDislike': 1.5, 'Dislike': 2, 'SomewhatDislike': 2.5, 'NoComment': 3, 'SomewhatLike': 3.5, 'Like': 4, 'StronglyLike': 4.5, 'StronglyRecommend': 5}
predictive_rating = {1: 'Hate', 1.5: 'StronglyDislike', 2: 'Dislike', 2.5: 'SomewhatDislike', 3: 'NoComment', 3.5: 'SomewhatLike', 4: 'Like', 4.5: 'StronglyLike', 5: 'StronglyRecommend'}

def use_existing_db():
    users = ["us1", "us2", "u1", "u2", "u3", "u4", "u5", "u6", "u7", "u8", "u9", "u10", "u11", "u12", "u13", "u14", "u15"]
    objective_users = ["u1", "u2", "u3", "u4", "u5", "u6", "u7", "u8", "u9", "u10", "u11", "u12", "u13", "u14", "u15"]
    subjective_users = ["us1", "us2"]
    active_user = "u11"
    items = ["i1", "i2", "i3", "i4", "i5"]
    simple_db ={     'us1': {'i1': 'Like', 'i3': 'Dislike', 'i2': 'StronglyLike', 'i5': 'Like', 'i4': 'StronglyDislike'},
                     'us2': {'i1': 'SomewhatLike', 'i3': 'Dislike', 'i2': 'Like', 'i5': 'StronglyLike', 'i4': 'Hate'},
                     'u1': {'i1': '', 'i3': 'Dislike', 'i2': 'Dislike', 'i5': 'NoComment', 'i4': 'StronglyLike'},
                     'u2': {'i1': 'StronglyLike', 'i3': '', 'i2': '', 'i5': 'HighlyRecommend', 'i4': 'StronglyDislike'},
                     'u3': {'i1': 'StronglyDislike', 'i3': 'StronglyLike', 'i2': 'Hate', 'i5': 'SomewhatDislike', 'i4': 'StronglyLike'},
                     'u4': {'i1': '', 'i3': '', 'i2': 'StronglyLike', 'i5': 'StronglyLike', 'i4': 'SomewhatDislike'},
                     'u5': {'i1': 'Dislike', 'i3': '', 'i2': 'Dislike', 'i5': 'StronglyDislike', 'i4': 'HighlyRecommend'},
                     'u6': {'i1': 'SomewhatDislike', 'i3': 'Dislike', 'i2': '', 'i5': 'HighlyRecommend', 'i4': ''},
                     'u7': {'i1': 'NoComment', 'i3': 'NoComment', 'i2': '', 'i5': 'SomewhatLike', 'i4': ''},
                     'u8': {'i1': '', 'i3': '', 'i2': 'Hate', 'i5': 'SomewhatDislike', 'i4': 'NoComment'},
                     'u9': {'i1': '', 'i3': 'Dislike', 'i2': 'HighlyRecommend', 'i5': 'StronglyLike', 'i4': ''},
                     'u10': {'i1': 'Dislike', 'i3': '', 'i2': '', 'i5': 'NoComment', 'i4': ''},
                     'u11': {'i1': 'NoComment', 'i3': 'StronglyDislike', 'i2': 'HighlyRecommend', 'i5': '', 'i4': 'SomewhatDislike'},
                     'u12': {'i1': 'Hate', 'i3': '', 'i2': 'StronglyDislike', 'i5': 'StronglyDislike', 'i4': 'HighlyRecommend'},
                     'u13': {'i1': 'NoComment', 'i3': 'NoComment', 'i2': 'NoComment', 'i5': 'NoComment', 'i4': ''},
                     'u14': {'i1': '', 'i3': '', 'i2': 'Dislike', 'i5': 'StronglyDislike', 'i4': ''},
                     'u15': {'i1': '', 'i3': '', 'i2': '', 'i5': '', 'i4': ''}}
    return [users,objective_users,subjective_users,active_user,items,simple_db]

def get_things(count, thing):
    thing_list = []
    for k in range(count):
        thing_list.append(raw_input("\nEnter name in the format '"+thing+"i' : "))
    return thing_list

def create_new_simple_db():
    number_of_items = raw_input("\nEnter the number of items : ")
    items = get_things(int(number_of_items), "i")
    number_of_us = raw_input("\nEnter the number of subjective users :")
    subjective_users = get_things(int(number_of_us), "us")
    number_of_uo  =raw_input("\nEnter the number of objective users : ")
    objective_users = get_things(int(number_of_uo), "u")
    users = subjective_users + objective_users
    active_user  = raw_input("\nEnter the active user : ")

    empty_list_dicts = []
    for i in range(users.__len__()):
        empty_list_dicts[i] = dict()

    simple_db = dict(zip(users, empty_list_dicts))
    print "\ncreate DB--\n",simple_db
    for user in users:
        for item in items:
            simple_db[user][item] = raw_input("Enter the user "+user+" rating for item "+item+" : ")

    print "\nNew Simple DB--\n", simple_db
    return [users,objective_users,subjective_users,active_user,items,simple_db]

