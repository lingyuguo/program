用python脚本将主机的信息收取到excle中
1.ansible

`ansible <name> -m copy -a "src=/root/env-check.py dest=/root/env-check.py"
  ansible <name>  -m shell  -a "python /root/env-check.py" > env.txt`

2.执行python excle.py


