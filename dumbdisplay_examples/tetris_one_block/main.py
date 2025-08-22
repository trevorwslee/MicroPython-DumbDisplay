###
# this is just a sample entrypoint
###

def sample_run():
    import random
    from dumbdisplay_examples.tetris_one_block.tetris_one_block import TetrisOneBlockApp
    print(f"*** Sample Run of TetrisOneBlockApp ***")
    app = TetrisOneBlockApp()
    app.run()


if __name__ == "__main__":
    sample_run()