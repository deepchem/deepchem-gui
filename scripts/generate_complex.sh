#!/bin/csh

cut -c-66 $2.pdbqt > $2.pdb

set a=`grep ENDMDL $2.pdb | wc -l`
set b=`expr $a - 2`
csplit -k -s -n 3 -f $2. $2.pdb '/^ENDMDL/+1' '{'$b'}'
foreach f ( $2.[0-9][0-9][0-9] )
  mv $f $f.pdb
end
cat $1.pdb $2.000.pdb | grep -v '^END   ' | grep -v '^END$' > $3.pdb
