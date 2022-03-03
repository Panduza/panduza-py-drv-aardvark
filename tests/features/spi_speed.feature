# Feature: Spi master read speed measurement
#   Spi master read speed must be measured

#   Scenario Outline: Measure time to read "<nb_bytes>" bytes "<nb_times>" times
#     Given two spi interfaces "<spi_master>" and "<spi_slave>"
#     And   spi slave "<spi_master>"
#     When  data "<data>" is emitted on spi "<spi_master>"
#     Then  data "<data>" must be received on spi "<spi_slave>"
#     When  data "<data>" is configured as response on spi "<spi_slave>"
#     Then  data "<data>" must be received by spi "<spi_master>" when it requests a transfer

#     Examples:
#       | spi_master    | spi_slave         | data        |
#       | spi_m1        | spi_s1            | tests       |


