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

    print("Define a Citizens object, which allows citizens to be members and vote")
    citizens = Citizens()

    print("Define three citizens DS, TS, and NS")
    DS_key = crypto_tools.generate_citizen_pub_priv_key(entropy = PRNG("1"))
    DS = {"citizen_name": "David S", "citizen_public_id": DS_key["citizen_public_id"]}
    NS_key = crypto_tools.generate_citizen_pub_priv_key(entropy = PRNG("2"))
    NS = {"citizen_name": "Nidhi S", "citizen_public_id": NS_key["citizen_public_id"]}
    TS_key = crypto_tools.generate_citizen_pub_priv_key(entropy=PRNG("3"))
    TS = {"citizen_name": "Tim S", "citizen_public_id": TS_key["citizen_public_id"]}

    print("Allow DS and TS to become members of Citizens")
    citizens.add_citizen(DS)
    citizens.add_citizen(TS)

    print("Create two rules")
    rule_murder = Rule("Murder", "/home/dave/git/lemo/rules/murder.txt")
    rule_theft = Rule("Theft", "/home/dave/git/lemo/rules/theft.txt")

    print("Define the opinions of each of the citizens on the rules")
    DS_rule_murder_vote = True
    NS_rule_murder_vote = True
    TS_rule_murder_vote = True

    DS_rule_theft_vote = True
    NS_rule_theft_vote = False
    TS_rule_theft_vote = True

    print("Generate a vote signature which verifies that the citizen voted for the particular rule")
    DS_murder_vote_sig = rule_murder.create_vote_signature(DS_key["citizen_private_id"], DS_rule_murder_vote)
    NS_murder_vote_sig = rule_murder.create_vote_signature(NS_key["citizen_private_id"], NS_rule_murder_vote)
    TS_murder_vote_sig = rule_murder.create_vote_signature(TS_key["citizen_private_id"], TS_rule_murder_vote)

    DS_theft_vote_sig = rule_theft.create_vote_signature(DS_key["citizen_private_id"], DS_rule_theft_vote)
    NS_theft_vote_sig = rule_theft.create_vote_signature(NS_key["citizen_private_id"], NS_rule_theft_vote)
    TS_theft_vote_sig = rule_theft.create_vote_signature(TS_key["citizen_private_id"], TS_rule_theft_vote)

    print("Allow the citizens to vote")
    rule_murder.vote(citizens, DS, DS_murder_vote_sig, DS_rule_murder_vote)
    print(rule_murder.get_result(citizens))
    rule_murder.vote(citizens, TS, TS_murder_vote_sig, TS_rule_murder_vote)
    print(rule_murder.get_result(citizens))

    print("DS tries to vote again")
    rule_murder.vote(citizens, DS, DS_murder_vote_sig, DS_rule_murder_vote)

    print("See that NS was not a member of Citizens so could not vote")
    rule_murder.vote(citizens, NS, NS_murder_vote_sig, NS_rule_murder_vote)
    print(rule_murder.get_result(citizens))

    print("Allow NS to become members of Citizens and vote")
    citizens.add_citizen(NS)
    rule_murder.vote(citizens, NS, NS_murder_vote_sig, NS_rule_murder_vote)
    print(rule_murder.get_result(citizens))

    print("DS decides to change his opinion about murder")
    DS_murder_vote_sig = rule_murder.create_vote_signature(DS_key["citizen_private_id"], not DS_rule_murder_vote)
    rule_murder.vote(citizens, DS, DS_murder_vote_sig, not DS_rule_murder_vote)
    print(rule_murder.get_result(citizens))

    print("All three citizens vote for theft")
    rule_theft.vote(citizens, DS, DS_theft_vote_sig, DS_rule_theft_vote)
    print(rule_theft.get_result(citizens))
    rule_theft.vote(citizens, NS, NS_theft_vote_sig, NS_rule_theft_vote)
    print(rule_theft.get_result(citizens))
    rule_theft.vote(citizens, TS, TS_theft_vote_sig, TS_rule_theft_vote)
    print(rule_theft.get_result(citizens))

    print("NS tries (and fails) to apply her theft sig to murder vote to cheat system")
    rule_murder.vote(citizens, NS, NS_theft_vote_sig, NS_rule_theft_vote)
    print(rule_theft.get_result(citizens))

