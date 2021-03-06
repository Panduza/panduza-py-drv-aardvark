Feature: Twi master/slave loopback
  Twi master must be able to communication with slave

  Scenario Outline: Test to loopback twi "<twi_master>" on twi "<twi_slave>"
    Given two twi interfaces "<twi_master>" and "<twi_slave>"
    When  data "<data>" is written on twi master "<twi_master>"
    Then  data "<data>" must be received by twi slave "<twi_slave>"

    Examples:
      | twi_master    | twi_slave         | data        |
      | twi_m1        | twi_s1            | tests       |


