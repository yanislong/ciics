url = "http://sittpapc.ciics.cn"
username = "lihailong@ciics"
passwd = "lihailong123"
mysqluser = "lihailong"
mysqlpasswd = "lihailong123"
mysql_host = "10.9.19.71"

expression = [{"是否医保定点医院":1,"责任类型":(2,3),"责任细分":(11,12)},
        {"是否医保定点医院":1,"责任类型":(1,4),"责任细分":(11,12)},
        {"是否医保定点医院":1,"责任类型":(2,3),"责任细分":(11,12)},
        {"是否医保定点医院":1,"责任类型":(2,3),"人工指定":1,"医院等级":32},
        {"是否医保定点医院":1,"责任类型":(1,4),"人工指定":1,"医院等级":32},
        {"责任细分":13,"人工指定":1,"是否医保定点医院":0},
        {"责任细分":13,"人工指定":1,"是否医保定点医院":1},
        {"责任细分":(11,12),"人工指定":1,"是否医保定点医院":1,"责任类型":(2,3)},
        {"责任细分":(11,12),"人工指定":1,"是否医保定点医院":1,"责任类型":(1,4)},
        {"责任细分":(11,12),"是否医保定点医院":1}]

text = """[计划一自付一]
        如果:{是否医保定点医院}='是' 并且  ({责任类型} = '门诊'  或者 {责任类型} = '门诊慢性病') 并且 {责任细分} != '女工门诊' 并且 {责任细分} != '女工住院'
        那么:自付一门诊;
        如果:{是否医保定点医院}='是' 并且  ( {责任类型} = '住院' 或者  {责任类型} = '门诊特殊病') 并且 {责任细分} != '女工门诊' 并且 {责任细分} != '女工住院'
        那么:自付一住院;
        [计划二自付门诊一千]
        如果:{是否医保定点医院}='是' 并且  ({责任类型} = '门诊' 或者 {责任类型} = '门诊慢性病')  并且 {责任细分} != '女工门诊' 并且 {责任细分} != '女工住院'
        那么: 门诊自费
        [计划三牙科三甲自费]
        如果:{是否医保定点医院}='是' 并且 {医院等级} = '三级甲等医院' 并且 人工指定({三甲}) = '是' 并且  ({责任类型} = '门诊' 或者 {责任类型} = '门诊慢性病') 并且 {责任细分} != '女工门诊' 并且 {责任细分} != '女工住院'
        那么:门诊全科自费;
        如果: {是否医保定点医院}='是' 并且  {医院等级} = '三级甲等医院' 并且 人工指定({三甲}) = '是' 并且 ({责任类型} = '住院' 或者 {责任类型} = '门诊特殊病') 并且 {责任细分} != '女工门诊' 并且 {责任细分} != '女工住院'
        那么:住院全科自费;
        如果:{责任细分} = '牙科'  并且 人工指定({牙科}) = '是' 并且  {是否医保定点医院} = '否' 并且 {责任细分} != '女工门诊' 并且 {责任细分} != '女工住院'
        那么:牙科自费非定点;
        如果:{责任细分} = '牙科'  并且 人工指定({牙科}) = '是' 并且  {是否医保定点医院} = '是' 并且 {责任细分} != '女工门诊' 并且 {责任细分} != '女工住院'
        那么:牙科自费定点;
        [计划四高龄重疾自费]
        如果: {是否医保定点医院}='是' 并且 人工指定({高龄重疾}) = '是' 并且 ({责任类型} = '门诊' 或者  {责任类型}='门诊慢性病') 并且 {责任细分} != '女工门诊' 并且 {责任细分} != '女工住院'
        那么:高龄重疾自费门诊;
        如果: {是否医保定点医院}='是' 并且 人工指定({高龄重疾}) = '是' 并且 ({责任类型} = '住院' 或者 {责任类型} = '门诊特殊病') 并且 {责任细分} != '女工门诊' 并且 {责任细分} != '女工住院'
        那么:高龄重疾自费住院;
        [计划五女工自付一]
        如果:{是否医保定点医院}='是' 并且  {责任细分} = '女工门诊' 或者 {责任细分} = '女工住院'
        那么:女工自付一;
        [方案一]
        如果:
        那么:计划五女工自付一;
        如果:
        那么:计划一自付一;
        如果:
        那么:计划三牙科三甲自费;
        如果:
        那么:计划四高龄重疾自费;
        如果:
        那么:计划二自付门诊一千"""
