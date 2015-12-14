Draftpy  [![Build Status](https://travis-ci.org/spudfkc/draftpy.svg?branch=master)](https://travis-ci.org/spudfkc/draftpy)
=======

How to use
----------
  1. `pip install -r requirements.txt`
  2. `python cli.py DKSalaries.csv`
  The following environment variables are supported:
    `NGEN: number of generations. each generation is a potential lineup`
    `MIN_PLAYER_POINTS: minimum points a player must be valued at to be considered in a lineup`

Note:
Due to the randomness of the generator, sometimes you might run this and not have any valid lineups generated.



TODO
--------
  - add logic for double-double and triple-double to strategies
  - learn more cool things about pandas
  - tests
  - account for injuries
