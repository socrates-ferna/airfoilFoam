#!/bin/sh
cd ${0%/*} || exit 1
rango1=$(seq 0 2 10)
rango2=$(seq 11 24)
rutres=../caso_gen/resultados
. $WM_PROJECT_DIR/bin/tools/RunFunctions
#-------------------------------------Preparamos la carpeta resultados-----------------------------------------
cd caso_gen

mkdir resultados 
cd resultados
mkdir coeficientes paraview residuals yPlus
cd paraview
mkdir $rango1 $rango2 
cd ../coeficientes

touch polar.dat
echo "Alpha	# Time                  Cm                      Cd                      Cl                      " >> polar.dat 
cd ../yPlus
touch yPlus.dat
echo "Alpha          # Time                  patch                      min                      max                  avg" >> yPlus.dat 
cd ../../../
for i in $rango1 $rango2;do
printf "Simulando alfa"
printf $i
cd $i/

runApplication decomposePar

runParallel `getApplication`

runApplication reconstructPar -latestTime

$(getApplication) -postProcess -func yPlus

cp -r `foamListTimes` $rutres/paraview/$i

mv postProcessing/residuals/0/residuals.dat $rutres/residuals/residuals_$i.dat

coefs=$(tail -n 1 postProcessing/forceCoeffs/0/forceCoeffs.dat)
y_alfa=$(tail -n 1 postProcessing/yPlus//yPlus_*.dat)

echo "$i	$coefs" >> $rutres/coeficientes/polar.dat
echo "$i        $y_alfa" >> $rutres/yPlus/yPlus.dat
mv postProcessing/yPlus $rutres/yPlus/yPlus_$i
mv postProcessing/forceCoeffs/0/forceCoeffs.dat $rutres/coeficientes/coeficientes_$i.dat
cd ..
rm -r $i
done
