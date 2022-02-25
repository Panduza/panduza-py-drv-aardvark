# Panduza Python Drivers Aardvark

Panduza drivers for aardvark adapters (compatible with the Panduza Python Platform)

## Setup

```bash
# Dependencies
pip install aardvark-py
```

## Spi Master

To declare a spi master from an aardvark append the following inside you panduza tree

```json
"interfaces": [
    {
        "name": "my_spi_master",
        "driver": "aardvark_spi_master",
        "settings": {
            "serial_number": 2237170206,    // serial number of the aardvark you want to use for this interface
            "bitrate_hz": 4000000,
            "clock_polarity": 0,            // CPOL 0 or 1
            "clock_phase": 0,               // CPHA 0 or 1
            "bitorder": "msb",              // msb/lsb
            "ss_polarity": "active_low"     // active_low / active_high
        }
    }
]
```

## Spi Slave

```json
"interfaces": [
    {
        "name": "my_spi_slave",
        "driver": "aardvark_spi_slave",
        "settings": {
            "serial_number": 2238487174,
            "bitrate_hz": 4000000,
            "clock_polarity": 0,
            "clock_phase": 0,
            "bitorder": "msb"
            // "ss_polarity": "active_low" fixed for aardvark spi slaves 
        }
    }
]
```

