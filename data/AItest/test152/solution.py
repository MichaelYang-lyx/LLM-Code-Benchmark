
def Strongest_Extension(class_name, extensions):
    def strength(extension):
        CAP = sum(1 for c in extension if c.isupper())
        SM = sum(1 for c in extension if c.islower())
        return CAP - SM

    strongest_extension = max(extensions, key=strength)
    return f"{class_name}.{strongest_extension}"

print(Strongest_Extension('my_class', ['AA', 'Be', 'CC']))
