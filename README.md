# Lemo - (L)iquid D(emo)cracy

Lemo is an implementation of a cryptographically verifiable democracy.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

To run this project easily, [install miniconda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html).


### Installing

Clone the GitHub repository into a local directory of your choice:

```
git clone git@github.com:desimmons/lemo.git
```

Move into the cloned directory:

```
cd lemo
```

Create a Python environment with all the lemo dependencies installed using Conda:

```
conda env create -f environment.yml
```


## Running the tests


To run an example:

```
python ./src/python/examples.py
```

## What it does

Lemocracy is a cryptographic implementation of a [liquid democracy](https://en.wikipedia.org/wiki/Delegative_democracy):
 a direct democracy that allows citizens to delegate their vote to representatives of their choice. In detail, it 
 allows us to create:
1. A citizen, represented by a name and public key (of which there is a corresponding private key). The citizen's 
public/private key pair is generated using ```jb_key = crypto_tools.generate_citizen_pub_priv_key(entropy=PRNG("seed"))```. 
The citizen is then defined to be the dictionary ```joey_b = {"citizen_name": "Joe Blogs", 
"citizen_public_id": key["citizen_public_id"]}```
2. A Citizens class, that:
    * issues citizenship via ```Citizens().add_citizen(joey_b)```. The Citizens object saves citizenship via an array 
    of the citizen's public keys.
    * allows its citizens to add and remove rule objects (the Rule class will be explained next) via 
    ```Citizens().add_rule(rule_1)``` and ```Citizens().remove_rule(rule_1)```
3. A Rule class that:
    * instantiates rule objects using a rule file contained in the ```./rules``` directory,
    * stores a cryptographic hash of the rule file so that any adjustment to the rule file will easy to spot,
    * allows citizens to vote via the ```Rule().vote(citizens, joey_b, vote_signature, vote)``` method. 
    For a citizen to be able to vote successfully, they **must**:
        * be a citizen of the ```citizens``` object passed to the ```vote``` method,
        * construct a ```valid vote_signature``` object using their private key and their ```vote```, a boolean.
 
## How it does it
TODO

## Authors

* **David Simmons** - [GitHub](https://github.com/desimmons), 
[Scholar](https://scholar.google.co.uk/citations?user=_O77iwwAAAAJ&hl=en)


## TODO list

* Create unit test examples.
* Create frontend Lemo website.
* Integrate homomorphic encryption into application.
* Create an identification platform

## Acknowledgments

* TODO