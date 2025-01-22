import pygame
from typing import Self
from typing import Callable

pygame.init()

class Button:
    def __init__(self, image: pygame.Surface, pos: tuple[int, int]):
        self.image = image
        self.pos = pos
        self.rect = self.image.get_rect(topleft=self.pos)
        self.clicking = False

    def update(self, surface: pygame.Surface) -> bool:
        surface.blit(self.image, self.pos)

        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
            if pygame.mouse.get_pressed()[0] == 1:
                self.clicking = True
        
        if self.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
            if pygame.mouse.get_pressed()[0] == 0 and self.clicking:
                self.clicking = False
                return True
        return False

class ButtonNode:
    def __init__(self, name: str, type: str, button: Button = None, parent_node: Self = None, child_node: Self = None, callback: Callable[[object], None] = None) -> None:
        self.name = name
        self.type = type
        self.button = button
        self.parent_node = parent_node
        self.child_node: list[Self] = [child_node]
        self.callback = callback
    
    def check_parent(self) -> bool:
        return self.parent_node != None
    
    def check_child(self) -> bool:
        return self.child_node != None
    
    def add_child(self, node: Self) -> None:
        if self.child_node[0] == None:
            self.child_node[0] = node
        else:
            self.child_node.append(node)
        node.parent_node = self
    
    def has_child(self, name: str) -> bool:
        if not self.child_node[0]:
            return False
        for child in self.child_node:
            if child.name == name:
                return True
        return False
    
    def get_child(self, name: str) -> Self:
        for child in self.child_node:
            if child.name == name:
                return child
    
    def update_children(self, screen: pygame.Surface) -> int | None:
        if not self.child_node[0]:
            return None
        for i, child in enumerate(self.child_node):
            if child.button.update(screen):
                return i
            
#add tree class to contain the nodes
class ButtonTree:
    def __init__(self) -> None:
        self.node = ButtonNode("main", "parent")
    
    def add_branch(self, dir: str, name:str, type: str, image: pygame.Surface, pos: tuple[int, int], func: Callable[[object], None] = None) -> None:
        steps = dir.split("/")
        button = Button(image, pos)
        node = ButtonNode(name, type, button, callback=func)
        cur_node = self.node
        for step in steps:
            if cur_node.has_child(step):
                cur_node = cur_node.get_child(step)
        
        cur_node.add_child(node)
    
    def starting_point(self) -> None:
        while self.node.name != "main":
            self.node = self.node.parent_node
    
    def update(self, screen: pygame.Surface, client: object) -> None:
        node = self.node.update_children(screen)
        if node != None and self.node.child_node[0]:
            self.node = self.node.child_node[node]
            t = self.node.type
            if t == "back":
                parent = self.node.parent_node
                self.node = parent.parent_node
            if t == "text":
                self.node = self.node.parent_node
            if t == "func":
                self.node.callback(client)
                self.node = self.node.parent_node
            if t == "quit":
                return False
        return True