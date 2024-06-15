class Technology:
    def __init__(self, name, research_time, cost, completed=False):
        self.name = name
        self.research_time = research_time
        self.cost = cost
        self.completed = completed
        self.children = []

    def add_child(self, child):
        self.children.append(child)



def create_tech_tree():
    """Example: root = Technology("Root Tech", 5, 100)
    tech1 = Technology("Tech 1", 3, 50)
    tech2 = Technology("Tech 2", 4, 75)
    tech3 = Technology("Tech 3", 2, 30)
    tech4 = Technology("Tech 4", 6, 120)

    root.add_child(tech1)
    root.add_child(tech2)
    tech1.add_child(tech3)
    tech2.add_child(tech4)

    return root"""