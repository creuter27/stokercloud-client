import decimal
from enum import Enum


class NotConnectedException(Exception):
    pass


class PowerState(Enum):
    ON = 1
    OFF = 0


class Unit(Enum):
    KWH = 'kwh'
    PERCENT = '%'
    DEGREE = 'deg'
    KILO_GRAM = 'kg'
    GRAM = 'g'
    CM = 'cm'
    MPS = 'm/s'


class State(Enum):
    POWER = 'state_5'
    HOT_WATER = 'state_7'
    IGNITION_1 = 'state_2'
    IGNITION_2 = 'state_4'
    FAULT_IGNITION = 'state_13'
    STOPPED_EXTCONTACT = 'state_24'
    COMPRESSOR_CLEANING = 'state_43'
    OFF = 'state_14'


STATE_BY_VALUE = {key.value: key for key in State}


class Value:
    def __init__(self, value, unit):
        self.value = decimal.Decimal(value)
        self.unit = unit

    def __eq__(self, other):
        if not isinstance(other, Value):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.value == other.value and self.unit == other.unit

    def __repr__(self):
        return "%s %s" % (self.value, self.unit)

def get_from_list_by_key(lst, key, value):
    for itm in lst:
        if itm.get(key) == value:
            return itm

class ControllerData:
    def __init__(self, data):
        if data['notconnected'] != 0:
            raise NotConnectedException("Furnace/boiler not connected to StokerCloud")
        self.data = data

    def get_sub_item(self, submenu, _id):
        return get_from_list_by_key(self.data[submenu], 'id', _id)

    @property
    def alarm(self):
        return {
            0: PowerState.OFF,
            1: PowerState.ON
        }.get(self.data['miscdata'].get('alarm'))

    @property
    def running(self):
        return {
            0: PowerState.OFF,
            1: PowerState.ON
        }.get(self.data['miscdata'].get('running'))

    @property
    def serial_number(self):
        return self.data['serial']

    @property
    def boiler_temperature_current(self):
        return Value(self.get_sub_item('frontdata', 'boilertemp')['value'], Unit.DEGREE)

    @property
    def boiler_temperature_requested(self):
        return Value(self.get_sub_item('frontdata', '-wantedboilertemp')['value'], Unit.DEGREE)

    @property
    def boiler_return_temperature(self):
        return Value(self.get_sub_item('boilerdata', '17')['value'], Unit.DEGREE)

    @property
    def exhaust_temmperature(self):
        return Value(self.get_sub_item('boilerdata', '3')['value'], Unit.DEGREE)

    @property
    def o2_percent(self):
        return Value(self.get_sub_item('boilerdata', '12')['value'], Unit.PERCENT)

    @property
    def time_online_percent_percent(self):
        return Value(self.get_sub_item('boilerdata', '9')['value'], Unit.PERCENT)

    @property
    def boiler_kwh(self):
        return Value(self.get_sub_item('boilerdata', '5')['value'], Unit.KWH)

    @property
    def outside_temp(self):
        return Value(self.get_sub_item('weatherdata', '1')['value'], Unit.DEGREE)

    @property
    def wind_speed(self):
        return Value(self.get_sub_item('weatherdata', '2')['value'], Unit.MPS)

    @property
    def wind_direction(self):
        return Value(self.get_sub_item('weatherdata', '3')['value'])

    @property
    def humidity(self):
        return Value(self.get_sub_item('weatherdata', '9')['value'], Unit.PERCENT)

    @property
    def state(self):
        return STATE_BY_VALUE.get(self.data['miscdata']['state']['value'])

    @property
    def hotwater_temperature_current(self):
        return Value(self.get_sub_item('frontdata', 'dhw')['value'], Unit.DEGREE)

    @property
    def hotwater_temperature_requested(self):
        return Value(self.get_sub_item('frontdata', 'dhwwanted')['value'], Unit.DEGREE)

    @property
    def consumption_total(self):
        return Value(self.get_sub_item('hopperdata', '4')['value'], Unit.KILO_GRAM)
    
    @property
    def consumption_day(self):
        return Value(self.get_sub_item('hopperdata', '3')['value'], Unit.KILO_GRAM)

    @property
    def output_percentage(self):
        return Value(self.data['miscdata']['outputpct'], Unit.PERCENT)

    @property
    def boiler_photosensor(self):
        return Value(self.get_sub_item('boilerdata', '6')['value'], Unit.PERCENT)

    @property
    def hopper_capacity(self):
        return Value(self.data['miscdata'].get('hopperdistance'), Unit.CM)

    @property
    def hopper_content(self):
        return Value(self.data['frontdata'].get('hoppercontent'), Unit.KILO_GRAM)

    @property
    def hopper_max_distance(self):
        return Value(self.data['miscdata'].get('hopper.distance_max'), Unit.CM)   

    @property
    def auger_moved_mass(self):
        return Value(self.get_sub_item('hopperdata', '2')['value'], Unit.GRAM)

    @property
    def consumption_total(self):
        return Value(self.get_sub_item('hopperdata', '4')['value'], Unit.KILO_GRAM)
    
    @property
    def power_10_percent(self):
        return Value(self.get_sub_item('hopperdata', '7')['value'], Unit.KWH)
    
    @property
    def power_100_percent(self):
        return Value(self.get_sub_item('hopperdata', '8')['value'], Unit.KWH)
    
    @property
    def consumption_day(self):
        return Value(self.get_sub_item('hopperdata', '3')['value'], Unit.KILO_GRAM)
    
    @property
    def dhw_on(self):
        return Value(self.data['leftoutput']['output-1']['val'], Unit(self.data['leftoutput']['output-1']['unit']))

    @property
    def dwh_pump(self):
        return Value(self.data['leftoutput']['output-2']['val'], Unit(self.data['leftoutput']['output-2']['unit']))

    @property
    def weathervalve(self):
        return Value(self.data['leftoutput']['output-3']['val'], Unit(self.data['leftoutput']['output-3']['unit']))

    @property
    def weatherpump(self):
        return Value(self.data['leftoutput']['output-4']['val'], Unit(self.data['leftoutput']['output-4']['unit']))

    @property
    def exhaustfan(self):
        return Value(self.data['leftoutput']['output-5']['val'], Unit(self.data['leftoutput']['output-5']['unit']))

    @property
    def ashauger(self):
        return Value(self.data['leftoutput']['output-6']['val'], Unit(self.data['leftoutput']['output-6']['unit']))

    @property
    def compressor_percent(self):
        return Value(self.data['leftoutput']['output-7']['val'], Unit(self.data['leftoutput']['output-7']['unit']))

    @property
    def weathervalve2(self):
        return Value(self.data['leftoutput']['output-8']['val'], Unit(self.data['leftoutput']['output-8']['unit']))

    @property
    def weatherpump2(self):
        return Value(self.data['leftoutput']['output-9']['val'], Unit(self.data['leftoutput']['output-9']['unit']))
