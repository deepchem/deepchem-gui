#!/bin/csh

cut -c-66 $1.pdbqt > $1.pdb
set a=`grep ENDMDL $1.pdb | wc -l`
set b=`expr $a - 2`
csplit -k -s -n 3 -f $1. $1.pdb '/^ENDMDL/+1' '{'$b'}'
foreach f ( $1.[0-9][0-9][0-9] )
  mv $f $f.pdb
end
