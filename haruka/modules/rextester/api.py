import requests

from haruka.modules.rextester.langs import languages

### API warper for rextester.com
## Author: Nitan Alexandru Marcel.
# LICENSE and github repo at https://github.com/nitanmarcel/rextester_cli

URL = "https://rextester.com/rundotnet/api"


class Rextester:
    def __init__(self, lang, code, stdin):
        if lang not in languages:
            raise CompilerError("Unknown language")

        data = {"LanguageChoice": languages[lang], "Program": code, "Input": stdin}

        request = requests.post(URL, data=data)
        self.response = request.json()
        self.result = self.response["Result"]
        self.warnings = self.response["Warnings"]
        self.errors = self.response["Errors"]
        self.stats = self.response["Stats"]
        self.files = self.response["Files"]

        if not code:
            raise CompilerError("Invalid Query")

        elif not any([self.result, self.warnings, self.errors]):
            raise CompilerError("Did you forget to output something?")


class CompilerError(Exception):
    pass
