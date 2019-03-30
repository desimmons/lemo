from src.python.Rule import Rule
from src.python.RuleBook import RuleBook
from src.python.utilities import crypto_tools
import ecdsa


class Citizens:
    class __Citizens:
        def __init__(self, arg):
            self.val = arg

        def __str__(self):
            return repr(self) + self.val
    instance = None

    def __init__(self):
        if not Citizens.instance:
            Citizens.instance = Citizens.__Citizens(True)
            self.citizens = []
        else:
            Citizens.instance.val = True

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def is_citizen(self, citizen):
        if citizen not in self.citizens:
            return False
        else:
            return True

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

    citizens = Citizens()
    x = RuleBook("eggs")
    print(x)
    y = RuleBook("sausage")
    print(y)
    z = RuleBook("cuc")
    print(z)

    print(x)
    print(y)

    DS_key = crypto_tools.generate_citizen_pub_priv_key()
    DS = {"citizen_name": "David Simmons", "citizen_public_id": DS_key["citizen_public_id"]}
    NS_key = crypto_tools.generate_citizen_pub_priv_key()
    NS = {"citizen_name": "David Simmons", "citizen_public_id": NS_key["citizen_public_id"]}

    citizens.add_citizen(DS)
    rule_murder = Rule("Murder", "/home/dave/git/lemo/rules/murder.txt")
    rule_theft = Rule("Theft", "/home/dave/git/lemo/rules/theft.txt")
    print(citizens.is_citizen(DS))
    vote = True
    murder_vote_signature = rule_murder.create_vote_signature(DS_key["citizen_private_id"], vote)
    theft_vote_signature = rule_theft.create_vote_signature(DS_key["citizen_private_id"], vote)

    print(murder_vote_signature)
    print(theft_vote_signature)

    rule_murder.vote(citizens, DS, murder_vote_signature, vote)
    rule_theft.vote(citizens, DS, theft_vote_signature, vote)

    print(rule_murder.get_result(citizens))


    print(citizens.citizens)
    citizens.remove_citizen(DS)
    print(citizens.citizens)


