#!/bin/bash
# author: 
rm test
rm code/*.o 
make
STARTTIME=$(date +%s)
tsp=("../1000.txt")
instancenum=(1000)
j=0
threads=64
use_rec=1
rec_only=$1
mcn=$2
md=$3
alpha=$4
beta=$5
ph=$6
retart=$7
retart_rec=$8
Param_T=$9

mkdir -p ./results/1000

for ((i=0;i<$threads;i++));do
{
	touch ./results/${instancenum[j]}/result_${i}.txt
	./test $i ./results/${instancenum[j]}/result_${i}.txt ${tsp[j]} ${instancenum[j]} ${use_rec} ${rec_only} ${mcn} ${md} ${alpha} ${beta} ${ph} ${retart} ${retart_rec} ${Param_T}
}&
done
wait


ENDTIME=$(date +%s)
echo "It takes $(($ENDTIME-$STARTTIME)) seconds to complete this task..."
echo "Done."
