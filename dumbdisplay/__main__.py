import sys

def main():
    run_what = None
    if len(sys.argv) > 1:
        run_what = sys.argv[1]
        if run_what == "example.tetris_classic":
            from dumbdisplay_examples.tetris.tetris_classic import run_tetris_classic
            run_tetris_classic()
            return
        if run_what == "example.tetris_one_block":
            from dumbdisplay_examples.tetris.tetris_one_block import run_tetris_one_block
            run_tetris_one_block()
            return
        if run_what == "example.tetris_two_block":
            from dumbdisplay_examples.tetris.tetris_two_block import run_tetris_two_block
            run_tetris_two_block()
            return
        if run_what == "example.space_shooting":
            from dumbdisplay_examples.space_shooting.space_shooting import run_space_shooting
            run_space_shooting()
            return
        print("Unknown run target:", run_what)
        return
    print("Please specifc what to run")

if __name__ == "__main__":
    main()