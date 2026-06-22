goto @main

#define PRINTAT(x,y,message) POKE781,y:POKE782,x:SYS(65520):PRINT message
#define PRINTAT1(x,y,message) print LEFT$( "{home}" + 25 * "{down}" ,Y); SPC(X); message;
#define CLR print "{clr}"
#define QTY 1
#define TEST 2

@main
{
    CLR
    _runner=0
    _start = TI
    @performanceLoop0
    {
        // ////////////////////////
        // TESTCODE 0 BEGINN
        {
            // IF variable assignment slower then peek poke?
            #if TEST = 1
            {
                _a = 0
                for _i = 0 to 255
                _a = _a + 1
                next _i
            }
            #endif
            #if TEST = 2
            {
                for _i = 0 to 255
                    PRINTAT(10,10,"0hallo")
                next _i
            }
            #endif
        }
        // TESTCODE 0 END
        // ////////////////////////
        _runner=_runner+1
        if _runner < QTY goto @performanceLoop0
        _end=TI
        _duration0 = _end-_start
    }

    _runner=0
    _start = TI
    @performanceLoop1
    {
        // ////////////////////////
        // TESTCODE 1 BEGINN
        {
            #if TEST = 1
            {
                poke 1023, 0
                for _i = 0 to 254

                _value = peek(1023) + 1
                poke 1023, _value

                next _i
            }
            #endif
            #if TEST = 2
            {
                for _i = 0 to 255
                    PRINTAT1(10,10,"1hallo")
                next _i
            }

        }
        // TESTCODE 1 END
        // ////////////////////////
        _runner=_runner+1
        if _runner < QTY goto @performanceLoop1
        _end=TI
        _duration1 = _end-_start
    }
}

@quit
{
    CLR
    // manipulates basic memory so list doesn't show the listing
    // poke 2049,0
    // poke 2050,0
    // poke 2051,0
    PRINTAT( 0,0, "load";chr$(34);"perf.bas.prg";chr$(34);"";chr$(44);"8";chr$(44);"1" )
    PRINTAT( 0,5, "run" )
    PRINTAT( 0,6, "list -10" )

    _duration0 = (_duration0/60)*1000
    _duration1 = (_duration1/60)*1000
    print ""
    PRINT "quantity tests  :"; QTY
    PRINT "duration tests 0:"; _duration0; "ms"
    PRINT "duration tests 1:"; _duration1; "ms"
    PRINT ""
    if _duration > 0 then{
        PRINT "delta:"; _duration1/_duration0*100; "%"
    }
    print ""
}
