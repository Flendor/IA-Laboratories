import game

state = game.State()
winner = state.get_winner()
while winner is None:
    game.Screen.draw(state.board)
    state = game.HumanStrategy.play(state)
    game.Screen.draw(state.board)
    # bot plays
    winner = state.get_winner()
game.Screen.draw(state.board)
if winner == game.PlayerTypes.HUMAN:
    print('YOU WON!!!!!!!!!!!!!!!!!!')
else:
    print("""     ,     ,
    (\\____/)
     (_oo_)
       (O)
     __||__    \\)
  []/______\\[] /
  / \\______/ \\/
 /    /__\\ We won at checkers!
(\\   /____\\ We are ready to take over the world!""")
