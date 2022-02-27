Feature: Spi master/slave loopback
  Spi master must be able to communication with slave

  Scenario Outline: Test to loopback "<pin_o>" on "<pin_i>"
    Given the panduza server is up
    And   the "<pin_o>" is set as output
    And   the "<pin_i>" is set as input
    When  the "<pin_o>" is writen to 1
    Then  the "<pin_i>" is read to 1
    When  the "<pin_o>" is writen to 0
    Then  the "<pin_i>" is read to 0

    Examples:
      | pin_o       | pin_i         |
      | io_1        | io_2          |
      | io_2        | io_1          |

