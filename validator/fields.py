# encoding=utf-8

from collections import OrderedDict

FORMATTED_TYPE_NAMES = {
    'str':   'String',
    'int':   'Integer',
    'list':  'List',
    'float': 'Float',
    'dict':  'Dictionary'
}


class DeclarativeFieldsMetaclass(type):
    """
    Metaclass for removing declared Fields from Validator instances.
    """

    def __new__(mcs, name, bases, attrs):
        """
        Remove declared Fields as object attributes

        Notes:
            This is necessary to allow a declarative interface for inherited
            Validation objects. We then reset the attrs to be the value from
            the incoming dictionary in the BaseValidator class, similar to how
            it's done in Django with Models.

        """
        declared_fields = []
        # required_fields = []

        for key, val in list(attrs.items()):
            if isinstance(val, Field):
                # if val.required:
                #     required_fields.append((key, val))
                declared_fields.append((key, val))
                attrs.pop(key)

        # Attach collected lists to attrs before object creation.
        attrs['_fields'] = OrderedDict(declared_fields)
        # attrs['_required_fields'] = OrderedDict(required_fields)

        new_class = super(DeclarativeFieldsMetaclass, mcs).__new__(mcs, name, bases, attrs)
        return new_class


class Field:
    """ Validation Field. """

    def __init__(self, data_type=None, validators=None, required=False, default=None):
        if data_type == str:
            data_type = [str, unicode]  # support unicode
        self.data_type = data_type
        self.validators = validators or []
        self.required = required
        self.default = default

    def validate_type(self, val):
        """ Validates field data type

        :param val: Value passed for checking
        :type val: Any

        :return: error message if any
        """
        err = None

        # A single valid data type
        if (type(self.data_type) != list) and (type(val) != self.data_type):
            err = "'{}' is expected to be a '{}'".format(val, self.formated_data_type(self.data_type))

        # Multiple valid types are passed as a list
        elif (type(self.data_type) == list) and (type(val) not in self.data_type):
           error_msg = " or ".join([self.formated_data_type(t) for t in self.data_type])
           err = "'{}' is expected to be a '{}'".format(val, error_msg)

        return err

    def formated_data_type(self, data_type):
        """Format data type name"""
        if data_type in FORMATTED_TYPE_NAMES:
            return FORMATTED_TYPE_NAMES[data_type.__name__]
        else:
            return data_type.__name__

    def validate(self, val):
        """ Validates value by passing into all validators

        :param val: Value to pass into validators
        :type val: Any

        :return: Errors or empty list.
        :rtype: list
        """
        errors = []

        if (not self.required) and val is None:
            return errors

        if self.data_type:
            err_msg = self.validate_type(val)

            if err_msg:	 # There was an error
                errors.append(err_msg)
                return errors

        for validator in self.validators:
            passed, err = validator(val)

            if not passed:
                errors.append(err)

        return errors

    def default_val(self):
        """Get default value"""
        if not self.default:
            return None
        if callable(self.default):
            return self.default()
        else:
            return self.default
