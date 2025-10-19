import sys

def main():
    from dumbdisplay import __version__
    #run_what = None
    show_help = False
    if len(sys.argv) > 1:
        run_what = sys.argv[1]
        if run_what == "--version" or run_what == "-v":
            print(__version__)
            return
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
        if run_what == "--help" or run_what == "-h":
            show_help = True
        else:
            print("Unknown run target:", run_what)
        #return
    if not show_help:
        print("Please specify what to run!!!")
    print(f"DumbDisplay v{__version__}")
    print("Run targets:")
    print(". example.tetris_classic : run Tetris Classic example")
    print(". example.tetris_one_block : run Tetris One Block example")
    print(". example.tetris_two_block : run Tetris Two Block example")
    print(". example.space_shooting : run Space Shooting example")
    print(". --version or -v : show version")
    print(". --help or -h : show help")

if __name__ == "__main__":
    main()