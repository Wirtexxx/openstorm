from cmd import Cmd


class OpenStormShell(Cmd):
    prompt = "openstorm> "

    def do_status(self, arg):
        print("DB status: running")

    def do_exit(self, arg):
        print("Bye")
        return True
