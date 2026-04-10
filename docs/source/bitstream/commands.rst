Bitstream Commands
===================

CMD_PATH
---------
To be able to specify die to program it is required to properly forward JTAG to specific
direction and set mode accordingly. To program first die we use 0x10 value for this command
and it first one to be executed.

.. list-table::
   :widths: 10 40
   :header-rows: 1

   * - Bit
     - Description
   * - 0
     - Reset to default state
   * - 1
     - Set to path to top
   * - 2
     - Set to path to right
   * - 3
     - Enable forwarding mode
   * - 4
     - Enable programming mode

.. warning::
    This command have data after payload, and it consists of 9 bytes ``0x00 0x00 0x00 0x00 0x33 0x00 0x00 0x00 0x00`` and
    it is used to execute this JTAG command.


CMD_LXLYS
----------
Before sending any configuration data it is required to specify location of a specific TILE, and for latch configuration that configures all
logic and IO blocks it is this command.

.. list-table::
   :widths: 10 10 40
   :header-rows: 1

   * - Byte
     - Range
     - Description
   * - 0
     - 0..81
     - X location (column)
   * - 1
     - 0..65
     - Y location (row)

CMD_DLXP
---------
Alternate way of setting location for configuration data is by setting pattern for both column and row.

This commands sets row pattern and each bit represent one of the rows. There are total of 9 bytes used in payload.

CMD_DLYP
---------
This commands sets column pattern and each bit represent one of the columns. There are total of 11 bytes used in payload.

CMD_DLCU
---------
After location is set with one of previous commands, it is required to set a data payload.

For configuring logic and IO tiles data payload is 112 bytes max. Payload can be smaller, but programming
will act as it is zero padded till full size.
This command is also used to configure RAM blocks, there we expect 27 bytes of payload maximum. 

CMD_RXRYS
----------
Similar to **CMD_LXLYS** command, there is a command to specify RAM block to program.

.. list-table::
   :widths: 10 10 40
   :header-rows: 1

   * - Byte
     - Range
     - Description
   * - 0
     - 0..3
     - X location (column)
   * - 1
     - 0..7
     - Y location (row)

CMD_DRXP
---------
As alternative to **CMD_RXRYS** command we can use this one to specify a pattern, note that
each bit of one byte payload is used to set one of 4 columns.

CMD_CFGRST
-----------
Resets all configuration latches to value of a byte from payload, except active SPI controller and configuration PLL.

CMD_ACLCU
----------

Defines start address for following block memory init data.

.. list-table::
   :widths: 10 40
   :header-rows: 1

   * - Byte
     - Description
   * - 0
     - addr[ 7:0]
   * - 1
     - addr[15:8]

CMD_FRAM
---------

Payload contains up to 5120 bytes of RAM content. Start address must be previously defined by **CMD_ACLCU** command.
And RAM block must be selected with **CMD_RXRYS** or **CMD_DRXP** command.

CMD_PLL
--------

.. list-table::
   :widths: 10 40
   :header-rows: 1

   * - Byte
     - Description
   * - 0
     - PLL Config data 0
   * - 1
     - PLL Config data 1
   * - 2
     - PLL Config data 2
   * - 3
     - PLL Config data 3
   * - 4
     - PLL Config data 4
   * - 5
     - PLL Config data 5
   * - 6
     - PLL Config data 6
   * - 7
     - PLL Config data 7
   * - 8
     - PLL Config data 8
   * - 9
     - PLL Config data 9
   * - 10
     - PLL Config data 10
   * - 11
     - PLL Config data 11
   * - 12
     - Config data for clock matrix CLKIN PLL0
   * - 13
     - Config data for clock matrix CLKIN PLL1
   * - 14
     - Config data for clock matrix CLKIN PLL2
   * - 15
     - Config data for clock matrix CLKIN PLL3
   * - 16
     - Config data for clock matrix CLKMUX PLL0 byte 0
   * - 17
     - Config data for clock matrix CLKMUX PLL0 byte 1
   * - 18
     - Config data for clock matrix CLKMUX PLL1 byte 0
   * - 19
     - Config data for clock matrix CLKMUX PLL1 byte 1
   * - 20
     - Config data for clock matrix CLKMUX PLL2 byte 0
   * - 21
     - Config data for clock matrix CLKMUX PLL2 byte 1
   * - 22
     - Config data for clock matrix CLKMUX PLL3 byte 0
   * - 23
     - Config data for clock matrix CLKMUX PLL3 byte 1

.. warning::
    This command have data after payload, and it consists of 6 NOP bytes ``0x00 0x00 0x00 0x00 0x00 0x00``.

CMD_SPLL
---------

.. list-table::
   :widths: 10 40
   :header-rows: 1

   * - Bit
     - Description
   * - 0
     - Write config for PLL0
   * - 1
     - Write config for PLL1
   * - 2
     - Write config for PLL2
   * - 3
     - Write config for PLL2
   * - 4
     - Configuration set for PLL0
   * - 5
     - Configuration set for PLL1
   * - 6
     - Configuration set for PLL2
   * - 7
     - Configuration set for PLL3

There are two configuration sets, that could be set for each PLL.

.. warning::
    Value 0x00 is special case and it is used for writing to all 4 PLLs, same as 0x0F

CMD_WAIT_PLL
-------------

Wait for PLL lock.

.. list-table::
   :widths: 10 40
   :header-rows: 1

   * - Bit
     - Description
   * - 0
     - Wait for PLL0
   * - 1
     - Wait for PLL1
   * - 2
     - Wait for PLL2
   * - 3
     - Wait for PLL3

CMD_CHG_STATUS
---------------

.. list-table::
   :widths: 10 10 40
   :header-rows: 1

   * - Byte
     - Bit
     - Description
   * - 0
     - 0
     - Configuration done
   * - 
     - 1
     - Stop configuration
   * - 
     - 2
     - Reconfiguration enable
   * - 
     - 3
     - Enable CPE configuration
   * - 
     - 4
     - CPE reset
   * - 
     - 5
     - Fill RAM enable
   * -
     - 6
     - Enable SERDES regfile access from CPE
   * - 
     - 7
     - Unused
   * - 1
     - 0..3
     - Configuration mode
   * - 
     - 4
     - Select configuration mode
   * - 
     - 5..7
     - Unused
   * - 2
     - 0
     - Enable GPIO bank S1
   * - 
     - 1
     - Enable GPIO bank S2
   * - 
     - 2
     - Unused
   * - 
     - 3
     - Enable GPIO bank S3 (CFG)
   * - 
     - 4
     - Enable GPIO bank E1
   * - 
     - 5
     - Enable GPIO bank E2
   * - 
     - 6..7
     - Unused
   * - 3
     - 0
     - Enable GPIO bank N1
   * - 
     - 1
     - Enable GPIO bank N2
   * - 
     - 2..3
     - Unused
   * - 
     - 4
     - Enable GPIO bank W1
   * - 
     - 5
     - Enable GPIO bank W2
   * - 
     - 6..7
     - Unused
   * - 4
     - 0
     - PLL0 PLL_RST_N
   * - 
     - 1
     - PLL0 PLL_EN
   * - 
     - 2
     - PLL0 PLL_AUTN
   * - 
     - 3
     - PLL0 SET_SEL
   * - 
     - 4
     - PLL0 USR_SET
   * - 
     - 5
     - PLL0 USR_CLK_REF
   * - 
     - 6
     - PLL0 CLK_OUT_EN
   * - 
     - 7
     - PLL0 LOCK_REQ
   * - 5
     - 0..2
     - PLL0 AUTN_CT_I[2:0], should be 001
   * - 
     - 3
     - PLL0 CLK180_DOUB
   * - 
     - 4
     - PLL0 CLK270_DOUB
   * - 
     - 5..6
     - Unused
   * - 
     - 7
     - PLL0 USR_CLK_OUT
   * - 6
     - 0
     - PLL1 PLL_RST_N
   * - 
     - 1
     - PLL1 PLL_EN
   * - 
     - 2
     - Unused
   * - 
     - 3
     - PLL1 SET_SEL
   * - 
     - 4
     - PLL1 USR_SET
   * - 
     - 5
     - PLL1 USR_CLK_REF
   * - 
     - 6
     - PLL1 CLK_OUT_EN
   * - 
     - 7
     - PLL1 LOCK_REQ
   * - 7
     - 0..2
     - Unused
   * - 
     - 3
     - PLL1 CLK180_DOUB
   * - 
     - 4
     - PLL1 CLK270_DOUB
   * - 
     - 5..6
     - Unused
   * - 
     - 7
     - PLL1 USR_CLK_OUT
   * - 8
     - 0
     - PLL2 PLL_RST_N
   * - 
     - 1
     - PLL2 PLL_EN
   * - 
     - 2
     - Unused
   * - 
     - 3
     - PLL2 SET_SEL
   * - 
     - 4
     - PLL2 USR_SET
   * - 
     - 5
     - PLL2 USR_CLK_REF
   * - 
     - 6
     - PLL2 CLK_OUT_EN
   * - 
     - 9
     - PLL2 LOCK_REQ
   * - 7
     - 0..2
     - Unused
   * - 
     - 3
     - PLL2 CLK180_DOUB
   * - 
     - 4
     - PLL2 CLK270_DOUB
   * - 
     - 5..6
     - Unused
   * - 
     - 7
     - PLL2 USR_CLK_OUT
   * - 10
     - 0
     - PLL3 PLL_RST_N
   * - 
     - 1
     - PLL3 PLL_EN
   * - 
     - 2
     - Unused
   * - 
     - 3
     - PLL3 SET_SEL
   * - 
     - 4
     - PLL3 USR_SET
   * - 
     - 5
     - PLL3 USR_CLK_REF
   * - 
     - 6
     - PLL3 CLK_OUT_EN
   * - 
     - 9
     - PLL3 LOCK_REQ
   * - 11
     - 0..2
     - Unused
   * - 
     - 3
     - PLL3 CLK180_DOUB
   * - 
     - 4
     - PLL3 CLK270_DOUB
   * - 
     - 5..6
     - Unused
   * - 
     - 7
     - PLL3 USR_CLK_OUT

.. warning::
    This command have data after payload, and it consists of 9 bytes ``0x00 0x00 0x00 0x00 0x33 0x00 0x00 0x00 0x00`` and
    it is used to execute this JTAG command.


CMD_D2D
--------

.. list-table::
   :widths: 10 40
   :header-rows: 1

   * - Bit
     - Description
   * - 0
     - Enable D2D on north
   * - 1
     - Enable D2D on east
   * - 2
     - Enable D2D on south
   * - 3
     - Enable D2D on west


CMD_SERDES
-----------

CMD_JUMP
--------

Jump to address in SPI flash.

.. list-table::
   :widths: 10 40
   :header-rows: 1

   * - Byte
     - Description
   * - 0
     - addr[7:0]
   * - 1
     - addr[15:8]
   * - 2
     - addr[23:16]
   * - 3
     - addr[31:24]

.. warning::
    This command requires data after payload, and it consists of 2 NOP bytes ``0x00 0x00``.

CMD_CFGMODE
------------

.. list-table::
   :widths: 10 10 40
   :header-rows: 1

   * - Byte
     - Bit
     - Description
   * - 0
     - 
     - Number of CRC retries
   * - 1
     - 
     - CRC error behaviour (0: checked, 1: ignored, 2: unused)
   * - 2
     - 0..1
     - SPI bus IO width for `cmd` (0: single, 1: dual, 3: quad)
   * - 
     - 2..3
     - SPI bus IO width for `addr` (0: single, 1: dual, 3: quad)
   * - 
     - 4..5
     - SPI bus IO width for `mode` (0: single, 1: dual, 3: quad)
   * - 
     - 6..7
     - SPI bus IO width for `txdata` (0: single, 1: dual, 3: quad)
   * - 3
     - 0..1
     - SPI bus IO width for `rxdata` (0: single, 1: dual, 3: quad)
   * - 
     - 2..7
     - Number of dummy cycles between `addr` and `rxdata`
   * - 4
     - 
     - Flash `addr` field length
   * - 5
     - 
     - Flash `READ` command

.. warning::
    This command have data after payload, and it consists of 3 NOP bytes ``0x00 0x00 0x00``.

CMD_FLASH
----------

CMD_SLAVE_MODE
---------------

.. warning::
    This command have data after payload, and it consists of 3 NOP bytes ``0x00 0x00 0x00``.
