class Game:
    def __init__(self):
        self.room = "initial_room"
        self.player_turn = 0
        self.room_enemies = 5
        self.available_moves = ["left","right","up","down"]

    def play(self):
        print( "##### WELCOME TO RPG ####")
        print("\n How to play:")
        print(" Something.")
        print("enjoy!")
        print("you are in: " + self.room + "- have " + str(self.room_enemies) + " enemies alive" + " and you can move to")
        print(self.available_moves)


if __name__ == '__main__':
    game = Game()
    game.play()
