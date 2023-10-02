import argparse
import time

import yaml

from sleuthconf import web
from sleuthconf.clicker import Clicker
from sleuthconf.trivia import Trivia
from sleuthconf.window import Window


def main():
    parser = argparse.ArgumentParser(description="The conference content server")
    parser.add_argument("trivia", help="The trivia YAML file")
    opts = parser.parse_args()

    with open(opts.trivia, "r") as stream:
        try:
            data = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            exit(1)

    window = Window()
    trivia = Trivia(data)

    clicker = Clicker(window, trivia, data)
    clicker.start()

    try:
        app = web.create_app(trivia)
        app.run(use_reloader=True)
    except KeyboardInterrupt:
        pass
    clicker.stop()
    print("done!")


if __name__ == "__main__":
    main()

