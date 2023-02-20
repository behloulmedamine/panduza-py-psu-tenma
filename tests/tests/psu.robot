*** Settings ***
Documentation       Test of the Power Supply API

Resource            ../rsc/fake_bench.resource

Suite Setup         Setup Bench Config


*** Test Cases ***

Basic tests
    Turn on power supply       psu_1
    Power Supply Should Be    psu_1    on
    Turn off power supply       psu_1
    Power Supply Should Be    psu_1    off
    Turn Power Supply    psu_1    on
    Power Supply Should Be    psu_1    on
    Turn Power Supply    psu_1    off
    Power Supply Should Be    psu_1    off
    Set Power Supply Voltage Goal    psu_1    3.3
    Set Power Supply Voltage Goal    psu_1    10
    Set Power Supply Current Goal    psu_1    2


