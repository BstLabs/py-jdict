import ast
from typing import Any, Final

jdict: str = "jdict"  # WPS226 Found string literal over-use


class JdictTransformer(ast.NodeTransformer):
    """
    The visitor class of the node that traverses,
    the abstract syntax tree and calls the visitor function
    for each node found. Inherits from class NodeTransformer
    """

    def visit_Module(self, node: ast.AST) -> Any:
        """
        Method imports jdict module into ast
        :param node: CodeType
        :return: node
        """
        visited_node = self.generic_visit(node)
        import_node = ast.ImportFrom(
            module=jdict, names=[ast.alias(name=jdict)], level=0
        )
        visited_node.body.insert(0, import_node)
        return visited_node

    def visit_Name(self, node: ast.Name) -> Any:
        if node.id == "dict":
            node.id = jdict
        return self.generic_visit(node)

    def visit_Dict(self, node: ast.AST) -> Any:
        """
        Method goes into the dict node and modifies it to jdict
        :param node:
        :return:
        """
        node = self.generic_visit(node)
        name_node = ast.Name(id="jdict", ctx=ast.Load())
        return ast.Call(func=name_node, args=[node], keywords=[])


def transform(src: str) -> Any:
    """
    Transforms the given source to use jdict to replace built in structures.
    :param src:  str
    :return: new_tree
    """
    tree: Final = ast.parse(src)
    transformer: Final = JdictTransformer()
    new_tree = transformer.visit(tree)
    ast.fix_missing_locations(new_tree)
    return new_tree
