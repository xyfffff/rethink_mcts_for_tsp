#!/bin/bash
# author: 
rm test
rm code/*.o 
make
STARTTIME=$(date +%s)
tsp=("../500.txt")
instancenum=(500)
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

mkdir -p ./results/500

for ((i=0;i<$threads;i++));do
{
	touch ./results/${instancenum[j]}/result_${i}.txt
	./test $i ./results/${instancenum[j]}/result_${i}.txt ${tsp[j]} ${instancenum[j]} ${use_rec} ${rec_only} ${mcn} ${md} ${alpha} ${beta} ${ph} ${retart} ${retart_rec}
}&
done
wait


ENDTIME=$(date +%s)
echo "It takes $(($ENDTIME-$STARTTIME)) seconds to complete this task..."
echo "Done."
