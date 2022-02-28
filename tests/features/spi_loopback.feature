Feature: Spi master/slave loopback
  Spi master must be able to communication with slave

  Scenario Outline: Test to loopback "<spi_master>" on "<spi_slave>"
    Given two interfaces "<spi_master>" and "<spi_slave>"
    When  data "<data>" is emitted on "<spi_master>"
    Then  data "<data>" must be received on "<spi_slave>"

    Examples:
      | spi_master    | spi_slave         | data        |
      | spi_m1        | spi_s1            | tests       |


