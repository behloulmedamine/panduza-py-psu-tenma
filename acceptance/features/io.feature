@action.platform_start.io_tree.json
Feature: API_IO

    Panduza provides a way to control simple input/output signals

    # -----------------------------------------------------------------------------
    # -----------------------------------------------------------------------------
    # -----------------------------------------------------------------------------
    Rule: API_IO must be comptabile with the discovery process

        Discovery requests are sent by the client on the topic *pza*.

        The driver must respond on its own topic {INTERFACE_PREFIX}/info.

        The payload exposed by the interface
        ```json
            {
                "type": "io", 
                "version": "1.0"
            }
        ```

        @fixture.client.test
        Scenario: Check scan information
            Given core aliases loaded with file "io_alias.json"
            Given a client "test" initialized with the mqtt test broker alias:"local_test"
            When  the client "test" start the connection
            And   the client "test" scan the interfaces
            Then  interface "pza/test_io/io_fake/io_in" contains information type == "io" and version == "1.0"

    # -----------------------------------------------------------------------------
    # -----------------------------------------------------------------------------
    # -----------------------------------------------------------------------------
    Rule: API_IO must be able to drive io direction

        Two topics are defined for this purpose:

        | Topic                                 | QOS | Retain |
        |:-------------------------------------:|:---:|:------:|
        | {INTERFACE_PREFIX}/atts/direction     | 0   | true   |
        | {INTERFACE_PREFIX}/cmds/direction/set | 0   | false  |

        The payload of those topics must be a json payload:

        | Key       | Type   | Description                       |
        |:-------- :|:------:|:---------------------------------:|
        | direction | string | direction of the io 'in' or 'out' |

        ```json
            {
                "direction": "in"
            }
        ```

        @fixture.interface.io.test
        Scenario: Io direction must be configurable
            Given core aliases loaded with file "io_alias.json"
            And  io interface "test" initialized with alias "io_test"
            When io interface "test" direction is set to "out"
            Then io interface "test" direction is "out"
            When io interface "test" direction is set to "in"
            Then io interface "test" direction is "in"

    # -----------------------------------------------------------------------------
    # -----------------------------------------------------------------------------
    # -----------------------------------------------------------------------------
    Rule: API_IO must be able to drive io value

        Two topics are defined for this purpose:

        | Topic                                 | QOS | Retain |
        |:-------------------------------------:|:---:|:------:|
        | {INTERFACE_PREFIX}/atts/value         | 0   | true   |
        | {INTERFACE_PREFIX}/cmds/value/set     | 0   | false  |

        The payload of those topics must be a json payload:

        | Key       | Type   | Description                       |
        |:-------- :|:------:|:---------------------------------:|
        | value     | number | value of the io                   |

        ```json
            {
                "value": 0
            }
        ```

        @fixture.interface.io.test
        Scenario: Io value must be configurable
            Given core aliases loaded with file "io_alias.json"
            And  io interface "test" initialized with alias "io_test"
            When io interface "test" direction is set to "out"
            Then io interface "test" direction is "out"
            When io interface "test" value is set to "0"
            Then io interface "test" value is "0"

        @fixture.interface.io.in
        @fixture.interface.io.out
        Scenario: Io value must support operation set and get through 2 interfaces in loopback
            Given core aliases loaded with file "io_alias.json"
            And  io interface "in" initialized with alias "io_in"
            And  io interface "out" initialized with alias "io_out"
            When io interface "in" direction is set to "in"
            And  io interface "out" direction is set to "out"
            When io interface "out" value is set to "1"
            Then io interface "in" value is "1"
            When io interface "out" value is set to "0"
            Then io interface "in" value is "0"

