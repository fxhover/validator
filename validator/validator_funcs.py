# encoding=utf-8


class ValidatorFuncs(object):

    @staticmethod
    def is_email(val):
        passed = False
        err = "{val} must contain @".format(val=val)

        if '@' in val:
            passed = True

        return passed, err

    @staticmethod
    def is_secure_password(val):
        passed = False
        err = "Password must be at least 8 characters in length and alphanumeric"

        if len(val) >= 8 and val.isalnum():
            passed = True

        return passed, err

    @staticmethod
    def is_min_length(min_length):
        def validator(val):
            passed = False
            err = "{val} must be at least {min_length} characters in length".format(val=val, min_length=min_length)

            if len(val) >= min_length:
                passed = True

            return passed, err

        return validator

    @staticmethod
    def is_max_length(max_length):
        def validator(val):
            passed = False
            err = "{val} must be at most {max_length} characters in length".format(val=val, max_length=max_length)

            if len(val) <= max_length:
                passed = True

            return passed, err

        return validator

    @staticmethod
    def is_gt_than(num):
        def validator(val):
            passed = False
            err = "{val} must be larger than {num}".format(val=val, num=num)

            if val > num:
                passed = True

            return passed, err

        return validator

    @staticmethod
    def is_gt_but_lt(flr, ceil):
        def validator(val):
            passed = False
            err = "{val} must be greater than {flr} and less than {ceil}".format(val=val, flr=flr, ceil=ceil)

            if flr < val < ceil:
                passed = True

            return passed, err

        return validator

    @staticmethod
    def is_in(enum_vals):
        def validator(val):
            passed = False
            err = "{val} must in {vals}.".format(val=val, vals=enum_vals)

            if val in enum_vals:
                passed = True

            return passed, err

        return validator
