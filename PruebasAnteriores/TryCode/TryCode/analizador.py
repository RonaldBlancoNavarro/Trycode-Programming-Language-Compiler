from TryCode import token as tk
from TryCode import error as er
from TryCode import nodo as nd


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()

    def advance(
        self,
    ):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok

    def parse(self):
        res = self.expr()
        if not res.error and self.current_tok.type != tk.TT_EOF:
            return res.failure(
                er.self.current_tok.pos_start,
                self.current_tok.pos_end,
                "Expected '+', '-', '*' or '/'",
            )
        return res

    ###################################

    def factor(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (tk.TT_PLUS, tk.TT_MINUS):
            res.register(self.advance())
            factor = res.register(self.factor())
            if res.error:
                return res
            return res.success(nd.UnaryOpNode(tok, factor))

        elif tok.type in (tk.TT_INT, tk.TT_FLOAT):
            res.register(self.advance())
            return res.success(nd.NumberNode(tok))

        elif tok.type == tk.TT_LPAREN:
            res.register(self.advance())
            expr = res.register(self.expr())
            if res.error:
                return res
            if self.current_tok.type == tk.TT_RPAREN:
                res.register(self.advance())
                return res.success(expr)
            else:
                return res.failure(
                    er.InvalidSyntaxError(
                        self.current_tok.pos_start,
                        self.current_tok.pos_end,
                        "Expected ')'",
                    )
                )

        return res.failure(
            er.InvalidSyntaxError(tok.pos_start, tok.pos_end, "Expected int or float")
        )

    def term(self):
        return self.bin_op(self.factor, (tk.TT_MUL, tk.TT_DIV))

    def expr(self):
        return self.bin_op(self.term, (tk.TT_PLUS, tk.TT_MINUS))

    ###################################

    def bin_op(self, func, ops):
        res = ParseResult()
        left = res.register(func())
        if res.error:
            return res

        while self.current_tok.type in ops:
            op_tok = self.current_tok
            res.register(self.advance())
            right = res.register(func())
            if res.error:
                return res
            left = nd.BinOpNode(left, op_tok, right)

        return res.success(left)


class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None

    def register(self, res):
        if isinstance(res, ParseResult):
            if res.error:
                self.error = res.error
            return res.node

        return res

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        self.error = error
        return self