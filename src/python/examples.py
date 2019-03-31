from src.python.Rule import Rule
from src.python.utilities import crypto_tools
from ecdsa.util import PRNG
from src.python import Citizens


def example_1():

    print("\nexample_1():\n\nThis example verifies non citizens cannot vote" +
          "\n\nDefine a Citizens object, which allows citizens to be members and vote")
    citizens = Citizens.Citizens()

    print("Define three citizens ds, ts, and ns")
    ds_key = crypto_tools.generate_citizen_pub_priv_key(entropy = PRNG("1"))
    ds = {"citizen_name": "David S", "citizen_public_id": ds_key["citizen_public_id"]}
    ns_key = crypto_tools.generate_citizen_pub_priv_key(entropy = PRNG("2"))
    ns = {"citizen_name": "Nidhi S", "citizen_public_id": ns_key["citizen_public_id"]}
    ts_key = crypto_tools.generate_citizen_pub_priv_key(entropy=PRNG("3"))
    ts = {"citizen_name": "Tim S", "citizen_public_id": ts_key["citizen_public_id"]}

    print("Allow ds and ts to become members of Citizens")
    citizens.add_citizen(ds)
    citizens.add_citizen(ts)

    print("Create two rules")
    rule_murder = Rule("Murder", "/home/dave/git/lemo/rules/murder.txt")

    print("Define the opinions of each of the citizens on the rules")
    ds_rule_murder_vote = True
    ns_rule_murder_vote = True
    ts_rule_murder_vote = True

    print("Generate a vote signature which verifies that the citizen voted for the particular rule")
    ds_murder_vote_sig = rule_murder.create_vote_signature(ds_key["citizen_private_id"], ds_rule_murder_vote)
    ns_murder_vote_sig = rule_murder.create_vote_signature(ns_key["citizen_private_id"], ns_rule_murder_vote)
    ts_murder_vote_sig = rule_murder.create_vote_signature(ts_key["citizen_private_id"], ts_rule_murder_vote)

    print("Allow the citizens to vote")
    rule_murder.vote(citizens, ds, ds_murder_vote_sig, ds_rule_murder_vote)
    print(rule_murder.get_result(citizens))
    rule_murder.vote(citizens, ts, ts_murder_vote_sig, ts_rule_murder_vote)
    print(rule_murder.get_result(citizens))
    print("See that ns was not a member of Citizens so could not vote")
    rule_murder.vote(citizens, ns, ns_murder_vote_sig, ns_rule_murder_vote)
    print(rule_murder.get_result(citizens))

    print("Allow ns to become members of Citizens and vote")
    citizens.add_citizen(ns)
    rule_murder.vote(citizens, ns, ns_murder_vote_sig, ns_rule_murder_vote)
    print(rule_murder.get_result(citizens))


def example_2():

    print("\nexample_2():\n\nThis example verifies citizens can change their vote\n\n" +
          "Define a Citizens object, which allows citizens to be members and vote")
    citizens = Citizens.Citizens()

    print("Define three citizens ds, ts, and ns")
    ds_key = crypto_tools.generate_citizen_pub_priv_key(entropy = PRNG("1"))
    ds = {"citizen_name": "David S", "citizen_public_id": ds_key["citizen_public_id"]}
    ns_key = crypto_tools.generate_citizen_pub_priv_key(entropy = PRNG("2"))
    ns = {"citizen_name": "Nidhi S", "citizen_public_id": ns_key["citizen_public_id"]}
    ts_key = crypto_tools.generate_citizen_pub_priv_key(entropy=PRNG("3"))
    ts = {"citizen_name": "Tim S", "citizen_public_id": ts_key["citizen_public_id"]}

    print("Allow ds, ns, and ts to become members of Citizens")
    citizens.add_citizen(ds)
    citizens.add_citizen(ts)
    citizens.add_citizen(ns)

    print("Create a rule")
    rule_murder = Rule("Murder", "/home/dave/git/lemo/rules/murder.txt")

    print("Define the opinions of each of the citizens on the rule")
    ds_rule_murder_vote = True
    ns_rule_murder_vote = True
    ts_rule_murder_vote = True

    print("Generate a vote signature which verifies that the citizen voted for the particular rule")
    ds_murder_vote_sig = rule_murder.create_vote_signature(ds_key["citizen_private_id"], ds_rule_murder_vote)
    ns_murder_vote_sig = rule_murder.create_vote_signature(ns_key["citizen_private_id"], ns_rule_murder_vote)
    ts_murder_vote_sig = rule_murder.create_vote_signature(ts_key["citizen_private_id"], ts_rule_murder_vote)

    print("Allow the citizens to vote")
    rule_murder.vote(citizens, ds, ds_murder_vote_sig, ds_rule_murder_vote)
    print(rule_murder.get_result(citizens))
    rule_murder.vote(citizens, ts, ts_murder_vote_sig, ts_rule_murder_vote)
    print(rule_murder.get_result(citizens))
    rule_murder.vote(citizens, ns, ns_murder_vote_sig, ns_rule_murder_vote)
    print(rule_murder.get_result(citizens))

    print("ds decides to change his opinion about murder")
    ds_murder_vote_sig = rule_murder.create_vote_signature(ds_key["citizen_private_id"], not ds_rule_murder_vote)
    rule_murder.vote(citizens, ds, ds_murder_vote_sig, not ds_rule_murder_vote)
    print(rule_murder.get_result(citizens))


def example_3():

    print("\nexample_3():\n\nThis verifies citizens cannot vote the same more than once\n\n" +
          "Define a Citizens object, which allows citizens to be members and vote")
    citizens = Citizens.Citizens()

    print("Define three citizens ds, ts, and ns")
    ds_key = crypto_tools.generate_citizen_pub_priv_key(entropy = PRNG("1"))
    ds = {"citizen_name": "David S", "citizen_public_id": ds_key["citizen_public_id"]}
    ts_key = crypto_tools.generate_citizen_pub_priv_key(entropy=PRNG("3"))
    ts = {"citizen_name": "Tim S", "citizen_public_id": ts_key["citizen_public_id"]}

    print("Allow ds and ts to become members of Citizens")
    citizens.add_citizen(ds)
    citizens.add_citizen(ts)

    print("Create two rules")
    rule_murder = Rule("Murder", "/home/dave/git/lemo/rules/murder.txt")

    print("Define the opinions of each of the citizens on the rules")
    ds_rule_murder_vote = True
    ts_rule_murder_vote = True

    print("Generate a vote signature which verifies that the citizen voted for the particular rule")
    ds_murder_vote_sig = rule_murder.create_vote_signature(ds_key["citizen_private_id"], ds_rule_murder_vote)
    ts_murder_vote_sig = rule_murder.create_vote_signature(ts_key["citizen_private_id"], ts_rule_murder_vote)

    print("Allow the citizens to vote")
    rule_murder.vote(citizens, ds, ds_murder_vote_sig, ds_rule_murder_vote)
    print(rule_murder.get_result(citizens))
    rule_murder.vote(citizens, ts, ts_murder_vote_sig, ts_rule_murder_vote)
    print(rule_murder.get_result(citizens))

    print("ds tries to vote again")
    rule_murder.vote(citizens, ds, ds_murder_vote_sig, ds_rule_murder_vote)


def example_4():
    print("\nexample_4():\n\nThis verifies citizens cannot introduce fraudulent signatures to vote more than once\n\n" +
          "Define a Citizens object, which allows citizens to be members and vote")
    citizens = Citizens.Citizens()

    print("Define three citizens ds, ts, and ns")
    ds_key = crypto_tools.generate_citizen_pub_priv_key(entropy=PRNG("1"))
    ds = {"citizen_name": "David S", "citizen_public_id": ds_key["citizen_public_id"]}
    ns_key = crypto_tools.generate_citizen_pub_priv_key(entropy=PRNG("2"))
    ns = {"citizen_name": "Nidhi S", "citizen_public_id": ns_key["citizen_public_id"]}
    ts_key = crypto_tools.generate_citizen_pub_priv_key(entropy=PRNG("3"))
    ts = {"citizen_name": "Tim S", "citizen_public_id": ts_key["citizen_public_id"]}

    print("Allow ds and ts to become members of Citizens")
    citizens.add_citizen(ds)
    citizens.add_citizen(ts)

    print("Create two rules")
    rule_murder = Rule("Murder", "/home/dave/git/lemo/rules/murder.txt")
    rule_theft = Rule("Theft", "/home/dave/git/lemo/rules/theft.txt")

    print("Define the opinions of each of the citizens on the rules")
    ds_rule_murder_vote = True
    ns_rule_murder_vote = True
    ts_rule_murder_vote = True

    ds_rule_theft_vote = True
    ns_rule_theft_vote = False
    ts_rule_theft_vote = True

    print("Generate a vote signature which verifies that the citizen voted for the particular rule")
    ds_murder_vote_sig = rule_murder.create_vote_signature(ds_key["citizen_private_id"], ds_rule_murder_vote)
    ns_murder_vote_sig = rule_murder.create_vote_signature(ns_key["citizen_private_id"], ns_rule_murder_vote)
    ts_murder_vote_sig = rule_murder.create_vote_signature(ts_key["citizen_private_id"], ts_rule_murder_vote)

    ds_theft_vote_sig = rule_theft.create_vote_signature(ds_key["citizen_private_id"], ds_rule_theft_vote)
    ns_theft_vote_sig = rule_theft.create_vote_signature(ns_key["citizen_private_id"], ns_rule_theft_vote)
    ts_theft_vote_sig = rule_theft.create_vote_signature(ts_key["citizen_private_id"], ts_rule_theft_vote)

    print("Allow the citizens to vote")
    rule_murder.vote(citizens, ds, ds_murder_vote_sig, ds_rule_murder_vote)
    print(rule_murder.get_result(citizens))
    rule_murder.vote(citizens, ts, ts_murder_vote_sig, ts_rule_murder_vote)
    print(rule_murder.get_result(citizens))

    print("ds tries to vote again")
    rule_murder.vote(citizens, ds, ds_murder_vote_sig, ds_rule_murder_vote)

    print("See that ns was not a member of Citizens so could not vote")
    rule_murder.vote(citizens, ns, ns_murder_vote_sig, ns_rule_murder_vote)
    print(rule_murder.get_result(citizens))

    print("Allow ns to become members of Citizens and vote")
    citizens.add_citizen(ns)
    rule_murder.vote(citizens, ns, ns_murder_vote_sig, ns_rule_murder_vote)
    print(rule_murder.get_result(citizens))

    print("ds decides to change his opinion about murder")
    ds_murder_vote_sig = rule_murder.create_vote_signature(ds_key["citizen_private_id"], not ds_rule_murder_vote)
    rule_murder.vote(citizens, ds, ds_murder_vote_sig, not ds_rule_murder_vote)
    print(rule_murder.get_result(citizens))

    print("All three citizens vote for theft")
    rule_theft.vote(citizens, ds, ds_theft_vote_sig, ds_rule_theft_vote)
    print(rule_theft.get_result(citizens))
    rule_theft.vote(citizens, ns, ns_theft_vote_sig, ns_rule_theft_vote)
    print(rule_theft.get_result(citizens))
    rule_theft.vote(citizens, ts, ts_theft_vote_sig, ts_rule_theft_vote)
    print(rule_theft.get_result(citizens))

    print("ns tries (and fails) to apply her theft sig to murder vote to cheat system")
    rule_murder.vote(citizens, ns, ns_theft_vote_sig, ns_rule_theft_vote)
    print(rule_theft.get_result(citizens))


if __name__ == "__main__":

    example_1()
    example_2()
    example_3()
    example_4()

