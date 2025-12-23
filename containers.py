
from io import StringIO

class Array:
    """
    A class wrapper over a list that provides additional helpful methods in daily usage.
    """
    class Wrapper:
        """
        A class representing a wrapped item in the Array, containing the item itself and its index in the Array.
        """
        def __init__(self, item, index):
            self.item = item
            self.index = index

    def __init__(self, items):
        self.items = items

    def append(self, item):
        """Appends an item to the end of the Array."""
        self.items.append(item)
    
    def insert(self, index, item):
        """Inserts an item at the specified index in the Array."""
        self.items.insert(index, item)
    def count(self):
        """Returns the number of items in the Array."""
        return len(self.items)
    
    def remove(self, item_wrapper): 
        """Removes an item from the Array using its wrapper."""
        self.items.pop(item_wrapper.index)

    def get_by_index(self, index):
        """Returns the item wrapper at the specified index."""
        return self.wrapper(self.items[index], index)
    def get(self, filter):
        """Returns the first item wrapper that matches the filter function, or None if no match is found."""
        for index, item in enumerate(self.items):
            if filter(item):
                return self.wrapper(item, index) 
        return None

    def sort(self, key, decending=True):
        """
        Sorts the Array items based on the specified key function and order.
        - key : function that takes an item and returns the value to sort by
        - decending : boolean indicating whether to sort in decending order or ascending order
        """
        self.items.sort(key=key, reverse=decending)

    def sort_exact(self, order, key):
        """
        Sorts the Array items to match the exact order specified in the order list based on the key function.
        - order : list of values of some property of the items in the Array
        - key : function that takes an item and returns the value of the property to be matched with the order list
        """
        for index in range(len(order)):
            for i, item in enumerate(self.items):
                if key(item) == order[index]:
                    self.items[index], self.items[i] = self.items[i], self.items[index]
                    break

    def write(self, output, format):
        """
        Writes the formatted representation of each item in the Array to the given output.
        - output : a file-like object with a write method
        - format : a function that takes an item and returns its string representation
        """
        for item in self.items:
            output.write(format(item) + "\n")

    def print(self, format):
        """
        Writes all elements of the Array to the standard output using the specified format function.
        - format : a function that takes an item and returns its string representation
        """
        output = StringIO()
        self.write(output, format)
        print(output.getvalue())

    # ========== Helpers ==========

    def __iter__(self):
        for index, item in enumerate(self.items):
            yield self.wrapper(item, index)
    def __len__(self):
        return len(self.items)
    def __getitem__(self, index):
        return self.get_by_index(index)
    def __setitem__(self, index, item):
        self.items[index] = item
    def wrapper(self, item, index):
        return Array.Wrapper(item, index)



if __name__ == "__main__":
    # Example usage
    arr = Array([5, 3, 8, 1])
    arr.append(4)
    arr.insert(2, 7)
    print("Count:", arr.count())  # Count: 6

    item_wrapper = arr.get(lambda x: x == 7)
    if item_wrapper:
        print("Found item:", item_wrapper.item, "at index:", item_wrapper.index)

    arr.reorder(key=lambda x: x)
    arr.print(format=lambda x: f"Item: {x}")

    arr.reorder_exact(order=[1, 3, 4, 5, 7, 8], key=lambda x: x)
    arr.print(format=lambda x: f"Item: {x}")
