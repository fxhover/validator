# encoding=utf-8

from collections import defaultdict, OrderedDict
from .fields import Field, DeclarativeFieldsMetaclass


class BaseValidator(object):
    """ Base validation class, handles all logic. """

    def __init__(self, data):
        self._data = data  # type: dict
        # self._missing_fields = set()
        self._errors = defaultdict(list)
        self._validated = False

    # ------------------------------------------
    # Properties
    # ------------------------------------------

    @property
    def errors(self):
        """ Returns dictionary with or without errors.

        :return: Errors
        :rtype: defaultdict
        """
        # if not self._errors:
        if not self._validated:
            self.full_validate()
        return self._errors

    # @property
    # def missing_fields(self):
    #     """ Returns a set of the missing fields.
    #
    #     :return: True or False
    #     :rtype: bool
    #     """
    #     if not self._missing_fields:
    #         self._missing_fields = (
    #             set(self._required_fields.keys()) - set(self._data.keys())
    #         )
    #     return self._missing_fields

    # ------------------------------------------
    # Public Methods
    # ------------------------------------------

    def is_valid(self):
        """ Returns if there is errors in validation.

        :return: True or False
        :rtype: bool
        """
        return not self.errors

    def full_validate(self):
        """ Runs full validation against all defined Fields. """

        self._errors = defaultdict(list)

        # Add missing fields to part of errors
        # if there's missing fields.
        # if self.missing_fields:
        #     for field_name in self.missing_fields:
        #         field = self._fields[field_name]  # type: Field
        #         if field.default is None:
        #             self._errors[field_name].append("{} field is required.".format(field_name))

        # Pass values through validation
        # where this is a declared Field.
        # for key, val in self.data.items():
        for field_name, field in self._fields.items():
            try:
                field = self._fields[field_name]  # type: Field
            except KeyError:
                continue
            else:
                val = self._data.get(field_name)
                if val is None and field.default:
                    val = field.default_val()
                if val is None and field.required:
                    self._errors[field_name].append(
                        "{} field is required.".format(field_name))
                    continue
                errors = field.validate(val)
                if errors:
                    self._errors[field_name].extend(errors)
            finally:
                setattr(self, field_name, val)
        self._validated = True

    def error_str(self, sep="; "):
        """返回错误信息文本"""
        if not self.errors:
            return ""
        errors = []
        for field_name, field_errors in self.errors.items():
            errors.append(field_name + " : " + ",".join(field_errors))
        return sep.join(errors)

    def to_dict(self, fields=None):
        """返回数据dict"""
        result = OrderedDict()
        for field_name, field in self._fields.items():
            if fields and field_name not in fields:
                continue
            if hasattr(self, field_name):
                result[field_name] = getattr(self, field_name)
            else:
                result[field_name] = field.default_val()
        return dict(result)

    def __getitem__(self, item):
        if item in self._fields.keys():
            return getattr(self, item)
        raise AttributeError("{} has no field '{}'.".format(self.__class__, item))


class Validator(BaseValidator):
    """ Class used to define custom Validator classes. """
    __metaclass__ = DeclarativeFieldsMetaclass


