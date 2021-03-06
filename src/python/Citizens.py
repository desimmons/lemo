from src.python.Rule import Rule
from src.python.utilities import crypto_tools
import ecdsa
from ecdsa.util import PRNG


class Citizens:
    def __init__(self):
        self.citizens = []
        self.rules = {}

    def is_citizen(self, citizen):
        if citizen not in self.citizens:
            return False
        else:
            return True

    def add_rule(self, rule):
        if rule.get_result(self)["result"]:
            file_hash = crypto_tools.md5(rule.rule_descriptor_file)
            self.rules.update({rule.rule_name: (file_hash, rule.rule_descriptor_file)})
        else:
            print("Vote has not won")

    def remove_rule(self, rule):
        if not rule.get_result(self)["result"]:
            file_hash = crypto_tools.md5(rule.rule_descriptor_file)
            self.rules.remove({rule.rule_name: (file_hash, rule.rule_descriptor_file)})

    def get_rule(self, **kwargs):
        pass

    @staticmethod
    def is_valid_citizen_format(self, citizen):
        if type(citizen["citizen_name"]) is not str and 30 > len(citizen["citizen_name"]) > 2:
            raise Exception("citizen_name must be a string with length 3 to 30 characters")
        elif not isinstance(citizen["citizen_public_id"], ecdsa.keys.VerifyingKey):
            raise Exception("citizen_public_id must be of type {} not {}"
                            .format(ecdsa.keys.VerifyingKey, type(citizen["citizen_public_id"])))
        elif len(citizen) is not 2:
            raise Exception("citizen must be a dictionary of two attributes: citizen_name and citizen_public_id")
        else:
            return True

    def add_citizen(self, citizen):
        if not self.is_valid_citizen_format(self, citizen):
            raise Exception("Invalid citizen construction")
        else:
            if not self.is_citizen(citizen):
                self.citizens.append(citizen)

    def remove_citizen(self, citizen):
        if not self.is_valid_citizen_format(self, citizen):
            raise Exception("Invalid citizen construction")
        else:
            if self.is_citizen(citizen):
                self.citizens.remove(citizen)  # TODO
            else:
                print(str(citizen) + " is not a citizen!")


if __name__ == "__main__":
    pass