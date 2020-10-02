Compilator pseudocod

-> variable declaration: (Di/Do: a natural, b real) sau (a <-(real) 10.5) sau (a <- 10.5 if a already declared)
-> mathematical and logical expressions
'''
a >= 10
a == 10
a != 10
'''

-> if else statements
'''
(daca a > 10 atunci
    scrie a
altfel
    scrie 10
sfdaca) sau (
daca a > 10 atunci
    scrie a
sfdaca
)
'''

-> Read and write instructions
'''
scrie a, b, c
citeste nr1, nr2
'''

!!! In the current version it's impossible to create string variables. You can just use strings in expressions...

More complexity will be added in the future

The compiler is outputing c++ code that is then compiled using g++

See the file program.pseudo as an example algorithm written in pseudocode. 
