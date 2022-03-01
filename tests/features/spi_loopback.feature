Feature: Spi master/slave loopback
  Spi master must be able to communication with slave

  Scenario Outline: Test to loopback spi "<spi_master>" on spi "<spi_slave>"
    Given two spi interfaces "<spi_master>" and "<spi_slave>"
    When  data "<data>" is emitted on spi "<spi_master>"
    Then  data "<data>" must be received on spi "<spi_slave>"
    When  data "<data>" is configured as response on spi "<spi_slave>"
    Then  data "<data>" must be received by spi "<spi_master>" when it requests a transfer

    Examples:
      | spi_master    | spi_slave         | data        |
      | spi_m1        | spi_s1            | tests       |


