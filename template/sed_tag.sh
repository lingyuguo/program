#!/bin/bash
###########path############
read -p "请输入您tgz所在的绝对路径 : " path
ls $path |grep  .tgz  > tag.txt
###########load  images###########
cat  tag.txt | while read line
do
	docker load -i ${line}
#	if [ $? -eq 0 ];then
#   		  echo"#####${line} 导入成功#####"
#	else
# 		  echo"#####${line} 导入失败#####"
#	fi
done
##########docker tag #############
sed -i "s/\.tgz/\ /g " `grep "\.tgz" -rl tag.txt`
sed -i "s/\#/\:/g" `grep "\#" -rl tag.txt`
sed -i "s/\_/\//g" `grep "\_" -rl tag.txt`
read -p "请输入您远端仓库的名称 : " warehouse
read -p "请输入您远端仓库的端口号 : " port
cat  tag.txt | while read line
do
  	tag=`echo "${line}" | awk -F '5001'  '{print $2}'`
   	warehouse_port="$warehouse:$port"
   	newtag=$warehouse_port$tag
   	docker tag  ${line}  $newtag
#    	if [ $? -eq 0 ];then
#                  echo"#####${line} 导入成功#####"
#        else    
#                  echo"#####${line} 导入失败#####"
#        fi
   	docker push ${line}  $newtag
   	echo "####耐心等待20s####"
   	sleep 20
#        if [ $? -eq 0 ];then
#                  echo"#####$newtag 导入成功#####"
#        else    
#                  echo"#####$newtag 导入失败#####"
#        fi
done
