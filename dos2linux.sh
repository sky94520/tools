#!/bin/bash
#author:任继位
#description:负责将编码转换为utf-8 以及将CRLF=> LF
#文件
#-r 反转，表示unix=>dos

#对文件进行转换
function trans()
{
	option=
	if [ $# == 2 ] ;then
		option=$2
	fi
	
	if [ "$option" == "-r" ] ; then
		unix2dos $1 && enconv -x $1
	else
		dos2unix $1 && enconv $1
	fi

	return $?
}

#参数为1时且为文件
if [ $# == "1" ] && [ -f "$1" ]; then
	trans $1
elif [ $# == "2" ] && [ "$1" == "-r" ] && [ -d "$2" ]; then
	#递归获取文件名
	declare -a list=( $(ls -R "$1") )
	#get length of the array
	len=${#list[*]}
	
	for (( i=0; i<${len}; i=i+1))
	do
		#simple and delete ':'
		name=${list[${i}]%:}
		#regular file
		if [ -f ${name} ]; then
			trans ${name}
		#directory
		elif [ -d ${name} ]; then
			path=${name%/}
		#try adding basename
		else
			filename="${path}/${name}"

			if [ -f "${filename}" ]; then
				trans ${filename}
			fi
		fi
	done
else	
	echo "error:Please input a filename or -r dir" && exit 1
fi
