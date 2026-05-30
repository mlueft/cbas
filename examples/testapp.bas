

goto @main


@runMenu
    print "{clr}"
    MENU_INDEX = 0
    @menuMenuDraw
        
        menuCount  = 1
        prefix$=" "
        if MENU_INDEX = 0 then prefix$="*"
        POKE781,15+0:POKE782,3:SYS(65520):PRINT prefix$+MENU_TEXT0$
        if MENU_TEXT1$ = "" goto @menuMainKeyLoop

        menuCount  = 2
        prefix$=" "
        if MENU_INDEX = 1 then prefix$="*"
        POKE781,15+1:POKE782,3:SYS(65520):PRINT prefix$+MENU_TEXT1$
        if MENU_TEXT2$ = "" goto @menuMainKeyLoop

        menuCount  = 3
        prefix$=" "
        if MENU_INDEX = 2 then prefix$="*"
        POKE781,15+2:POKE782,3:SYS(65520):PRINT prefix$+MENU_TEXT2$
        if MENU_TEXT3$ = "" goto @menuMainKeyLoop

        menuCount  = 4
        prefix$=" "
        if MENU_INDEX = 3 then prefix$="*"
        POKE781,15+3:POKE782,3:SYS(65520):PRINT prefix$+MENU_TEXT3$
        if MENU_TEXT4$ = "" goto @menuMainKeyLoop

        menuCount  = 5
        prefix$=" "
        if MENU_INDEX = 4 then prefix$="*"
        POKE781,15+4:POKE782,3:SYS(65520):PRINT prefix$+MENU_TEXT4$
        if MENU_TEXT5$ = "" goto @menuMainKeyLoop

        menuCount  = 6
        prefix$=" "
        if MENU_INDEX = 5 then prefix$="*"
        POKE781,15+5:POKE782,3:SYS(65520):PRINT prefix$+MENU_TEXT5$
        if MENU_TEXT6$ = "" goto @menuMainKeyLoop

        menuCount  = 7
        prefix$=" "
        if MENU_INDEX = 6 then prefix$="*"
        POKE781,15+6:POKE782,3:SYS(65520):PRINT prefix$+MENU_TEXT6$
        if MENU_TEXT7$ = "" goto @menuMainKeyLoop

        menuCount  = 8
        prefix$=" "
        if MENU_INDEX = 7 then prefix$="*"
        POKE781,15+7:POKE782,3:SYS(65520):PRINT prefix$+MENU_TEXT7$
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
    POKE781, 10:POKE782, 5:SYS(65520):PRINT  "{pink}see you next time!" 
    rempoke 2049,0
    rempoke 2050,0
    rempoke 2051,0
    POKE781,0:POKE782, 0:SYS(65520):PRINT  "load";chr$(34);"a.prg";chr$(34);"";chr$(44);"8";chr$(44);"1" 
    POKE781,5:POKE782, 0:SYS(65520):PRINT  "run" 
