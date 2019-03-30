from src.python.utilities import crypto_tools


class RuleBook:
    class __RuleBook:
        def __init__(self, citizens):
            self.citizens = citizens
            self.rules = {}

        def __str__(self):
            return repr(self) + self.citizens

        def add_rule(self, rule):
            if rule.get_result(self.citizens)["result"]:
                file_hash = crypto_tools.md5(rule.rule_descriptor_file)
                self.rules.update({rule.rule_name: (file_hash, rule.rule_descriptor_file)})
            else:
                print("Vote has not won")

        def remove_rule(self, rule):
            if not rule.get_result(self.citizens)["result"]:
                file_hash = crypto_tools.md5(rule.rule_descriptor_file)
                self.rules.remove({rule.rule_name: (file_hash, rule.rule_descriptor_file)})

        def get_rule(self, **kwargs):
            pass

    instance = None

    def __init__(self, citizens):
        if not RuleBook.instance:
            RuleBook.instance = RuleBook.__RuleBook(citizens)
        else:
            print("New RuleBook instance not created")

    def __getattr__(self, name):
        return getattr(self.instance, name)


if __name__ == "__main__":
    rule_book = RuleBook("The Law")
    rule_book.add_rule("murder", "../../rules/murder.txt")
    a = 1
