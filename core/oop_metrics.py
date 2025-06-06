import ast

# AST-візітор для обчислення RFC (Response for Class)
class ClassRFCVisitor(ast.NodeVisitor):
    def __init__(self):
        self.methods = set()
        self.called = set()

    def visit_FunctionDef(self, node):
        self.methods.add(node.name)
        for child in ast.walk(node):
            if isinstance(child, ast.Call) and isinstance(child.func, ast.Attribute):
                self.called.add(child.func.attr)
        self.generic_visit(node)

# AST-візітор для збору ООП-метрик з класів
class ClassMetricsVisitor(ast.NodeVisitor):
    def __init__(self):
        self.class_defs = {}

    def visit_ClassDef(self, node):
        class_name = node.name
        method_count = 0
        attributes = set()
        used_attributes = {}
        local_couplings = set()

        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                method_count += 1
                method_name = item.name
                used_attributes[method_name] = set()

                for stmt in ast.walk(item):
                    if isinstance(stmt, ast.Attribute) and isinstance(stmt.value, ast.Name) and stmt.value.id == "self":
                        attributes.add(stmt.attr)
                        used_attributes[method_name].add(stmt.attr)

                    if isinstance(stmt, ast.Call) and isinstance(stmt.func, ast.Attribute):
                        if isinstance(stmt.func.value, ast.Name):
                            local_couplings.add(stmt.func.value.id)

        # LCOM (зв’язність методів)
        shared = 0
        total_pairs = 0
        methods = list(used_attributes.keys())
        for i in range(len(methods)):
            for j in range(i + 1, len(methods)):
                total_pairs += 1
                if used_attributes[methods[i]].intersection(used_attributes[methods[j]]):
                    shared += 1
        lcom = 1 - (shared / total_pairs) if total_pairs > 0 else 0.0
        lcom = max(0.0, round(lcom, 2))

        # RFC = методи + виклики
        rfc_visitor = ClassRFCVisitor()
        rfc_visitor.visit(node)
        class_rfc = len(rfc_visitor.methods.union(rfc_visitor.called))

        self.class_defs[class_name] = {
            "methods": method_count,
            "rfc": class_rfc,
            "lcom": lcom,
            "coupled": local_couplings,
            "bases": [base.id for base in node.bases if isinstance(base, ast.Name)]
        }

        self.generic_visit(node)

# Обчислює DIT (глибина ієрархії спадкування)
def compute_dit(hierarchy):
    def get_depth(cls, visited=None):
        if visited is None:
            visited = set()
        if cls in visited or cls not in hierarchy or not hierarchy[cls]:
            return 1
        visited.add(cls)
        return 1 + max(get_depth(base, visited) for base in hierarchy[cls])

    return max(get_depth(cls) for cls in hierarchy) if hierarchy else 1

# Основна функція обчислення ООП-метрик
def compute_oop_metrics(tree):
    visitor = ClassMetricsVisitor()
    visitor.visit(tree)

    rfc = sum(data["rfc"] for data in visitor.class_defs.values())

    base_class_usage = {}
    for data in visitor.class_defs.values():
        for base in data["bases"]:
            base_class_usage[base] = base_class_usage.get(base, 0) + 1
    noc = sum(base_class_usage.values())

    coupled_classes = set()
    for data in visitor.class_defs.values():
        coupled_classes.update(data["coupled"])
        coupled_classes.update(data["bases"])
    cbo = len(coupled_classes)

    lcom_values = [data["lcom"] for data in visitor.class_defs.values()]
    lcom = round(sum(lcom_values) / len(lcom_values), 2) if lcom_values else 0.0

    hierarchy = {cls: data["bases"] for cls, data in visitor.class_defs.items()}
    dit = compute_dit(hierarchy)

    return {
        "class_count": len(visitor.class_defs),
        "rfc": rfc,
        "noc": noc,
        "cbo": cbo,
        "lcom": lcom,
        "hierarchy": hierarchy,
        "dit": dit
    }
