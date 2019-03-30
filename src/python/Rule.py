from src.python.utilities import crypto_tools
import ecdsa


class Rule:

    def __init__(self, rule_name, rule_descriptor_file):
        self.rule_name = rule_name  # TODO: Check existence
        self.rule_descriptor_file = rule_descriptor_file
        self.rule_hash = crypto_tools.md5(self.rule_descriptor_file)
        self.yes_count = 0
        self.no_count = 0
        self.signatures = []

    def __str__(self):
        return repr(self) + ": " + self.rule_name

    def __change_vote(self, vote_boolean):
        if vote_boolean is True:
            self.yes_count += 1
            self.no_count -= 1
            return "You voted yes for the rule %s, with file description %s".format(self.rule_name,
                                                                                    self.rule_descriptor_file)
        elif vote_boolean is False:
            self.no_count += 1
            self.yes_count -= 1
            return "You voted no for the rule %s, with file description %s".format(self.rule_name,
                                                                                   self.rule_descriptor_file)
        else:
            ValueError()

    def __add_vote(self, vote_boolean):
        if vote_boolean is True:
            self.yes_count += 1
            return "You voted yes for the rule %s, with file description %s".format(self.rule_name,
                                                                                    self.rule_descriptor_file)
        elif vote_boolean is False:
            self.no_count += 1
            return "You voted no for the rule %s, with file description %s".format(self.rule_name,
                                                                                   self.rule_descriptor_file)
        else:
            ValueError()

    def create_vote_signature(self, sk, vote):
        message = bytes(str(vote)+str(self.rule_hash), 'utf-8')
        signed_vote = sk.sign_deterministic(message)
        return signed_vote

    def vote(self, citizens, citizen, vote_signature, vote):
        # check signature and public key are valid
        if not citizens.is_citizen(citizen):
            raise Exception("Citizen trying to vote is not real citizen")
        elif type(vote) is not bool:
            raise Exception("Vote is not of type bool")
        elif vote_signature in self.signatures:
            raise Exception("Vote has already been made")
        else:
            message = bytes(str(vote)+str(self.rule_hash), 'utf-8')
            message_comp = bytes(str(not vote)+str(self.rule_hash), 'utf-8')
            vk = ecdsa.VerifyingKey.from_string(citizen["citizen_public_id"].to_string(), curve=ecdsa.SECP256k1)
            changing_vote = False
            for sig in self.signatures:
                try:
                    if vk.verify(sig, message_comp):
                        changing_vote = True
                        original_signature = sig
                except ecdsa.keys.BadSignatureError:
                    pass

            if not vk.verify(vote_signature, message):
                raise Exception("Invalid vote signature")
            elif changing_vote:
                self.signatures.append(vote_signature)
                self.signatures.remove(original_signature)
                self.__change_vote(vote)
            else:
                self.signatures.append(vote_signature)
                self.__add_vote(vote)

    def get_result(self, citizens):
        in_favour_ratio = self.yes_count / len(citizens.citizens)
        if in_favour_ratio > 0.5:
            return {"in_favour_ratio": in_favour_ratio, "result": True}
        else:
            return {"in_favour_ratio": in_favour_ratio, "result": False}

    def get_current_result(self, **kwargs):
        pass


if __name__ == "__main__":
    pass
