*** Settings ***

Library      panduza.robof.Keywords
Variables    envs/fake_bench.py


*** Keywords ***

Setup Bench Config
    Load Pza Interfaces From Aliases    ${pza_aliases}
