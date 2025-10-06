"""Tests unitaires pour les classes regex_ast."""

import pytest
from baobab_automata.automata.finite.regex_ast import ASTNode, NodeType


@pytest.mark.unit
class TestNodeType:
    """Tests pour l'énumération NodeType."""

    def test_node_type_enumeration(self):
        """Test que tous les types de nœuds sont définis."""
        expected_types = {
            "LITERAL", "UNION", "CONCATENATION", "KLEENE_STAR", 
            "KLEENE_PLUS", "OPTIONAL", "GROUP", "EMPTY", "EPSILON"
        }
        actual_types = {node_type.name for node_type in NodeType}
        assert actual_types == expected_types

    def test_node_type_values(self):
        """Test les valeurs des types de nœuds."""
        assert NodeType.LITERAL.value == "literal"
        assert NodeType.UNION.value == "union"
        assert NodeType.CONCATENATION.value == "concatenation"
        assert NodeType.KLEENE_STAR.value == "kleene_star"
        assert NodeType.KLEENE_PLUS.value == "kleene_plus"
        assert NodeType.OPTIONAL.value == "optional"
        assert NodeType.GROUP.value == "group"
        assert NodeType.EMPTY.value == "empty"
        assert NodeType.EPSILON.value == "epsilon"

    def test_node_type_count(self):
        """Test le nombre de types de nœuds."""
        assert len(NodeType) == 9


@pytest.mark.unit
class TestASTNode:
    """Tests pour la classe ASTNode."""

    def test_ast_node_creation_basic(self):
        """Test la création basique d'un nœud AST."""
        node = ASTNode(NodeType.LITERAL, "a")
        assert node.type == NodeType.LITERAL
        assert node.value == "a"
        assert node.children == []

    def test_ast_node_creation_with_children(self):
        """Test la création d'un nœud AST avec des enfants."""
        child1 = ASTNode(NodeType.LITERAL, "a")
        child2 = ASTNode(NodeType.LITERAL, "b")
        node = ASTNode(NodeType.UNION, children=[child1, child2])
        
        assert node.type == NodeType.UNION
        assert node.value is None
        assert len(node.children) == 2
        assert node.children[0] == child1
        assert node.children[1] == child2

    def test_ast_node_creation_without_children(self):
        """Test la création d'un nœud AST sans enfants."""
        node = ASTNode(NodeType.LITERAL, "a", children=None)
        assert node.children == []

    def test_ast_node_repr_with_value(self):
        """Test la représentation string d'un nœud avec valeur."""
        node = ASTNode(NodeType.LITERAL, "a")
        repr_str = repr(node)
        assert "ASTNode" in repr_str
        assert "literal" in repr_str
        assert "a" in repr_str
        assert "0 children" in repr_str

    def test_ast_node_repr_without_value(self):
        """Test la représentation string d'un nœud sans valeur."""
        child = ASTNode(NodeType.LITERAL, "a")
        node = ASTNode(NodeType.UNION, children=[child])
        repr_str = repr(node)
        assert "ASTNode" in repr_str
        assert "union" in repr_str
        assert "1 children" in repr_str

    def test_ast_node_equality_same(self):
        """Test l'égalité de deux nœuds identiques."""
        node1 = ASTNode(NodeType.LITERAL, "a")
        node2 = ASTNode(NodeType.LITERAL, "a")
        assert node1 == node2

    def test_ast_node_equality_different_type(self):
        """Test l'égalité de deux nœuds de types différents."""
        node1 = ASTNode(NodeType.LITERAL, "a")
        node2 = ASTNode(NodeType.UNION, "a")
        assert node1 != node2

    def test_ast_node_equality_different_value(self):
        """Test l'égalité de deux nœuds avec des valeurs différentes."""
        node1 = ASTNode(NodeType.LITERAL, "a")
        node2 = ASTNode(NodeType.LITERAL, "b")
        assert node1 != node2

    def test_ast_node_equality_different_children(self):
        """Test l'égalité de deux nœuds avec des enfants différents."""
        child1 = ASTNode(NodeType.LITERAL, "a")
        child2 = ASTNode(NodeType.LITERAL, "b")
        node1 = ASTNode(NodeType.UNION, children=[child1])
        node2 = ASTNode(NodeType.UNION, children=[child2])
        assert node1 != node2

    def test_ast_node_equality_with_non_ast_node(self):
        """Test l'égalité avec un objet non-ASTNode."""
        node = ASTNode(NodeType.LITERAL, "a")
        assert node != "not a node"
        assert node != 42
        assert node != None

    def test_ast_node_hash(self):
        """Test le hash d'un nœud AST."""
        node1 = ASTNode(NodeType.LITERAL, "a")
        node2 = ASTNode(NodeType.LITERAL, "a")
        node3 = ASTNode(NodeType.LITERAL, "b")
        
        assert hash(node1) == hash(node2)
        assert hash(node1) != hash(node3)

    def test_ast_node_hash_with_children(self):
        """Test le hash d'un nœud AST avec des enfants."""
        child1 = ASTNode(NodeType.LITERAL, "a")
        child2 = ASTNode(NodeType.LITERAL, "b")
        node1 = ASTNode(NodeType.UNION, children=[child1, child2])
        node2 = ASTNode(NodeType.UNION, children=[child1, child2])
        node3 = ASTNode(NodeType.UNION, children=[child2, child1])
        
        assert hash(node1) == hash(node2)
        assert hash(node1) != hash(node3)

    def test_ast_node_is_leaf_true(self):
        """Test qu'un nœud sans enfants est une feuille."""
        node = ASTNode(NodeType.LITERAL, "a")
        assert node.is_leaf() is True

    def test_ast_node_is_leaf_false(self):
        """Test qu'un nœud avec des enfants n'est pas une feuille."""
        child = ASTNode(NodeType.LITERAL, "a")
        node = ASTNode(NodeType.UNION, children=[child])
        assert node.is_leaf() is False

    def test_ast_node_is_unary_true(self):
        """Test qu'un nœud unaire est identifié correctement."""
        node1 = ASTNode(NodeType.KLEENE_STAR)
        node2 = ASTNode(NodeType.KLEENE_PLUS)
        node3 = ASTNode(NodeType.OPTIONAL)
        
        assert node1.is_unary() is True
        assert node2.is_unary() is True
        assert node3.is_unary() is True

    def test_ast_node_is_unary_false(self):
        """Test qu'un nœud non-unaire n'est pas identifié comme unaire."""
        node1 = ASTNode(NodeType.LITERAL, "a")
        node2 = ASTNode(NodeType.UNION)
        node3 = ASTNode(NodeType.CONCATENATION)
        node4 = ASTNode(NodeType.GROUP)
        
        assert node1.is_unary() is False
        assert node2.is_unary() is False
        assert node3.is_unary() is False
        assert node4.is_unary() is False

    def test_ast_node_is_binary_true(self):
        """Test qu'un nœud binaire est identifié correctement."""
        node1 = ASTNode(NodeType.UNION)
        node2 = ASTNode(NodeType.CONCATENATION)
        
        assert node1.is_binary() is True
        assert node2.is_binary() is True

    def test_ast_node_is_binary_false(self):
        """Test qu'un nœud non-binaire n'est pas identifié comme binaire."""
        node1 = ASTNode(NodeType.LITERAL, "a")
        node2 = ASTNode(NodeType.KLEENE_STAR)
        node3 = ASTNode(NodeType.GROUP)
        
        assert node1.is_binary() is False
        assert node2.is_binary() is False
        assert node3.is_binary() is False

    def test_ast_node_is_terminal_true(self):
        """Test qu'un nœud terminal est identifié correctement."""
        node1 = ASTNode(NodeType.LITERAL, "a")
        node2 = ASTNode(NodeType.EPSILON)
        node3 = ASTNode(NodeType.EMPTY)
        
        assert node1.is_terminal() is True
        assert node2.is_terminal() is True
        assert node3.is_terminal() is True

    def test_ast_node_is_terminal_false(self):
        """Test qu'un nœud non-terminal n'est pas identifié comme terminal."""
        node1 = ASTNode(NodeType.UNION)
        node2 = ASTNode(NodeType.CONCATENATION)
        node3 = ASTNode(NodeType.KLEENE_STAR)
        node4 = ASTNode(NodeType.GROUP)
        
        assert node1.is_terminal() is False
        assert node2.is_terminal() is False
        assert node3.is_terminal() is False
        assert node4.is_terminal() is False

    def test_ast_node_add_child(self):
        """Test l'ajout d'un enfant à un nœud."""
        node = ASTNode(NodeType.UNION)
        child = ASTNode(NodeType.LITERAL, "a")
        
        assert len(node.children) == 0
        node.add_child(child)
        assert len(node.children) == 1
        assert node.children[0] == child

    def test_ast_node_add_multiple_children(self):
        """Test l'ajout de plusieurs enfants à un nœud."""
        node = ASTNode(NodeType.UNION)
        child1 = ASTNode(NodeType.LITERAL, "a")
        child2 = ASTNode(NodeType.LITERAL, "b")
        
        node.add_child(child1)
        node.add_child(child2)
        
        assert len(node.children) == 2
        assert node.children[0] == child1
        assert node.children[1] == child2

    def test_ast_node_get_child_valid_index(self):
        """Test la récupération d'un enfant avec un index valide."""
        child1 = ASTNode(NodeType.LITERAL, "a")
        child2 = ASTNode(NodeType.LITERAL, "b")
        node = ASTNode(NodeType.UNION, children=[child1, child2])
        
        assert node.get_child(0) == child1
        assert node.get_child(1) == child2

    def test_ast_node_get_child_invalid_index_negative(self):
        """Test la récupération d'un enfant avec un index négatif."""
        child = ASTNode(NodeType.LITERAL, "a")
        node = ASTNode(NodeType.UNION, children=[child])
        
        assert node.get_child(-1) is None

    def test_ast_node_get_child_invalid_index_too_large(self):
        """Test la récupération d'un enfant avec un index trop grand."""
        child = ASTNode(NodeType.LITERAL, "a")
        node = ASTNode(NodeType.UNION, children=[child])
        
        assert node.get_child(1) is None
        assert node.get_child(10) is None

    def test_ast_node_to_string_literal(self):
        """Test la conversion en string d'un nœud littéral."""
        node = ASTNode(NodeType.LITERAL, "a")
        assert node.to_string() == "a"

    def test_ast_node_to_string_literal_empty_value(self):
        """Test la conversion en string d'un nœud littéral avec valeur vide."""
        node = ASTNode(NodeType.LITERAL, "")
        assert node.to_string() == ""

    def test_ast_node_to_string_literal_none_value(self):
        """Test la conversion en string d'un nœud littéral avec valeur None."""
        node = ASTNode(NodeType.LITERAL, None)
        assert node.to_string() == ""

    def test_ast_node_to_string_epsilon(self):
        """Test la conversion en string d'un nœud epsilon."""
        node = ASTNode(NodeType.EPSILON)
        assert node.to_string() == "ε"

    def test_ast_node_to_string_empty(self):
        """Test la conversion en string d'un nœud vide."""
        node = ASTNode(NodeType.EMPTY)
        assert node.to_string() == "∅"

    def test_ast_node_to_string_kleene_star(self):
        """Test la conversion en string d'un nœud étoile de Kleene."""
        child = ASTNode(NodeType.LITERAL, "a")
        node = ASTNode(NodeType.KLEENE_STAR, children=[child])
        assert node.to_string() == "(a)*"

    def test_ast_node_to_string_kleene_star_no_children(self):
        """Test la conversion en string d'un nœud étoile de Kleene sans enfants."""
        node = ASTNode(NodeType.KLEENE_STAR)
        assert node.to_string() == ""

    def test_ast_node_to_string_kleene_plus(self):
        """Test la conversion en string d'un nœud plus de Kleene."""
        child = ASTNode(NodeType.LITERAL, "a")
        node = ASTNode(NodeType.KLEENE_PLUS, children=[child])
        assert node.to_string() == "(a)+"

    def test_ast_node_to_string_kleene_plus_no_children(self):
        """Test la conversion en string d'un nœud plus de Kleene sans enfants."""
        node = ASTNode(NodeType.KLEENE_PLUS)
        assert node.to_string() == ""

    def test_ast_node_to_string_optional(self):
        """Test la conversion en string d'un nœud optionnel."""
        child = ASTNode(NodeType.LITERAL, "a")
        node = ASTNode(NodeType.OPTIONAL, children=[child])
        assert node.to_string() == "(a)?"

    def test_ast_node_to_string_optional_no_children(self):
        """Test la conversion en string d'un nœud optionnel sans enfants."""
        node = ASTNode(NodeType.OPTIONAL)
        assert node.to_string() == ""

    def test_ast_node_to_string_union(self):
        """Test la conversion en string d'un nœud union."""
        child1 = ASTNode(NodeType.LITERAL, "a")
        child2 = ASTNode(NodeType.LITERAL, "b")
        node = ASTNode(NodeType.UNION, children=[child1, child2])
        assert node.to_string() == "(a|b)"

    def test_ast_node_to_string_union_insufficient_children(self):
        """Test la conversion en string d'un nœud union avec moins de 2 enfants."""
        child = ASTNode(NodeType.LITERAL, "a")
        node = ASTNode(NodeType.UNION, children=[child])
        assert node.to_string() == ""

    def test_ast_node_to_string_concatenation(self):
        """Test la conversion en string d'un nœud concaténation."""
        child1 = ASTNode(NodeType.LITERAL, "a")
        child2 = ASTNode(NodeType.LITERAL, "b")
        node = ASTNode(NodeType.CONCATENATION, children=[child1, child2])
        assert node.to_string() == "ab"

    def test_ast_node_to_string_concatenation_insufficient_children(self):
        """Test la conversion en string d'un nœud concaténation avec moins de 2 enfants."""
        child = ASTNode(NodeType.LITERAL, "a")
        node = ASTNode(NodeType.CONCATENATION, children=[child])
        assert node.to_string() == ""

    def test_ast_node_to_string_group(self):
        """Test la conversion en string d'un nœud groupe."""
        child = ASTNode(NodeType.LITERAL, "a")
        node = ASTNode(NodeType.GROUP, children=[child])
        assert node.to_string() == "(a)"

    def test_ast_node_to_string_group_no_children(self):
        """Test la conversion en string d'un nœud groupe sans enfants."""
        node = ASTNode(NodeType.GROUP)
        assert node.to_string() == ""

    def test_ast_node_to_string_complex_expression(self):
        """Test la conversion en string d'une expression complexe."""
        # Expression: (a|b)*c
        a = ASTNode(NodeType.LITERAL, "a")
        b = ASTNode(NodeType.LITERAL, "b")
        union = ASTNode(NodeType.UNION, children=[a, b])
        kleene = ASTNode(NodeType.KLEENE_STAR, children=[union])
        c = ASTNode(NodeType.LITERAL, "c")
        concat = ASTNode(NodeType.CONCATENATION, children=[kleene, c])
        
        assert concat.to_string() == "((a|b))*c"

    def test_ast_node_to_string_nested_groups(self):
        """Test la conversion en string d'expressions avec groupes imbriqués."""
        # Expression: ((a|b)|c)
        a = ASTNode(NodeType.LITERAL, "a")
        b = ASTNode(NodeType.LITERAL, "b")
        inner_union = ASTNode(NodeType.UNION, children=[a, b])
        inner_group = ASTNode(NodeType.GROUP, children=[inner_union])
        c = ASTNode(NodeType.LITERAL, "c")
        outer_union = ASTNode(NodeType.UNION, children=[inner_group, c])
        outer_group = ASTNode(NodeType.GROUP, children=[outer_union])
        
        assert outer_group.to_string() == "((((a|b))|c))"

    def test_ast_node_to_string_unknown_type(self):
        """Test la conversion en string d'un type de nœud inconnu."""
        # Créer un nœud avec un type qui ne correspond à aucun cas
        node = ASTNode(NodeType.LITERAL)  # Type terminal mais sans valeur
        # Simuler un type inconnu en modifiant le type après création
        node.type = "unknown_type"
        assert node.to_string() == ""

    def test_ast_node_immutability_after_creation(self):
        """Test que les propriétés de base ne changent pas après création."""
        node = ASTNode(NodeType.LITERAL, "a")
        original_type = node.type
        original_value = node.value
        original_children = node.children.copy()
        
        # Les propriétés ne devraient pas changer
        assert node.type == original_type
        assert node.value == original_value
        assert node.children == original_children

    def test_ast_node_children_mutation(self):
        """Test que les enfants peuvent être modifiés après création."""
        node = ASTNode(NodeType.UNION)
        child1 = ASTNode(NodeType.LITERAL, "a")
        child2 = ASTNode(NodeType.LITERAL, "b")
        
        node.add_child(child1)
        assert len(node.children) == 1
        
        node.add_child(child2)
        assert len(node.children) == 2
        
        # Modifier directement la liste des enfants
        node.children.append(ASTNode(NodeType.LITERAL, "c"))
        assert len(node.children) == 3

    def test_ast_node_deep_copy_behavior(self):
        """Test le comportement de copie profonde des nœuds."""
        child = ASTNode(NodeType.LITERAL, "a")
        node1 = ASTNode(NodeType.UNION, children=[child])
        node2 = ASTNode(NodeType.UNION, children=[child])
        
        # Les deux nœuds partagent le même enfant
        assert node1.children[0] is node2.children[0]
        
        # Modifier l'enfant affecte les deux nœuds
        child.value = "b"
        assert node1.children[0].value == "b"
        assert node2.children[0].value == "b"