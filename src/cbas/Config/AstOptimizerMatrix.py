import cbas.DataStructures.TraverseMode
import cbas.AstOptimizer.AstOptimizer

TraverseMode              = cbas.DataStructures.TraverseMode.TraverseMode
ArithmeticOptimizer       = cbas.AstOptimizer.AstOptimizer.ArithmeticOptimizer
SyntaxCheckerV2           = cbas.AstOptimizer.AstOptimizer.SyntaxCheckerV2
LogicOptimizer            = cbas.AstOptimizer.AstOptimizer.LogicOptimizer

class AstOptimizerMatrix():

    Parameters = [
        # AR
        {
            "name": "",
            "description":"",
        },
        # PP
        {
            "name": "",
            "description":"",
        },
        # V2
        {
            "name": "",
            "description":"",
        },
        # v3.5
        {
            "name": "",
            "description":"",
        },
        # v3.6
        {
            "name": "",
            "description":"",
        },
        # v4
        {
            "name": "",
            "description":"",
        },
        # v4+
        {
            "name": "",
            "description":"",
        },
        # v7
        {
            "name": "",
            "description":"",
        },
        # v10
        {
            "name": "",
            "description":"",
        },
        
    ]

    TokensSemanticcheck = {
        "semanticchecker_v2" : { "order":0, "instance": SyntaxCheckerV2(),     "direction":TraverseMode.OUTLINE  }
    }

    Matrixsemanticcheck = {
        # ------------------------------------------------------------------
        #                         AR    PP    V2    v3.5  v3.6  v4    v4+   v7    v10
        # ------------------------------------------------------------------
        "semanticchecker_v2":    [ 0,    0,    1,    0,    0,    0,    0,    0,    0    ],
    }

    TokensPostParser = {
        "arithmetic"         : { "order":1, "instance": ArithmeticOptimizer(), "direction":TraverseMode.BOTTOM_UP },
        "logical"            : { "order":2, "instance": LogicOptimizer(),      "direction":TraverseMode.BOTTOM_UP }
    }

    MatrixPostParser = {
        # ------------------------------------------------------------------
        #                         AR    PP    V2    v3.5  v3.6  v4    v4+   v7    v10
        # ------------------------------------------------------------------
        "arithmetic":            [ 1,    1,    1,    1,    1,    1,    1,    1,    1    ],
        "logical":               [ 0,    1,    1,    1,    1,    1,    1,    1,    1    ],

    }