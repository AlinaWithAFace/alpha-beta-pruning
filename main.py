import collections
import anytree
import queue
from anytree import RenderTree
from anytree.exporter import DotExporter
import graphviz
import subprocess
import math
import inf


# import heapq


class AlphaBetaNode(anytree.Node):
    def __init__(self, value, name, **kwargs):
        super().__init__(name, **kwargs)
        self.is_max_node = None  # type: bool
        # True for alpha/max, False for beta/min
        self.value = value  # type: int
        self.alpha_value = None  # type: int
        self.beta_value = None  # type: int

    def __lt__(self, other):
        # print("Comparing...")
        # print(self)
        # print(other)
        if other is not None:
            return self.value < other.value
        else:
            return self


def initialize_tree(input_string):
    """
    Build the tree, quick and dirty but it gets the job done
    """
    # print("building tree...\n\n")
    input_string = input_string.split()

    root = AlphaBetaNode(None, "root")

    root.alpha_value = -math.inf
    root.beta_value = math.inf
    root.is_max_node = True

    child_a = AlphaBetaNode(None, "A", parent=root)
    child_b = AlphaBetaNode(None, "B", parent=root)
    child_c = AlphaBetaNode(None, "C", parent=root)

    child_aa = AlphaBetaNode(None, "AA", parent=child_a)
    child_ab = AlphaBetaNode(None, "AB", parent=child_a)

    child_ba = AlphaBetaNode(None, "BA", parent=child_b)
    child_bb = AlphaBetaNode(None, "BB", parent=child_b)

    child_ca = AlphaBetaNode(None, "CA", parent=child_c)
    child_cb = AlphaBetaNode(None, "CB", parent=child_c)

    child_0 = AlphaBetaNode(int(input_string[0]), input_string[0], parent=child_aa)
    child_1 = AlphaBetaNode(int(input_string[1]), input_string[1], parent=child_aa)

    child_2 = AlphaBetaNode(int(input_string[2]), input_string[2], parent=child_ab)
    child_3 = AlphaBetaNode(int(input_string[3]), input_string[3], parent=child_ab)

    child_4 = AlphaBetaNode(int(input_string[4]), input_string[4], parent=child_ba)
    child_5 = AlphaBetaNode(int(input_string[5]), input_string[5], parent=child_ba)

    child_6 = AlphaBetaNode(int(input_string[6]), input_string[6], parent=child_bb)
    child_7 = AlphaBetaNode(int(input_string[7]), input_string[7], parent=child_bb)

    child_8 = AlphaBetaNode(int(input_string[8]), input_string[8], parent=child_ca)
    child_9 = AlphaBetaNode(int(input_string[9]), input_string[9], parent=child_ca)

    child_10 = AlphaBetaNode(int(input_string[10]), input_string[10], parent=child_cb)
    child_11 = AlphaBetaNode(int(input_string[11]), input_string[11], parent=child_cb)

    # print("Finished Skeleton:\n")
    # print(RenderTree(root))
    # print("\n\n")

    return root


def evaluate_node(node, maximizer_queue, minimizer_queue):
    if node is not None:
        print("[Node {}] [{}] Start: [{}] | [{}] [{}]".format(
            node.name, node.is_max_node, node.value, node.alpha_value, node.beta_value))
        # print("[Node {}] [{}] START [value {}] [alpha {}] [beta {}]".format(
        #     parent.name, parent.is_max_node, parent.value, parent.alpha_value, parent.beta_value))
        # parent = parent  # type: AlphaBetaNode
        children = node.children

        for child in children:  # type: AlphaBetaNode

            # set the child to max or min mode
            if node.is_max_node:
                #  if this is a max node, set the child to a min node
                child.is_max_node = False
            else:
                #  if this is a min node, set the child to a max node
                child.is_max_node = True

            #  if the child has no alpha or beta values, inherit some
            if child.alpha_value is None:
                child.alpha_value = node.alpha_value

            if child.beta_value is None:
                child.beta_value = node.beta_value

            # if the child has no value, check its children for values
            if child.value is None:
                # (evaluate_node(child))
                # heapq.heappush(maximizer_queue, (child.beta_value, child))
                # heapq.heappush(minimizer_queue, (child.alpha_value, child))
                maximizer_queue.append(child)
                minimizer_queue.append(child)
            elif node.is_max_node:
                # if the child's alpha is greater than the parent's alpha, inherit it
                print("node's alpha {} < {} child ".format(node.alpha_value, child.value))
                if node.alpha_value < child.value:
                    node.alpha_value = child.value

            elif not node.is_max_node:
                print("node's beta {} > {} child".format(node.beta_value, child.value))
                # if the child's alpha is less than the parent's alpha, inherit it
                if node.beta_value > child.value:
                    node.beta_value = child.value
            else:
                print("I don't know how but they found me")

            print("[Node {}] [{}] Checkpoint: [{}] | [{}] [{}]".format(
                node.name, node.is_max_node, node.value, node.alpha_value, node.beta_value))

            # copy value from alpha or beta based on whether its a max or min node
            if node.is_max_node:
                # print("Node is max, setting value {} from alpha {} (beta: {})".format(
                #     parent.value, parent.alpha_value, parent.beta_value))
                node.value = node.alpha_value
                if node.parent:
                    node.parent.beta_value = node.value
            elif not node.is_max_node:
                # print("Node is min, setting value {} from beta {} (alpha: {})".format(
                #     parent.value, parent.beta_value, parent.alpha_value))
                node.value = node.beta_value
                if node.parent:
                    node.parent.alpha_value = node.value

            if node.alpha_value >= node.beta_value:
                print("alpha >= beta, prune?")
                node.children = None

            # if node.alpha_value < node.beta_value:
            #     print("beta < alpha, riot")

            print("[Node {}] [{}] End: [{}] | [{}] [{}]".format(
                node.name, node.is_max_node, node.value, node.alpha_value, node.beta_value))

    return node


def choose_next_node(alpha, maximizer_queue, minimizer_queue):
    """
    :param maximizer_queue:
    :param minimizer_queue:
    :param alpha: True for alpha/max, False for beta/min
    :return:
    """
    # print("chosing next node")
    # print(alpha)
    # print(maximizer_queue)
    # print(minimizer_queue)
    # print("{} | {} | {}".format(alpha, maximizer_queue, minimizer_queue))
    print("\n\n")
    node = None
    if alpha:
        if not maximizer_queue:
            print("maximizer empty")
            return
        node = maximizer_queue.pop()
        print("pulled from max:")
    else:
        if not minimizer_queue:
            print("minimizer empty")
            return
        node = minimizer_queue.pop()
        print("pulled from min:")

    print(node)
    print("\n")

    evaluate_node(node, maximizer_queue, minimizer_queue)

    # print("Adding children to heaps...")
    # children = node.children
    # if children:
    #     for child in children:  # type: AlphaBetaNode
    #         if alpha:
    #             # print("adding child to min")
    #             heapq.heappush(minimizer_queue, (child.beta_value, child))
    #
    #         else:
    #             # print("adding child to max")
    #             heapq.heappush(maximizer_queue, (child.alpha_value, child))
    #         if child.reevaluate_flag:
    #             child.reevaluate_flag = False
    #             heapq.heappush(maximizer_queue, (node.value, node))
    #             heapq.heappush(minimizer_queue, (node.value, node))

    # print(RenderTree(node))
    choose_next_node(not alpha, maximizer_queue, minimizer_queue)
    return node


def alpha_beta_problem(input_string):
    print("starting alpha-beta on {}".format(input_string))
    tree_root = initialize_tree(input_string)

    maximizer_queue = collections.deque([tree_root])
    minimizer_queue = collections.deque([tree_root])

    print(maximizer_queue)
    print(minimizer_queue)

    choose_next_node(True, maximizer_queue, minimizer_queue)

    print("finished alpha-beta on {}, ended up with \n\n{}".format(input_string, RenderTree(tree_root)))
    return tree_root


def tests():
    # tree_root = initialize_tree("3 17 2 12 15 25 0 2 5 3 2 14")
    # print(RenderTree(tree_root))
    #
    # maximizer_queue = collections.deque([tree_root])
    # minimizer_queue = collections.deque([tree_root])
    #
    # print(maximizer_queue)
    # print(minimizer_queue)
    #
    # print(maximizer_queue.pop())

    alpha_beta_problem("3 17 2 12 15 25 0 2 5 3 2 14")


tests()
# alpha_beta_problem("0 1 2 3 4 5 6 7 8 9 10 11")
#
# alpha_beta_problem("4 6 7 9 1 2 0 1 8 1 9 2")

# alpha_beta_problem("3 17 2 12 15 25 0 2 5 3 2 14")
