# Preprocessor

## CLI

```
preprocessor.py -i test.bas -o ./obj -l ./lib;/tmp;c:\temp
```

| col1 | col2 |
| --- | --- |
| -i --inputfile | The file to process |
| -o --outputfolder | The folder to store processed files. |
| -l --libfolders | CSV-list of paths to look for include files in. |


## Statements

The Preprocessor suports the following statements:

* #include
* #config
* #define
* #undefine
* #ifdef
* #ifndef
* #else
* #endif
* #if

### include

```
#include "filename"
```

Replaces the include statement with the content of the given file.

### config

```
#config keepindentation [true|false]
```

* keepindentation - Keeps the indentation of the #include statement for the inserted file content.

### define

```
#define NAME 
#define NAME 4
#define sum(%0,%1) (%0+%1)

a = sum(5,4)
```

### undefine

```
#undefine NAME
```

### ifdef

```
#defien NAME
#ifdev NAME
...
#endif
```

### ifndev

```
#ifndev NAME
...
#endif
```

### if

```
#define A 4
#if A = 4
...
#endif
```

### else

```
#define NAME
#ifdev NAME
...
#else
...
#endif
```

### endif

```
#define A
ifdef A
...
#endif
```

.

