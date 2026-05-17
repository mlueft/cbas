
#define PRINTAT(x,y,message) POKE781,y:POKE782,x:SYS(65520):PRINT message

goto @main


@runMenu
    print "{clr}"
    #define POS_X 3
    #define POS_Y 15
    MENU_INDEX = 0
    @menuMenuDraw
        
        menuCount  = 1
        prefix$=" "
        if MENU_INDEX = 0 then prefix$="*"
        PRINTAT(POS_X,POS_Y+0,prefix$+MENU_TEXT0$)
        if MENU_TEXT1$ = "" goto @menuMainKeyLoop

        menuCount  = 2
        prefix$=" "
        if MENU_INDEX = 1 then prefix$="*"
        PRINTAT(POS_X,POS_Y+1,prefix$+MENU_TEXT1$)
        if MENU_TEXT2$ = "" goto @menuMainKeyLoop

        menuCount  = 3
        prefix$=" "
        if MENU_INDEX = 2 then prefix$="*"
        PRINTAT(POS_X,POS_Y+2,prefix$+MENU_TEXT2$)
        if MENU_TEXT3$ = "" goto @menuMainKeyLoop

        menuCount  = 4
        prefix$=" "
        if MENU_INDEX = 3 then prefix$="*"
        PRINTAT(POS_X,POS_Y+3,prefix$+MENU_TEXT3$)
        if MENU_TEXT4$ = "" goto @menuMainKeyLoop

        menuCount  = 5
        prefix$=" "
        if MENU_INDEX = 4 then prefix$="*"
        PRINTAT(POS_X,POS_Y+4,prefix$+MENU_TEXT4$)
        if MENU_TEXT5$ = "" goto @menuMainKeyLoop

        menuCount  = 6
        prefix$=" "
        if MENU_INDEX = 5 then prefix$="*"
        PRINTAT(POS_X,POS_Y+5,prefix$+MENU_TEXT5$)
        if MENU_TEXT6$ = "" goto @menuMainKeyLoop

        menuCount  = 7
        prefix$=" "
        if MENU_INDEX = 6 then prefix$="*"
        PRINTAT(POS_X,POS_Y+6,prefix$+MENU_TEXT6$)
        if MENU_TEXT7$ = "" goto @menuMainKeyLoop

        menuCount  = 8
        prefix$=" "
        if MENU_INDEX = 7 then prefix$="*"
        PRINTAT(POS_X,POS_Y+7,prefix$+MENU_TEXT7$)
        if MENU_TEXT8$ = "" goto @menuMainKeyLoop

    @menuMainKeyLoop
        get a$
        
        if a$ = "" then gosub @idleLoop: goto @menuMainKeyLoop
        if a$ = "{up}" and MENU_INDEX > 0 then MENU_INDEX = MENU_INDEX-1
        if a$ = "{down}" and MENU_INDEX < menuCount-1 then MENU_INDEX = MENU_INDEX+1
        if a$ = "{return}" then goto @menuMainSelected
        goto @menuMenuDraw
    goto @menuMainKeyLoop
    @menuMainSelected
    return

@idleLoop
    color = peek(53280)+1
    if color>255 then color=0
    poke 53280,color
    return

@mainMenu
    MENU_TEXT0$ = "menu1"
    MENU_TEXT1$ = "menu2"
    MENU_TEXT2$ = "menu3"
    MENU_TEXT3$ = "menu4"
    MENU_TEXT4$ = "menu5"
    MENU_TEXT5$ = "menu6"
    MENU_TEXT6$ = "menu7"
    MENU_TEXT7$ = "quit"
    gosub @runMenu
    print MENU_INDEX
    return

@main
    print "main loop"
    gosub @mainMenu

    

@quit
    print "{clr}"
    PRINTAT( 5, 10, "{pink}see you next time!" )
    rempoke 2049,0
    rempoke 2050,0
    rempoke 2051,0
    PRINTAT( 0,0, "load";chr$(34);"a.prg";chr$(34);"";chr$(44);"8";chr$(44);"1" )
    PRINTAT( 0,5, "run" )
