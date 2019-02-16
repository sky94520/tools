#! /bin/bash
#./make.sh [链接库名称] -f filename [参数] 
#参数将传递给filename可执行文件
#./make.sh -lm -f 1.c 1 2 3

#bug 更新命令行参数
# make.sh -f "1 2 3" 传递字符串“1 2 3”
# make.sh -f 1 2 3 传递1 2 3

#判断对应的链接库是否存在
function has_link()
{
	return 0
}

#运行c/c++程序
#$1 编译工具gcc/g++
#$2 filename 文件名
#$3 target 编译文件名
#$4 libs 追加库
function compile_and_run_c()
{
	COMPILE=$1
	filename=$2
	target=$3
	libs=$4

	if ${COMPILE} ${filename} -o "bin/${target}" ${libs} ; then
		echo -e "\033[34mcompile success,now running\033[0m"
		#execute
		./bin/${target} ${args}
		echo -e "\033[34mprogram return\033[0m \033[31m$?\033[0m"
		exit 1
	else
		echo -e "\033[31mcompile error\033[0m"
	fi

	return 0
}

#编译并运行java程序 把class文件放在bin目录下 需要bin目录存在
#$1 filename 文件名
#$2 target 目标文件
function compile_and_run_java()
{
	filename=$1
	target=$2

	if javac -d bin ${filename} ; then
		cd bin && java ${target} && cd ..
	else
		echo -e "\033[31mcompile error\033[0m"
	fi
	return 0
}

libs=
#先处理链接库
while [ -n "$1" ]
do
	case "$1" in
		#对应的文件
		"-f") break ;;
		#要链接的库
		*) 
		if has_link "$1" ; then
			libs="${libs} $1"
			shift
		fi
	esac
done

#处理后续参数
set --$(getopt "f:" "$@")

filename=
args=

while [ -n "$1" ]
do
	case "$1" in
		"-f")
			filename="$2"
			shift 2
			;;
		"--") shift ;;
		"?") 
			echo "Invalid parameter $1"
			shift;;
		*) 
			args="${args} $1"
			shift ;;
	esac
done

#去除文件扩展名
target=${filename%.*}
#获得文件扩展名
suffix=${filename##*.}

COMPILE=gcc
if [ "${suffix}" = "cpp" ]; then
	COMPILE=g++
elif [ "${suffix}" = "c" ]; then
	COMPILE=gcc
elif [ "${suffix}" = "java" ]; then
	COMPILE=javac
fi

#检测对应的文件是否存在
if [ -e ${filename} ] && [ -f ${filename} ];  then
	#是否存在对应的bin文件夹
	test -e bin || mkdir bin
	#尝试编译文件 执行文件
	if [ "${suffix}" = "java" ]; then
		compile_and_run_java ${filename} ${target}
	else
		compile_and_run_c ${COMPILE} ${filename} ${target} ${libs}
fi
else
	echo -e "\033[31mfile:${filename} not exist\033[0m" && exit 1
fi



