#! /bin/bash
#./make.sh [链接库名称] -f filename [参数] 
#参数将传递给filename可执行文件
#./make.sh -lm -f 1.c 1 2 3

#判断对应的链接库是否存在
function has_link()
{
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
if [ ${suffix} = cpp ]; then
	COMPILE=g++
fi

#检测对应的文件是否存在
if [ -e ${filename} ] && [ -f ${filename} ];  then
	#是否存在对应的bin文件夹
	test -e bin || mkdir bin
	#尝试编译文件 执行文件
	if ${COMPILE} ${filename} -o "bin/${target}" ${libs} ; then
		echo -e "\033[34mcompile success,now running\033[0m"
		./bin/${target}  ${args}
		echo -e "\033[34mprogram return\033[0m \033[31m$?\033[0m"
		exit 1
	else
		echo -e "\033[31mcompile error\033[0m"
	fi
else
	echo -e "\033[31mfile:${filename} not exist\033[0m" && exit 1
fi



