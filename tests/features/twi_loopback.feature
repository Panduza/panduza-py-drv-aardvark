Feature: Twi master/slave loopback
  Twi master must be able to communication with slave

  Scenario Outline: Test to loopback twi "<twi_master>" on twi "<twi_slave>"
    Given two twi interfaces "<twi_master>" and "<twi_slave>"
    # When  data "<data>" is emitted on twi "<twi_master>"
    # Then  data "<data>" must be received on twi "<twi_slave>"
    # When  data "<data>" is configured as response on twi "<twi_slave>"
    # Then  data "<data>" must be received by twi "<twi_master>" when it requests a transfer

    Examples:
      | twi_master    | twi_slave         | data        |
      | twi_m1        | twi_s1            | tests       |

