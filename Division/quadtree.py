from typing import Iterable

from geometry import Point2D, Rectangle2D
from tree import RegionData, NodeBase



class QuadTree:
    def __init__(self, rectangle: Rectangle2D, max_accumulation: int):
        self.main_node: NodeBase = AccumulatingNode(self, rectangle)
        self.max_accumulation = max_accumulation

    # Adds item to tree
    def add(self, item) -> None:
        self.main_node: NodeBase = self.main_node.add(item)

    # Returns all leaf regions
    def get_regions(self) -> list[RegionData]:
        return self.main_node.get_regions()


class QuadNode(NodeBase):
    def __init__(self, tree: QuadTree, rectangle: Rectangle2D):
        NodeBase.__init__(self, tree, rectangle)
        self.subnodes = list[NodeBase]()
        for y in range(2):
            for x in range(2):
                rect = self.get_subrectangle(x, y)
                self.subnodes.append(AccumulatingNode(self.tree, rect))

    def add(self, item) -> NodeBase:
        point = item.location
        x = min(int((point.x - self.rectangle.location.x) / self.rectangle.width * 2), 1)
        y = min(int((point.y - self.rectangle.location.y) / self.rectangle.height * 2), 1)
        index = y * 2 + x
        self.subnodes[index] = self.subnodes[index].add(item)
        return self

    def get_subrectangle(self, node_x: int, node_y: int) -> Rectangle2D:
        half_w = self.rectangle.width / 2
        half_h = self.rectangle.height / 2
        x = self.rectangle.location.x
        if node_x > 0:
            x += half_w
        y = self.rectangle.location.y
        if node_y > 0:
            y += half_h
        return Rectangle2D(Point2D(x, y), half_w, half_h)

    def get_regions(self) -> list[RegionData]:
        regions = []
        for i in range(len(self.subnodes)):
            subregions = self.subnodes[i].get_regions()
            regions.extend(subregions)
        return regions


class AccumulatingNode(NodeBase):
    def __init__(self, tree: QuadTree, rectangle: Rectangle2D):
        NodeBase.__init__(self, tree, rectangle)
        self.items = list()

    def add(self, item) -> NodeBase:
        if len(self.items) < self.tree.max_accumulation:
            self.items.append(item)
            return self
        else:
            new_node = QuadNode(self.tree, self.rectangle)
            for prevItem in self.items:
                new_node.add(prevItem)
            new_node.add(item)
            return new_node

    def get_regions(self) -> list[RegionData]:
        return [ RegionData(self.rectangle, self.items) ]

