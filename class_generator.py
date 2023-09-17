class ClassGenerator:
    def __init__(self, class_name, properties=None, methods=None):
        self.class_name = class_name
        self.properties = properties if properties else []
        self.methods = methods if methods else []

    def generate(self):
        lines = [f"class {self.class_name}:"]
        
        if not self.properties and not self.methods:
            lines.append("    pass")
        else:
            # __init__ method
            lines.append("    def __init__(self, " + ', '.join(self.properties) + "):")
            for prop in self.properties:
                lines.append(f"        self._{prop} = {prop}")

            # properties with @property
            for prop in self.properties:
                # getter
                lines.append(f"\n    @property")
                lines.append(f"    def {prop}(self):")
                lines.append(f"        return self._{prop}")

                # setter
                lines.append(f"\n    @{prop}.setter")
                lines.append(f"    def {prop}(self, value):")
                lines.append(f"        self._{prop} = value")

            # methods
            for method_name, method_code in self.methods.items():
                lines.append(f"\n    def {method_name}(self):")
                method_lines = [f"        {line}" for line in method_code.split('\n')]
                lines.extend(method_lines)
        self.str_class = '\n'.join(lines)
    
    def show(self):
        print(self.str_class)

if __name__ == '__main__':
    methods = {
        "introduce": "print(f'I am {self.name} and I am {self.age} years old.')"
    }

    generator = ClassGenerator("Person", ["name", "age"], methods)
    print(generator.generate())
