from product import PhysicalProduct, DigitalProduct, CanBeShipped

for weight in (0, 0.1, 2.5, 10):
    item = PhysicalProduct("P1", "Test", 1.0, 1, weight)
    print(weight, "kg ->", item.calculate_shipping_cost())

digital = DigitalProduct("P2", "OS", 99.99, 10, 4200)
physical = PhysicalProduct("P3", "Guitar", 450.0, 5, 3.5)
print("Digital can be shipped:", isinstance(digital, CanBeShipped))
print("Physical can be shipped:", isinstance(physical, CanBeShipped))