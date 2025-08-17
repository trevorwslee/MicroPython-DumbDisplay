###
# this is just a sample entrypoint
###

def sample_run():
    from dumbdisplay_examples.passive_blink.passive_blink_app import PassiveBlinkApp
    print(f"*** Sample Run of PassiveBlinkApp ***")
    app = PassiveBlinkApp()
    app.run()


if __name__ == "__main__":
    sample_run()