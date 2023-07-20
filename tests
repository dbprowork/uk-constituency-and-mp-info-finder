import requests
import json
import sys
import pytest
from project import Constituency
from project import MP
from project import c_input_check
from project import c_out
from project import m_out


def main():
    test_c_init()
    test_c_out()
    test_c_input_check()
    test_m_init()
    test_m_out()


def test_c_init():
    test_c_o = Constituency("tottenham")
    assert test_c_o.options[0] == "Tottenham"

    test_c_o = Constituency("tot")
    assert test_c_o.options[1] == "Tottenham"


def test_c_out():
    test_c_o = Constituency("tottenham")
    test_c_o.ind = 0
    test_c_o.c_prep()
    assert c_out(test_c_o, "1") == "The constituency ID for Tottenham is 3811."
    assert c_out(test_c_o, "2") == "The MP for Tottenham is Mr David Lammy."
    assert c_out(test_c_o, "3") == "Tottenham is held by Labour."
    assert c_out(test_c_o, "a") == "Choice must be a number."
    assert c_out(test_c_o, "5") == "Option not available."


def test_c_input_check():
    test_c_o = Constituency("1")
    with pytest.raises(SystemExit, match="Search cannot include numbers or special characters. Restart to try again."):
        c_input_check(test_c_o)

    test_c_o = Constituency("testnone")
    with pytest.raises(SystemExit, match=f"{test_c_o.search.title()} not recognised. Restart to try again."):
        c_input_check(test_c_o)


def test_m_init():
    test_c_o = Constituency("tottenham")
    test_c_o.ind = 0
    test_c_o.c_prep()
    test_mp_o = MP(test_c_o.mp, test_c_o.mp_id)
    test_mp_o.m_prep()
    assert test_mp_o.mp_name == "Mr David Lammy"
    assert test_mp_o.mp_contact.rstrip() == "david.lammy.mp@parliament.uk"


def test_m_out():
    test_c_o = Constituency("tottenham")
    test_c_o.ind = 0
    test_c_o.c_prep()
    test_mp_o = MP(test_c_o.mp, test_c_o.mp_id)
    test_mp_o.m_prep()


    assert m_out(test_mp_o, "1") == "The email address for Mr David Lammy is david.lammy.mp@parliament.uk."
    assert m_out(test_mp_o, "2") ==  [["Africa, Caribbean, Latin America, USA"], ["Health, Treasury (regeneration), arts and culture, education, international development"]]
    assert m_out(test_mp_o, "3") == "The last election result for Mr David Lammy was Lab Hold."
    assert m_out(test_c_o, "a") == "Choice must be a number."
    assert m_out(test_c_o, "5") == "Option not available."


if __name__ == "__main__":
    main()
