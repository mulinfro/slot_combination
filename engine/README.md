#  语义

###  程序结构
 - builtin.py 内置关键词，特殊符号等
 - util.py
 - items.py  
 - stream.py 
 - config.py 配置文件
 - syntax.md  语法说明文件
 - syntax_check.py  语法检查辅助类
 - ac.py  AC自动机
 - tokens.py
 - ast.py  解析成语法树
 - parse.py  把语法树解析成特殊的Trie树，及后处理信息
 - search.py  搜索出所有可以匹配的规则
 - select.py  筛选出最优匹配
 - run.py 运行入口文件
 - post_register.py 后处理库注册
 - post_libs  定义后处理函数的目录
