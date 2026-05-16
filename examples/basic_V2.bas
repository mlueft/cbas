a = sys(10,20,-ABS(19))
a = str$(10)
a = ABS(ABS(10))
a = asc(10)
a = atn(10)
a = right$(10)
a = left$(10)
a = chr$(10)
a = mid$(10)
a = peek(10)
a = cos(10)
a = fre(10)
a = int(10)
a = len(10)
a = log(10)
a = pos(10)
a = rnd(10)
a = sgn(10)
a = sin(10)
a = spc(10)
a = sqr(10)
a = tab(10)
a = tan(10)
a = usr(10)
a = val(10)
a = EXP(10)

clr
new
restore
return
st
status
stop
ti
ti$
time
time$
π
end  :rem - end the program. switches to direct mode
cont :rem - continues a basic program

GO TO 120
GOTO 121
GOSUB 123
RUN 124
close 3

POKE 1024,4 : rem test
VERIFY 1024,4 : rem test
SAVE "WWW" : rem test
SAVE "WWW",8 : rem test
SAVE "WWW",8,1 : rem test
LOAD "WWW" : rem test
LOAD "WWW",8 : rem test
LOAD "WWW",8,1 : rem test
WAIT 1024 : rem test
WAIT 1024,4 : rem test
WAIT 1024,4,1 : rem test

OPEN 1 : rem test
OPEN 1 ,2 : rem test
OPEN 1 ,2 , 4: rem test
OPEN 1 ,2 , 4, "filename": rem test
OPEN 1 ,2 , 4, "filename,type": rem test
OPEN 1 ,2 , 4, "filename,type,mode": rem test
NEXT A: rem test
NEXT A$: rem test
NEXT A%: rem test
NEXT A$, a$: rem test

LIST  : rem test
LIST 10 : rem test
LIST 10-20 : rem test
LET a = 8+3/2 : rem test
FN test(19) : rem test
READ 10, 10, 10 : rem test
DATA 10, "a", b : rem test
GET a : rem test
GET a,b,c : rem test
GET# 1,a,b,c : rem test
INPUT# 1,a,b,c : rem test
PRINT# 1,a,b,c : rem test
CMD 1, a,b;c : rem test
def fn te(a)=2+a:a=1 : rem test
ON a GOSUB 10,20,30: a=1 : rem test
ON a GOTO 10,20,30:i=10 : rem test
INPUT "Bitte um Eingabe!";a : rem test
INPUT "Bitte um Eingabe!";a,b : rem test
INPUT "Bitte um Eingabe!";a,b,c : rem test


dim a(10): rem test
dim a$(10): rem test
dim a%(10): rem test
dim a%(10):i=0: rem test
dim a(10,10): rem test
dim a(10)=4+3/4: rem test
print "a": rem test
print "a","b": rem test
print "a";"b": rem test
print "a";"b";: rem test

if 10 = 11 then i=0: rem test
if 10 < 11 then i=0: rem test
if 10 < 11 then i=0:b=10: rem test
IF 11<10 GOTO 10: rem test
IF 4+3<10 THEN 1024: rem test
for i = 0 to 10: rem test
for i = a to 10 step 2: rem test
    rem loop code
    i=10
    a= fn test(10)
    print "hallo"
next i: rem test
print "global"
