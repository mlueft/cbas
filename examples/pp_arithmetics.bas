
#define MACRO(%0,%1) CONTENT-%0-%1-   

MACRO("p0",1024)|test

MACRO

#define TEST a
TEST

#include test.pp

!.
#define BB .
#include test.pp
#undefine BB
!BB

#define AA hello world!
hello world!
AA

#define AA
#ifdef AA
OK - a ist definiert. 
#else
!! - a ist definiert. 
#endif
#undefine AA
#ifndef AA
OK - a ist nicht definiert. 
#else
!! - a ist nicht definiert. 
#endif

#config keepindentation true
#include test.pp
  #include test.pp
    #include test.pp

#config keepindentation false
    #include test.pp

#define AA 4
#if AA = 4
OK - aa = 4
#else
!! - aa = 4
#endif

#if 4 = 4
OK - 4 = 4
#else
!! - 4 = 4
#endif

#if 5 = 4
!! - 5 = 4
#else
OK - 5 = 4
#endif

#if 3 < 4
OK - 3 < 4
#else
!! - 3 < 4
#endif

#if 4 < 4
!! - 4 < 4
#else
OK - 4 < 4
#endif

#if 5 > 4
OK - 5 > 4
#else
!! - 5 > 4
#endif

#if 4 > 4
!! - 4 > 4
#else
OK - 4 > 4
#endif

#if 5 >= 4
OK - 5 >= 4
#else
!! - 5 >= 4
#endif

#if 4 >= 4
OK - 4 >= 4
#else
!! - 4 >= 4
#endif

#if 3 >= 4
!! - 3 >= 4
#else
OK - 3 >= 4
#endif

#if 3 <= 4
OK - 3 <= 4
#else
!! - 3 <= 4
#endif

#if 4 <= 4
OK - 4 <= 4
#else
!! - 4 <= 4
#endif

#if 5 <= 4
!! - 5 <= 4
#else
OK - 5 <= 4
#endif

#if 4 <> 4
!! - 4 <> 4
#else
OK - 4 <> 4
#endif

#if 5 <> 4
OK - 5 <> 4
#else
!! - 5 <> 4
#endif

#if 5 = 4+1
OK - 5 = 4+1
#else
!! - 5 = 4+1
#endif

#if 5 = 4-1
!! - 5 = 4-1
#else
OK - 5 = 4-1
#endif

#if 10 = 2*(10/2)+6-(2*(4-1))
OK - 10 = 2*(10/2)+6-(2*(4-1))
#else
!! - 10 = 2*(10/2)+6-(2*(4-1))
#endif

#define AA 2*(10/2)+6-(2*(4-1))
#if 10 = AA
OK - 10 = 2*(10/2)+6-(2*(4-1))
#else
!! - 10 = 2*(10/2)+6-(2*(4-1))
#endif

#if true
OK - true
#else
!! - true
#endif

#if false
!! - false
#else
OK - false
#endif

#if true = true
OK - true = true
#else
!! - true = true
#endif

#if true = false
!! - true = false
#else
OK - true = false
#endif

#if true <> false
OK - true <> false
#else
!! - true <> false
#endif

#if true <> true
!! - true <> true
#else
OK - true <> true
#endif

