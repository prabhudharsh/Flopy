import ast
from graphviz import Digraph

class CodeToFlowchart(ast.NodeVisitor):
    def __init__(self):
        self.graph = Digraph(format='svg')
        self.node_count = 0

    def new_node(self, label, shape="rectangle"):
        node_name = f'node{self.node_count}'
        self.graph.node(node_name, label, shape=shape)
        self.node_count += 1
        return node_name

    def connect(self, from_node, to_node, label=""):
        self.graph.edge(from_node, to_node, label)

    def visit_FunctionDef(self, node, prev_node=None):
        start_node = self.new_node("Start", "oval")
        func_node = self.new_node(f"Function: {node.name}", "rectangle")
        self.connect(start_node, func_node)
        prev_node = func_node

        for stmt in node.body:
            prev_node = self.visit(stmt, prev_node)

        end_node = self.new_node("End", "oval")
        self.connect(prev_node, end_node)
        return end_node

    def visit_If(self, node, prev_node):
        cond_node = self.new_node(f"If: {ast.unparse(node.test)}", "diamond")
        self.connect(prev_node, cond_node)

        true_branch = cond_node
        for stmt in node.body:
            true_branch = self.visit(stmt, true_branch)

        if node.orelse:
            false_branch = cond_node
            for stmt in node.orelse:
                false_branch = self.visit(stmt, false_branch)
        else:
            false_branch = self.new_node("Pass", "rectangle")

        join_node = self.new_node("", "point")
        self.connect(cond_node, true_branch, label="True")
        self.connect(cond_node, false_branch, label="False")
        self.connect(true_branch, join_node)
        self.connect(false_branch, join_node)
        return join_node

    def visit_For(self, node, prev_node):
        label = f"For: {ast.unparse(node.target)} in {ast.unparse(node.iter)}"
        loop_check = self.new_node(label, "diamond")
        self.connect(prev_node, loop_check)

        loop_entry = loop_check
        for stmt in node.body:
            loop_entry = self.visit(stmt, loop_entry)

        loop_join = self.new_node("Loop Join", "point")
        self.connect(loop_entry, loop_check, label="loop")

        after_loop = self.new_node("After Loop", "rectangle")
        self.connect(loop_check, after_loop, label="exit",)
        return after_loop

    def visit_Assign(self, node, prev_node):
        assign_node = self.new_node(ast.unparse(node), "rectangle")
        self.connect(prev_node, assign_node)
        return assign_node

    def visit_Expr(self, node, prev_node):
        expr_node = self.new_node(ast.unparse(node), "parallelogram")
        self.connect(prev_node, expr_node)
        return expr_node

    def visit_Return(self, node, prev_node):
        ret_node = self.new_node(f"Return: {ast.unparse(node.value)}", "rectangle")
        self.connect(prev_node, ret_node)
        return ret_node

    def visit(self, node, prev_node=None):
        method = f'visit_{node.__class__.__name__}'
        visitor = getattr(self, method, None)
        if visitor:
            return visitor(node, prev_node)
        return prev_node

    def generate(self, code):
        tree = ast.parse(code)
        for stmt in tree.body:
            if isinstance(stmt, ast.FunctionDef):
                self.visit(stmt)
        return self.graph

