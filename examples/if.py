========================= IF

if a then{
    print "a"
}

if not (a) then goto @endif
    print "a"
@endif

===================== IF ELSE

if a then{
    print "a"
}else{
    print "else"
}

if not(a) then goto @else
    print "a"
    goto @endif
@else
    print "else"
@endif

==================== IF ELIF

if a then{
    print "a"
}elif b then{
    print "b"
}

if not(a) then goto @b
    print "a"
    goto @endif
@b
if not(b) then goto @endif
    print "b"
@endif

================ IF ELIF ELSE

if a then{
    print "a"
}elif b then{
    print "b"
}else{
    print "else"
}

if not(a) then goto @b
    print "a"
    goto @endif
@b
if not(b) then goto @else
    print "b"
    goto @endif
@else
    print "else"
@endif
