import math

# 修正后的四舍五入
def my_round_45(float_num, n):
    result = int(float_num * math.pow(10, n) + 0.5) / math.pow(10, n)
    return result



