###
# this is just a sample entrypoint
###

def sample_run():
    import random
    from dumbdisplay_examples.sliding_puzzle.sliding_puzzle_app import SlidingPuzzleApp
    print(f"*** Sample Run of SlidingPuzzleApp ***")
    suggest_move_from_dir_func = lambda board_manager: random.randint(0, 3)
    app = SlidingPuzzleApp(suggest_move_from_dir_func=suggest_move_from_dir_func)
    app.run()


sample_run()