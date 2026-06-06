# MEX - My eytensions

* We use labels instead of line numbers
* Logical, arithmetic and string expressions are resolved at compile time.
* Variables of any size are allowed.
* { } can be used for scoping
* Experimental. Lokal variables from a scope are reused after the scope.
* // can be used for single line comments.
* /* and */ can be used for multi line comments.
* 

# Preprocessor

## CLI

```
preprocessor.py -s test.bas -o ./obj -l ./lib;/tmp;c:\temp
```

| parameter | Description |
| --- | --- |
| -s | The file to process. |
| -o | The folder to store processed files. |
| -l | CSV-list of paths to look for include files in. |

## Statements

The Preprocessor suports the following statements:

* #include
* #pragma
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

### pragma

```
#pragma keepindentation [true|false]
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

# Compiler

## CLI

```
cbas.py -s test.bas -o ./obj -l ./lib;/tmp;c:\temp
```

| parameter | Description |
| --- | --- |
| -s | The file to process. |
| -o | The folder to store processed files. |
| -v | Basicversion to generate |
| -t | Temp folder to store files in.|
| -l | Line number start[, step]. Default 1,1|
| -a | Address of Basic programm. Default 2049|
| -b | Beautify Basic code. Spaces are inserted to make code readable.|

# Thoughts

## Preprocessor

* What about multi line macros? Are they needed?

## cbas

1. The lexer switches between assignment(=) and eq(=)
   The firat = in a line is assumed as a assignment.
   All following = are handles as comparators.
   IF and FOR switches to comparator mode
   : then and TO switches to assignment mode.
2. The code builder casts function parameters to target types.
3. Values of castTypes should come from cbas.config
4. Values from skipOpen should come from cbas.config
5. BasicBuilder.getHandler() should come from config.
6. Petscii should be a static class
7. 

## Passes

0. Preprocessor
   1. Filecleaner
      1. Concatenate lines.( Lines ending with underscores get the next line concatenated.)
      2. Remove comments.
      3. Clean whitespaces.
      4. Remove empty lines.
   2. Execute Directives.
1. Lexer
   1. Tokenize Source code
   2. Add variables to symbol table.
2. TokenchainOptimizer
3. Parser
   Are tags at PrimaryExpression nedded?
4. Ast-Optimizers
   1. Shemantic error checking
   2. Resolve arithmetic expressions
   3. Resolve logical expressions
   4. Resolve Stringarithmetic
5. codeBuilders
   1. Generate code lines from Ast.
      Tokenizer manages generation of basic or prg
   2. Resolve Symbols
   3. Concatenate lines. (Combines  commants seperated by :)
   4. Cleanup Code.
      1. Remove scope definitions.
6. Write binary file.

```

``````

