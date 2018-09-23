import fire
import re
import subprocess

from colorama import Fore, Back, Style


class Subversion:
    def status(self):
        process = subprocess.run(["svn", "status"], stdout=subprocess.PIPE)

        output = process.stdout.decode("utf-8")
        lines = output.splitlines()

        types = {
            "A": {
                "message": "Inserted files:",
                "color": Fore.BLUE,
                "desc": "inserted:\t",
            },
            "M": {
                "message": "Updated files:",
                "color": Fore.GREEN,
                "desc": "modified:\t",
            },
            "!": {
                "message": "Warning files:",
                "color": Fore.YELLOW,
                "desc": "warning:\t",
            },
            "?": {
                "message": "Not tracked files:",
                "color": Fore.RED,
                "desc": "not tracked\t",
            },
        }

        for type, data in types.items():
            print(data["color"] + data["message"])
            for line in lines:
                if line[0] == type:
                    print(data["color"] + data["desc"] + line)
            print("\n")

    def add(self, file):
        find_process = subprocess.run(["find", file], stdout=subprocess.PIPE)
        stat_process = subprocess.run(["svn", "status"], stdout=subprocess.PIPE)

        find_files = find_process.stdout.decode("utf-8")
        files = find_files.splitlines()

        stat_files = stat_process.stdout.decode("utf-8")
        lines = stat_files.splitlines()
        lines = [line for line in lines if line[0] == "?"]
        lines = ["." if line[8:] == "." else "./" + line[8:] for line in lines]

        valid_files = [val for val in files if val in lines]

        for file in valid_files:
            subprocess.run(["svn", "add", file], stdout=subprocess.PIPE)


if __name__ == "__main__":
    fire.Fire(Subversion)
