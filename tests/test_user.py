# encoding=utf-8

from validator import Validator, Field, ValidatorFuncs


class UserParams(Validator):
    """
    User params validator.
    """
    username = Field(
        data_type=str,
        validators=[ValidatorFuncs.is_min_length(5), ValidatorFuncs.is_max_length(50)],
        required=True
    )
    email = Field(
        data_type=str,
        validators=[ValidatorFuncs.is_email],
        required=True
    )
    password = Field(
        data_type=str,
        validators=[ValidatorFuncs.is_secure_password],
        required=True
    )
    age = Field(
        data_type=int,
        validators=[ValidatorFuncs.is_gt_than(10)],
        required=True
    )
    sex = Field(
        data_type=str,
        validators=[ValidatorFuncs.is_in(["男", "女"])],
        required=True
    )
    status = Field(
        data_type=int,
        validators=[ValidatorFuncs.is_in([0, 1])],
        default=1
    )


user_params = UserParams({
    "username": "test",
    "email": "xxx",
    "age": 9,
    # "sex": "其他"
})



# 验证，返回错误信息字典
print(user_params.errors)

# 验证，返回str格式的错误信息
print(user_params.error_str())

# 属性方式获取字段值
print(user_params.sex)

# []方式获取字段值
print(user_params["username"])

# 自动填充默认值
print(user_params.status)
