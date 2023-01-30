from utils.logger import run_log


def verity_handler(status_code, res_data, check_type, judge_value):
    # 需要先根据status code判断，返回是否为200。
    # 根据需要校验的字段去判断，是否符合预期。
    # 需要返回的内容：error code, error msg.
    # check_type：0 只校验返回为200，1 校验返回内容是否为空，2 校验返回内容指定字段

    error_code = error_msg = None

    if status_code != 200:
        error_code = 5001
        error_msg = f"请求异常， 状态码{status_code}与200不符。"
    # 0 只校验返回为200
    if check_type == 0:
        run_log.debug(f"check request 200: {error_code}, {error_msg}")
        return error_code, error_msg

    if len(res_data) == 0:
        error_code = 5002
        error_msg = f"请求返回内容为空。"
    # 1 校验返回内容是否为空
    if check_type == 1:
        run_log.debug(f"check empty: {error_code}, {error_msg}")
        return error_code, error_msg

    if judge_value is None or check_type != 2:
        run_log.debug("check_type error or judge_value is empty!")
    else:
        fail_result, fail_mes = judge_json_result(res_data, judge_value)
        if len(fail_result) != 0:
            error_code = 5003
            fail_result = combine_text(fail_result)
            # print(fail_result)
            error_msg = f'响应结果字段检查未通过(关键字缺失或值为空), 未通过关键字 : {fail_result}'
        run_log.debug(f"check result: {error_code}, {error_msg}")
    return error_code, error_msg


def judge_json_result(data, judgemes):
    fail_result = []
    fail_mes = []
    spiltres = pathsplit(judgemes)
    for s in spiltres:
        path, num, condition, judgestand = s
        res = single_result(data, path, num, condition, judgestand)
        if res is not True:
            fail_result.append(s)
            if isinstance(res, list):
                fail_mes.append(res)
    return fail_result, fail_mes


def single_result(data, path, num, condition, judge):
    error_result = True
    count_conform = 0
    error_mes = []

    if not data:
        return False

    flag = False
    for i in condition:
        if i is not None:
            k, s, v, f = i
            if f == '*':
                flag = True

    def wrap(data, path, num, condition, judge):

        nonlocal count_conform
        nonlocal error_result
        nonlocal error_mes

        if not error_result:
            return False

        length = len(path)
        if length > 1:
            pi = path[0]
            ni = num[0]
            ci = condition[0]

            if isinstance(data, dict):
                data = data.get(pi)
                if isinstance(data, list) and len(data) != 0:
                    if ni is None and ci is None:
                        for t in data:
                            wrap(t, path[1:], num[1:], condition[1:], judge)
                        return

                    if ni is None and ci is not None:
                        k, symbol, v, flag = ci
                        for t in data:
                            if data_judge_flag(t, k, symbol, v):
                                wrap(t, path[1:], num[1:], condition[1:], judge)
                        return

                    if ni is not None and ci is None:
                        if len(data) > int(ni):
                            data = data[int(ni)]
                            return wrap(data, path[1:], num[1:], condition[1:], judge)

                    if ni is not None and ci is not None:
                        if len(data) > int(ni):
                            data = data[int(ni)]
                            k, symbol, v, flag = ci
                            if data_judge_flag(data, k, symbol, v):
                                return wrap(data, path[1:], num[1:], condition[1:], judge)
                elif isinstance(data, dict):
                    return wrap(data, path[1:], num[1:], condition[1:], judge)

            error_result = False
            return False

        count_conform += 1
        field = path[0]
        mes = panduan(data, field, judge)
        if isinstance(mes, dict):
            if mes["type"] != "web_url_item":
                error_result = False
                error_mes.append(mes)
        elif isinstance(mes, list):
            for d in mes:
                if d["type"] != "web_url_item":
                    error_result = False
                    error_mes.append(d)
        # if mes is not True:
        #     error_result = False
        #     error_mes.append(mes)

    wrap(data, path, num, condition, judge)

    if flag:
        if count_conform == 0:
            error_result = False
            return False

    if not error_result:
        return error_mes
    else:
        return True


def data_judge_flag(data, k, symbol, v):
    if isinstance(data, dict):
        if symbol == '==':
            return data.get(k) == v
        elif symbol == '!=':
            return data.get(k) != v
        elif symbol == '>=':
            return data.get(k) >= v
        elif symbol == '<=':
            return data.get(k) <= v
        else:
            return False
    else:
        return False


def panduan(data, field, judge):
    if not data:
        return False
    # print(f"data: {data}")
    # print(f"field: {field}")
    # print(f"judge: {judge}")
    if isinstance(data, dict):
        value = data.get(field)
        if judge == 'NN':
            # print(f"value: {value}")
            if value is not None:
                if field == "pic" and len(value) != 0:
                    # print(f"picture length check: {len(value)}")
                    return True
                return True

        if judge == 'EX':
            keys = data.keys()
            if field in keys:
                return True

        if judge[0] == 'L':
            length = int(judge[1:])
            # if isinstance(value, list):
            if len(value) >= length:
                return True

        if judge[0] == 'V':
            expect_value = judge[2:]
            print(f"expect_value: {expect_value}")
            if value == expect_value:
                return True

        data_err = {
            "id": data.get("id"),
            "name": data.get("name"),
            "type": data.get("type"),
            "poster": ""
        }
        if data.get("poster"):
            data_err["poster"] = data.get("poster")
        return data_err

    elif isinstance(data, list):
        error_data = []
        for d in data:
            if isinstance(d, dict):
                value = d.get(field)
                if judge == 'NN':
                    if not value or value == 0:
                        error_data.append(d)

                if judge == 'EX':
                    keys = d.keys()
                    if field not in keys:
                        error_data.append(d)

                if judge[0] == 'L':
                    length = int(judge[1:])
                    # if isinstance(value, list):
                    if len(value) < length:
                        error_data.append(d)
                    # else:
                    #     error_data.append(d)

                if judge[0] == 'V':
                    expect_value = judge[2:]
                    print(f"expect_value: {expect_value}")
                    if value == expect_value:
                        return True

        if error_data:
            return error_data
        else:
            return True
    else:
        return False


def pathsplit(strdata):
    """
    根据约定条件对字符串进行分割.
    例: 'relatedCards(type==normal)/resources/resources(*type!=publisher)/id'
    返回:
    [[
    ['relatedCards', 'resources', 'resources', 'id'],
    [None, None, None, None],
    [['type', '==', 'normal', None], None, ['type', '!=', 'publisher', '*'], None],
    'NN']]
    第一个是字段路径,
    第二个是字段值所选择的列表位置,如果为None则遍历列表,否则选择对应位置元素 (前提是列表,如果是字典或者字符串则不做此选择),
    第三个是根据特定条件选择具体的元素(例如,选择type 等于 banners的列表元素),
    第四个是判断原则(NN: notNone, EX: exist, L4: 列表长度不小于4)
    """
    result = []
    if not strdata:
        return strdata

    for s in strdata:
        s = s.strip()

        if ':' in s:
            path = s.split(':')[0]
            judge = s.split(':')[1]
        else:
            path = s
            judge = 'NN'

        if '/' in path:
            paths = path.split('/')[:-1]
            field = path.split('/')[-1]
        else:
            paths = None
            field = path

        fields = field.split(',')
        # print(fields)

        pathlist = []
        pathnum = []
        pathext = []
        if paths:
            for p in paths:
                p, ext = extract(p, '(', ')')
                if '-' in p:
                    p1 = p.split('-')[0]
                    p2 = p.split('-')[1]
                else:
                    p1 = p
                    p2 = None
                pathlist.append(p1)
                pathnum.append(p2)
                pathext.append(ext)

        for f in fields:
            res = []
            # 校验等于
            if "==" in f:
                f, ext = extract(f, '(', ')')
                if '-' in f:
                    p1 = f.split('-')[0]
                    p2 = f.split('-')[1]
                else:
                    p1 = f
                    p2 = None
                pathlist.append(p1)
                pathnum.append(p2)
                pathext.append(ext)

            temp1 = pathlist[:]
            temp2 = pathnum[:]
            temp3 = pathext[:]

            temp1.append(f)
            temp2.append(None)
            temp3.append(None)

            res.append(temp1)
            res.append(temp2)
            res.append(temp3)
            res.append(judge)

            result.append(res)
    return result


def extract(strdata, lletter='(', rletter=')'):
    """
    提取出需要判断的k,v和判断条件,并返回剩下的字符串
    例: resources(*type==banners)   返回:resources,['type', '==', 'banners', '*]
    """
    judge_flag = ['==', '!=', '>=', '<=']

    if lletter in strdata and rletter in strdata:
        l = strdata.find(lletter)
        r = strdata.find(rletter)

        other = strdata[:l] + strdata[r + 1:]
        ext = strdata[l + 1:r]
        if ext[0] == '*':
            flag = '*'
            ext = ext[1:]
        else:
            flag = None
        res = []
        for x in judge_flag:
            if x in ext:
                length = len(x)
                k = ext[:ext.find(x)]
                v = ext[ext.find(x) + length:]
                symbol = x
                res.append(k)
                res.append(symbol)
                res.append(v)
                res.append(flag)
        return other, res
    else:
        return strdata, None


def combine_text(spilt_result):
    """
    将分隔展开的检查字段在合并起来,便于查看
    :param spilt_result:
    :return:
    """
    res = '\n'
    for s in spilt_result:
        path, num, condition, judge = s
        if len(path) is not len(num):
            return False
        for i in range(len(path)):
            res += path[i]
            if condition[i] is not None:
                k, symbol, v, flag = condition[i]
                if flag is None:
                    flag = ''
                res += f'({flag}{k}{symbol}{v})'
            if num[i] is not None:
                res += f'-{num[i]}'
            if i != len(path) - 1:
                res += '/'
        res += f':{judge}; \n'
    res = res.replace('NN', '字段缺失或值为空')
    res = res.replace('EX', '字段不存在')
    res = res.replace(':L', ':字段值个数不足')
    res = res.replace(':V_', ':字段值与预期值不符_')
    return res
