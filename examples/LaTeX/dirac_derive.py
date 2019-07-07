from __future__ import print_function
import sys

from sympy import symbols,sin,cos,latex
from galgebra.ga import Ga
from galgebra.printer import Format, xpdf

g = '# 0 0 0,0 # 0 0,0 0 # 0,0 0 0 #'

Format()
(sp4d,g0,g1,g2,g3) = Ga.build('gamma*0|1|2|3',g=g)

psi = sp4d.mv('psi','even')

print(psi)

B = sp4d.mv('B','bivector')

print(B)

print(B*psi-psi*B)

# xpdf()
xpdf(pdfprog=None)
