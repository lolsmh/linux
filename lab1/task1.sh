#!/bin/bash

compareFiles() {
	if cmp -s "$1" "$2" ;
	then
		echo "YES"
	else
		echo "NO"
	fi
}

testDirectory='/home/user/test'
testSubDirectory="${testDirectory}/.sub"
linksDirectory="${testDirectory}/links"
listPath="${testDirectory}/list"
list1Path="${testDirectory}/list1"
listHlinkPath="${linksDirectory}/list_hlink"
listSlinkPath="${linksDirectory}/list_slink"
listLinkPath='/home/user/list_link'
listConfPath='/home/user/list_conf'
listDPath='/home/user/list_d'
listConfDPath='/home/user/list_conf_d'
manPath='/home/man.txt'
concatManPath='man.dir/concatMan.txt'
filesToRemove=($listLinkPath $listConfPath $listDPath $listConfDPath $manPath)
directoriesToRemove=($testDirectory "man.dir")

for directory in ${directoriesToRemove[*]}
do
	if [[ -d $directory ]]
	then
		rm -f -r $directory
	fi
done


for file in ${filesToRemove[*]}
do
	if [[ -f $file ]]
	then
		rm -f $file
	fi
done


#1
mkdir $testDirectory

#2
echo "Directories" > $listPath
ls -a /etc/*/ >> $listPath
echo "Files" >> $listPath
ls -a -p /etc | grep -v / >> $listPath

#3
echo "Count of directories" >> $listPath
ls -a -l /etc | grep -c ^d >> $listPath
echo "Count of hidden files" >> $listPath
find /etc -name ".*" -ls | wc -l >> $listPath

#4
mkdir $linksDirectory

#5
ln $listPath $listHlinkPath

#6
ln -s $listPath $listSlinkPath

#7
echo "Count of hard links on list"
ls -l $listPath | wc -l
echo "Count of hard links on list_hlink"
ls -l $listHlinkPath | wc -l
echo "Count of hard links on list_slink"
ls -l $listSlinkPath | wc -l

#8
cat $listPath | wc -l >> $listHlinkPath

#9
compareFiles $listHlinkPath $listSlinkPath

#10
mv $listPath $list1Path

#11
compareFiles $listHlinkPath $listSlinkPath

#12
ln $list1Path $listLinkPath

#13
ls -R -a  /etc | grep '\.conf$' >> $listConfPath

#14
ls -a /etc | grep '\.d$' >> $listDPath

#15
cat $listConfPath >> $listConfDPath
cat $listDPath >> $listConfDPath

#16
mkdir $testSubDirectory

#17
cp $listConfDPath $testSubDirectory

#18
cp -b $listConfDPath $testSubDirectory

#19
find $testDirectory -name "*"

#20
man man > $manPath

#21
split -b 1k $manPath "s_"

#22
mkdir man.dir

#23
mv $PWD/s_* $PWD/man.dir

#24
cat man.dir/s_?? > $concatManPath

#25
compareFiles $manPath $concatManPath

#26
echo "$(echo 'I am hungry and begging for pizza' | cat $manPath)" > $manPath
echo "Also I would like to buy the money store vinyl by Death Grips" >> $manPath

#27
diff $concatManPath $manPath > mapPatchfile.txt

#28
mv $PWD/mapPatchfile.txt $PWD/man.dir

#29
patch $concatManPath $PWD/man.dir/mapPatchfile.txt

#30
compareFiles $concatManPath $manPath
