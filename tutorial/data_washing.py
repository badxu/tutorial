# -*- coding:utf-8 -*-
# 列表过滤和使用lambda函数过滤
import re
re_url = re.compile('^\/maszbw/infodetail/\?.*')

if __name__ == "__main__":
    info = """>>>>>用来演示普通方式过滤列表和使用lambda函数过滤<<<<<"""

def filterForLi(li):
    info = ">>>>>使用普通过滤列表<<<<<"
    out_data = [element for element in li if re_url.match(element)!= None] #int类型没有长度，所以需要首先排除
# 使用lambda函数过滤
def filterByLambda(li):
    info = ">>>>>使用lambda函数进行列表信息过滤<<<<<"
    # 定义一个lambda函数:int类型没有长度，所以需要首先排除
    g = lambda x : not isinstance(x,int) and len(x)>5
    out_data = [element for element in li if g(element)]
