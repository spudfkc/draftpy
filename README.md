Draftpy[![Build Status](https://travis-ci.org/spudfkc/draftpy.svg?branch=master)](https://travis-ci.org/spudfkc/draftpy)
=======

How to use
----------
  1. `pip install -r requirements.txt`
  2. `python draftpy/draftpy.py <away@home> <away@home> ...`
    The <away@home> should be a team's three letter abbreviation (case-insensitive).
    You can list all the team abbreviations with the following command:
        `python -c 'import nba_py.team; print [i for i in nba_py.team.TEAMS]'`


TODO
--------
  - add logic for double-double and triple-double
  - incorporate salary
  - actually generate lineups
  - learn more cool things about pandas
  - probably make a base strategy class that includes common logic/attributes
  - look into cacheing since stats.nba.com takes forever
  - tests
  - move CLI logic into own module
