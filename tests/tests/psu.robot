*** Settings ***
Documentation       Test of the Power Supply API

Resource            ../rsc/fake_bench.resource

Suite Setup         Setup Bench Config


*** Test Cases ***

Turn on and off the Power Supply
    Turn on power supply       psu_1    True
    Power Supply Should Be    psu_1    on


