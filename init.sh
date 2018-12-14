#! /bin/sh
ls

# && 短路功能 即前边 test 结果成立 则执行下一条 反之不执行
test "$(pip3 list | grep Flask)" = '' && pip3 install flask flask-restful
test "$(pip3 list | grep selenium)" = '' && pip3 install pip3 install selenium
test "$(pip3 list | grep pymongo)" = '' && pip3 install pip3 install pymongo

python3 ./src/serve/ApiServe

# 发现 grep -q 静默模式 即 $? == 0 为已找到； $? == 1 未找到； $? > 1 命令执行错误； 
# pss: 在 mac 报错 Message: 'wheel          0.31.1 ' 暂未解决
