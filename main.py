import datetime

user_dict = {
    "705131444": "Aanish Farrukh"
}


def inputread():
    id = input("Please enter your ID (or type 'quit' to exit): ")
    return id


def get_name_by_id(id, user_dict):
    id_first_9 = id[:9]
    if id_first_9 in user_dict:
        return user_dict[id_first_9]
    else:
        return None


while True:
    entered_id = inputread()

    if entered_id.lower() == "quit":
        print("Exiting the program.")
        break

    name = get_name_by_id(entered_id, user_dict)
    if name:
        current_time = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-4)))
        print(f"{name} is here! Time: {current_time.strftime('%I:%M:%S %p')}")
    else:
        print("ID not found")
