import logging


def decode_mf(b1, b2):
        h = b2 + b1
        name = \
            chr(((int(h, 16) & 0xFC00)//1024)+64) + \
            chr(((int(h, 16) & 0x3E0)//32)+64) + \
            chr(((int(h, 16) & 0x1F)+64))
        return name


def decode_medium(m):
    list_of_mediums = ['Other', 'Oil', 'Electricity', 'Gas',
                       'Heat (Outlet)', 'Steam', 'Hot Water', 'Water',
                       'Heat Cost Allocator', 'Compressed Air',
                       'Cooling Load Meter (Outlet)', 'Cooling Load Meter (Inlet)',
                       'Heat (Inlet)', 'Heat / Cooling Load Meter',
                       'Bus / System', 'Unknown Medium', 'Reserved',
                       'Reserved', 'Reserved', 'Reserved', 'Reserved',
                       'Reserved', 'Cold Water', 'Dual Water',
                       'Pressure', 'A/D Converter', 'Reserved']
    n = int(m, 16)
    if n >= 32:
        return 'Reserved'
    else:
        return list_of_mediums[n]


def decode_lvar(first_byte):
    # Variable Length: With data field = `1101b` several data types with variable length can be used.
    # The length of the data is given after the DRH with the first byte of real data,
    # which is here called LVAR (e.g. LVAR = 02h: ASCII string with two characters follows) ♣.
    lvar = int(first_byte, 16)
    if lvar < 0:
        logging.error('LVAR less than zero!')
        exit(1)
    elif lvar < 192:  # 00h..BFh : ASCII string with LVAR characters
        return 'ASCII', lvar
    elif lvar < 208:  # C0h..CFh : positive BCD number with (LVAR - C0h) • 2 digits
        return 'BCD', (lvar-192)
    elif lvar < 224:  # D0h..DFH : negative BCD number with (LVAR - D0h) • 2 digits
        return 'BCD', (lvar-208)
    elif lvar < 240:  # E0h..EFh : binary number with (LVAR - E0h) bytes
        return 'Binary Number', (lvar-224)
    elif lvar < 251:  # F0h..FAh : float with (LVAR  - F0h) bytes [to be defined]
        return 'Floating Point Number', (lvar-240)
    elif lvar < 255:  # Reserved
        return 'Reserved', lvar
    else:
        logging.error('WEIRD LVAR!')
        exit(1)


def decode_dif(dif):
    dif = int(dif, 16)
    # Shows if there's a DIFE following this DIF.
    extension_bit = (dif & 0x80) != 0
    # Least significant bit of storage number. 0: Actual value, 1: historic value. Higher numbers requires DIFE.
    lsb_of_storage = (dif & 0x40) >> 6
    # The function field gives the type of data as follows.
    function_field = (dif & 0x30) >> 4
    function_codes = ['Instantaneous value', 'Maximum value', 'Minimum value', 'Value during error state']
    # The data field shows how the data from the master must be interpreted in respect of length
    # and coding. The following table contains the possible coding of the data field:
    data_field = (dif & 0x0F)
    data_codes = ['No data', '8bit Integer', '16bit Integer', '24bit Integer',
                  '32bit Integer', '32bit Real', '48bit Integer', '64bit Integer',
                  'Selection for Readout', '2 digit BCD', '4 digit BCD', '6 digit BCD',
                  '8 digit BCD', 'Variable length', '12 digit BCD', 'Special functions']
    data_length = [0, 1, 2, 3, 4, 4, 6, 8, 0, 1, 2, 3, 4, 1, 6, 0]

    return extension_bit, lsb_of_storage, function_codes[function_field], \
        data_codes[data_field], data_length[data_field]


def decode_dife(dife):
    dife = int(dife, 16)
    # Shows if there's another DIFE following this one.
    extension_bit = (dife & 0x80) != 0
    # Next most significant bit of the device subunit, from least to most, I think.
    subunit = (dife & 0x40) >> 6
    # Tariff code..?
    tariff = (dife & 0x30) >> 4
    # Next most significant bit of the storage number, from least to most, I think.
    storage_bits = (dife & 0x0F)

    return extension_bit, subunit, tariff, storage_bits


def decode_vif(vif):
    vif = int(vif, 16)
    extension_bit = (vif & 0x80) != 0
    code = (vif & 0x7F) >> 3
    nnn = vif & 0b00000111
    nn = nnn & 0b011
    if code == 0:
        quantity = pow(10, (nnn-3))
        description = 'Energy'
        si_unit = '{}Wh'.format(quantity)
    elif code == 1:
        quantity = pow(10, (nnn-3))
        description = 'Energy'
        si_unit = '{}kJ'.format(quantity)
    elif code == 2:
        quantity = pow(10, (nnn-3))
        description = 'Volume'
        si_unit = '{}L'.format(quantity)
    elif code == 3:
        quantity = pow(10, (nnn-3))
        description = 'Mass'
        si_unit = '{}kg'.format(quantity)
    elif code == 4:
        t = ['seconds', 'minutes', 'hours', 'days']
        si_unit = t[nn]
        if nnn < 4:
            description = 'On Time'
        else:
            description = 'Operating Time'
    elif code == 5:
        quantity = pow(10, (nnn-3))
        description = 'Power'
        si_unit = '{}W'.format(quantity)
    elif code == 6:
        quantity = pow(10, (nnn-3))
        description = 'Power'
        si_unit = '{}kJ/h'.format(quantity)
    elif code == 7:
        quantity = pow(10, (nnn-3))
        description = 'Volume Flow'
        si_unit = '{}L/h'.format(quantity)
    elif code == 8:
        quantity = pow(10, (nnn-4))
        description = 'Volume Flow Ext.'
        si_unit = '{}L/min'.format(quantity)
    elif code == 9:
        quantity = pow(10, (nnn-6))
        description = 'Volume Flow Ext.'
        si_unit = '{}L/s'.format(quantity)
    elif code == 10:
        quantity = pow(10, (nnn-3))
        description = 'Mass Flow'
        si_unit = '{}kg/h'.format(quantity)
    elif code == 11:
        if nnn < 4:
            description = 'Flow Temperature'
        else:
            description = 'Return Temperature'
        quantity = pow(10, (nn-3))
        si_unit = '{}C'.format(quantity)
    elif code == 12:
        quantity = pow(10, (nn-3))
        if nnn < 4:
            description = 'Temperature Difference'
            si_unit = '{}K'.format(quantity)
        else:
            description = 'External Temperature'
            si_unit = '{}C'.format(quantity)
    elif code == 13:
        if nnn < 4:
            quantity = pow(10, (nn-3))
            si_unit = '{}bar'.format(quantity)
            description = 'Pressure'
        elif nnn < 6:
            description = 'Time Point'
            if nnn == 4:
                si_unit = 'Date, coded as type G. See MBus Documentation 8.2'
            else:
                si_unit = 'Time & Date, coded as type F. See MBus Documentation 8.2'
        elif nnn == 6:
            description = 'Units for H.C.A.'
            si_unit = 'dimensionless'
        else:
            description = 'Reserved'
            si_unit = 'RESERVED ERROR!'
    elif code == 14:
        t = ['seconds', 'minutes', 'hours', 'days']
        si_unit = t[nn]
        if nnn < 4:
            description = 'Averaging Duration'
        else:
            description = 'Actuality duration'
    elif code == 15:
        si_unit = ''
        if nnn == 0:
            description = 'Fabrication Number'
        elif nnn == 1:
            description = '(Enhanced, see 6.4.2)'
        elif nnn == 2:
            description = 'Bus Address'
        elif nnn == 3:
            description = 'EXT_B - Extension of VIF-codes - 8.4.4b, true VIF is given in the first VIFE'
        elif nnn == 4:
            description = 'STR - VIF in the following string'
        elif nnn == 5:
            description = 'EXT_A - Extension of VIF-codes - 8.4.4a, true VIF is given in the first VIFE'
        elif nnn == 6:
            description = 'Any VIF, used for readout selection of all VIFs'
        elif nnn == 7:
            description = 'Manufacturer specific'
        else:
            description = 'UNDEFINED'
    else:
        quantity = pow(10, (nnn-3))
        description = 'Magic Dust (Unknown Code)'
        si_unit = '{}X'.format(quantity)

    return extension_bit, description, si_unit


def decode_vife(vife):
    vife = int(vife, 16)
    extension_bit = (vife & 0x80) != 0
    si_unit = ''
    code = (vife & 0x7F)
    if code == 32:
        description = 'per second'
    elif code == 33:
        description = 'per minute'
    elif code == 34:
        description = 'per hour'
    elif code == 35:
        description = 'per day'
    elif code == 36:
        description = 'per week'
    elif code == 37:
        description = 'per month'
    elif code == 38:
        description = 'per year'
    elif code == 39:
        description = 'per revolution/measurement'
    elif code == 40:
        description = 'increment per input pulse on input channel 0'
    elif code == 41:
        description = 'increment per input pulse on input channel 1'
    elif code == 42:
        description = 'increment per output pulse on output channel 0'
    elif code == 43:
        description = 'increment per output pulse on output channel 1'
    elif code == 44:
        description = 'per liter'
    elif code == 45:
        description = 'per m^3'
    elif code == 46:
        description = 'per kg'
    elif code == 47:
        description = 'per K'
    elif code == 48:
        description = 'per KWh'
    elif code == 49:
        description = 'per GJ'
    elif code == 50:
        description = 'per kW'
    elif code == 51:
        description = 'per (Kelvin*liter)'
    elif code == 52:
        description = 'per V'
    elif code == 53:
        description = 'per A'
    elif code == 54:
        description = 'multiplied by sek'
    elif code == 55:
        description = 'multiplied by sek/V'
    elif code == 56:
        description = 'multiplied by sek/A'
    elif code == 57:
        description = 'start date(/time) of '
    elif code == 58:
        description = 'VIF contains uncorrected unit instead of corrected unit'
    elif code == 59:
        description = 'Accumulation only if positive contributions'
    elif code == 60:
        description = 'Accumulation of abs value only if negative contributions'
    else:
        description = ''

    return extension_bit, description, si_unit


def decode_vife_a(vife):
    vife = int(vife, 16)
    extension_bit = (vife & 0x80) != 0
    code = (vife & 0x7F)
    nnnn = vife & 0b00001111    # Could write 15, but this is more visual :)
    nnn = nnnn & 0b0111         # 7
    nn = nnn & 0b011            # 3
    si_unit = ''
    if code < 4:
        quantity = pow(10, (nn-3))
        description = 'Credit of {} of the nominal local legal currency units'.format(quantity)
    elif code < 8:
        quantity = pow(10, (nn-3))
        description = 'Debit of {} of the nominal local legal currency units'.format(quantity)
    elif code == 8:
        description = 'Access Number (transmission count)'
    elif code == 9:
        description = 'Medium (as in fixed header)'
    elif code == 10:
        description = 'Manufacturer (as in fixed header)'
    elif code == 11:
        description = 'Parameter set identification'
    elif code == 12:
        description = 'Model / Version'
    elif code == 13:
        description = 'Hardware version #'
    elif code == 14:
        description = 'Firmware version #'
    elif code == 15:
        description = 'Software version #'
    elif code == 16:
        description = 'Customer location'
    elif code == 17:
        description = 'Customer'
    elif code == 18:
        description = 'Access Code User'
    elif code == 19:
        description = 'Access Code Operator'
    elif code == 20:
        description = 'Access Code System Operator'
    elif code == 21:
        description = 'Access Code Developer'
    elif code == 22:
        description = 'Password'
    elif code == 23:
        description = 'Error flags (binary)'
    elif code == 24:
        description = 'Error mask'
    elif code == 25:
        description = 'Reserved'
    elif code == 26:
        description = 'Digital Output (binary)'
    elif code == 27:
        description = 'Digital Input (binary)'
    elif code == 28:
        description = 'Baudrate [Baud]'
    elif code == 29:
        description = 'response delay time [bittimes]'
    elif code == 30:
        description = 'Retry'
    elif code == 31:
        description = 'Reserved'
    elif code == 32:
        description = 'First storage # for cyclic storage'
    elif code == 33:
        description = 'Last storage # for cyclic storage'
    elif code == 34:
        description = 'Size of storage block'
    elif code == 35:
        description = 'Reserved'
    elif code == 36:
        description = 'Storage interval [secs]'
    elif code == 37:
        description = 'Storage interval [minutes]'
    elif code == 38:
        description = 'Storage interval [hours]'
    elif code == 39:
        description = 'Storage interval [days]'
    elif code == 40:
        description = 'Storage interval month(s)'
    elif code == 41:
        description = 'Storage interval year(s)'
    elif code == 42:
        description = 'Reserved'
    elif code == 43:
        description = 'Reserved'
    elif code == 44:
        description = 'Duration since last readout [secs]'
    elif code == 45:
        description = 'Duration since last readout [minutes]'
    elif code == 46:
        description = 'Duration since last readout [hours]'
    elif code == 47:
        description = 'Duration since last readout [days]'
    elif code == 48:
        description = 'Start (date/time) of tariff'
    elif code == 49:
        description = 'Duration of tariff (minutes)'
    elif code == 50:
        description = 'Duration of tariff (hours)'
    elif code == 51:
        description = 'Duration of tariff (days)'
    elif code == 52:
        description = 'Period of tariff [secs]'
    elif code == 53:
        description = 'Period of tariff [minutes]'
    elif code == 54:
        description = 'Period of tariff [hours]'
    elif code == 55:
        description = 'Period of tariff [days]'
    elif code == 56:
        description = 'Period of tariff months(s)'
    elif code == 57:
        description = 'Period of tariff year(s)'
    elif code == 58:
        description = 'dimensionless / no VIF'
    elif code == 59:
        description = 'Reserved'
    elif code == 60:
        description = 'Reserved'
    elif code == 61:
        description = 'Reserved'
    elif code == 62:
        description = 'Reserved'
    elif code == 63:
        description = 'Reserved'
    elif code < 80:
        quantity = pow(10, (nnnn-9))
        description = '{} Volts'.format(quantity)
    elif code < 96:
        quantity = pow(10, (nnnn-12))
        description = '{} Ampere'.format(quantity)
    elif code == 96:
        description = 'Reset Counter'
    elif code == 97:
        description = 'Cumulation counter'
    elif code == 98:
        description = 'Control signal'
    elif code == 99:
        description = 'Day of week'
    elif code == 100:
        description = 'Week number'
    elif code == 101:
        description = 'Time point of day change'
    elif code == 102:
        description = 'State of parameter activation'
    elif code == 103:
        description = 'Special supplier information'
    elif code == 104:
        description = 'Duration since last cumulation [hours]'
    elif code == 105:
        description = 'Duration since last cumulation [days]'
    elif code == 106:
        description = 'Duration since last cumulation [months]'
    elif code == 107:
        description = 'Duration since last cumulation [years]'
    elif code == 108:
        description = 'Operating time battery[hours]'
    elif code == 109:
        description = 'Operating time battery[days]'
    elif code == 110:
        description = 'Operating time battery[months]'
    elif code == 111:
        description = 'Operating time battery[years]'
    elif code == 112:
        description = 'Date and time of battery change'
    else:
        description = 'Reserved'

    return extension_bit, description, si_unit


def decode_vife_b(vife):
    vife = int(vife, 16)
    extension_bit = (vife & 0x80) != 0
    code = (vife & 0x7F)
    code2 = code >> 2   # the VIF without the last two bits
    nnn = vife & 0b00000111
    nn = nnn & 0b011
    n = nn & 0b1
    si_unit = ''

    if code == 0 or code == 1:
        quantity = pow(10, (n-1))
        description = 'Energy'
        si_unit = '{}MWh'.format(quantity)
    elif code == 8 or code == 9:
        quantity = pow(10, (n-1))
        description = 'Energy'
        si_unit = '{}GJ'.format(quantity)
    elif code == 16 or code == 17:
        quantity = pow(10, (n+2))
        description = 'Volume'
        si_unit = '{}m^3'.format(quantity)
    elif code == 24 or code == 25:
        quantity = pow(10, (n+2))
        description = 'Mass'
        si_unit = '{}t'.format(quantity)
    elif code == 33:
        description = 'Volume'
        si_unit = '0,1 feet^3'
    elif code == 34:
        description = 'Volume'
        si_unit = '0,1 american gallon'
    elif code == 35:
        description = 'Volume'
        si_unit = '1 american gallon'
    elif code == 36:
        description = 'Volume flow'
        si_unit = '0,001 american gallon/min'
    elif code == 37:
        description = 'Volume flow'
        si_unit = '1 american gallon/min'
    elif code == 38:
        description = 'Volume flow'
        si_unit = '1 american gallon/h'
    elif code == 40 or code == 41:
        quantity = pow(10, (n-1))
        description = 'Power'
        si_unit = '{}MW'.format(quantity)
    elif code == 48 or code == 49:
        quantity = pow(10, (n-1))
        description = 'Power'
        si_unit = '{}GJ/h'.format(quantity)
    elif code2 == 22:
        quantity = pow(10, (nn-3))
        description = 'Flow Temperature'
        si_unit = '{}°F'.format(quantity)
    elif code2 == 23:
        quantity = pow(10, (nn-3))
        description = 'Return Temperature'
        si_unit = '{}°F'.format(quantity)
    elif code2 == 24:
        quantity = pow(10, (nn-3))
        description = 'Temperature difference'
        si_unit = '{}°F'.format(quantity)
    elif code2 == 25:
        quantity = pow(10, (nn-3))
        description = 'External Temperature'
        si_unit = '{}°F'.format(quantity)
    elif code2 == 28:
        quantity = pow(10, (nn-3))
        description = 'Cold/Warm Temperature Limit'
        si_unit = '{}°F'.format(quantity)
    elif code2 == 29:
        quantity = pow(10, (nn-3))
        description = 'Cold/Warm Temperature Limit'
        si_unit = '{}°C'.format(quantity)
    elif code2 == 30:
        quantity = pow(10, (nnn-3))
        description = 'cumul. count max power'
        si_unit = '{}W'.format(quantity)
    else:
        description = 'Reserved'

    return extension_bit, description, si_unit
