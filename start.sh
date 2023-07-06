#! /bin/bash
# application='/home/wangping/'

# py='/usr/bin/python3.6'
# py='python3'

b=`ps aux| grep '/usr/bin/python3.6 app.py' | grep -v 'grep'| wc -l`
if [ ! $1 ];then
 echo "请传参数 start|stop|restart"  
else
 if [ $1 == "start" ];then
    if [ "$b" -gt "0" ];then
        echo "<---------------------程序总是运行--------------------->"
    else
        nohup /usr/bin/python3.6 app.py >output.log 2>log &
        echo "<---------------------程序运行成功--------------------->" 
        pid=`ps aux | grep '/usr/bin/python3.6 app.py' | grep -v 'grep' | awk '{print $2}'`
        echo $pid
   fi
 fi

 if [ $1 == 'stop' ];then
    pid=`ps aux | grep '/usr/bin/python3.6 app.py' | grep -v 'grep' | awk '{print $2}'`
    echo $pid
    if [ ! $pid ];then
      echo "<--------程序不在运行------->"
    else
      kill -s 9 $pid
      echo "<--------程序已停止------->"
    fi
 fi

 if [ $1 == 'restart' ];then
    pid=`ps aux | grep '/usr/bin/python3.6 app.py' | grep -v 'grep' | awk '{print $2}'`
    echo $pid
    if [ ! $pid ];then
      nohup /usr/bin/python3.6 app.py >output.log 2>log &
      echo "<---------------------程序未在运行，程序已启动--------------------->"
      pid=`ps aux | grep '/usr/bin/python3.6 app.py' | grep -v 'grep' | awk '{print $2}'`
      echo $pid
    else
      kill -s 9 $pid
      nohup /usr/bin/python3.6 app.py >output.log 2>log &
      echo "<---------------------程序已重启--------------------->"
      pid=`ps aux | grep '/usr/bin/python3.6 app.py' | grep -v 'grep' | awk '{print $2}'`
      echo $pid
    fi
 fi
fi
