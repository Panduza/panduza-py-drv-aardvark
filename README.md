# Panduza Python Drivers Aardvark

Panduza drivers for aardvark adapters (compatible with the Panduza Python Platform)

## Spi Master

To declare a spi master from an aardvark append the following inside you panduza tree

```json
"interfaces": [
    {
        "name": "my_spi_master",
        "driver": "aardvark_spi_master",
        "params": {
            "serial_number": 2237171234     // serial number of the aardvark you want to use for this interface
        }
    }
]
```

## Spi Slave
