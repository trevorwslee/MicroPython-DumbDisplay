###
# this is just a sample entrypoint
###


def sample_run():
    import random
    from dumbdisplay_examples.mnist.mnist_app import MnistApp
    print(f"*** Sample run of MnistApp ***")
    inference_func = lambda board_manager: random.randint(0, 9)
    app = MnistApp(inference_func=inference_func)
    app.run()


if __name__ == "__main__":
    sample_run()