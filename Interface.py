class UserInterface:

    def __init__(self):
        pass

    def get_user_input(self):
        entered_task = int(
            input(
                "enter: 0 for quit"
                "\nenter: 1 for init DB"
                "\nenter: 2 for parsing genres"
                "\nenter: 3 for parsing games"
                "\nenter: 4 for parsing online"
                "\nenter: 5 for parsing news (API method)\n"))
        return entered_task

    def get_user_game(self):
        entered_game = input("enter full name of game\n")
        return entered_game

    def output_end_msg(self, msg):
        print(f"\n{msg} successfully parsed")

    def output_err(self, msg):
        print(f"caused err: {msg}")
