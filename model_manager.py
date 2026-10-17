
import pickle
import json


class ModelMetadata:
    class Filter:
        def __init__(self, name=None, version=None, path=None, additional=None):
            self.name = name
            self.version = version
            self.path = path
            self.additional = additional
        def match(self, metadata):
            if self.name is not None and self.name != metadata.name:
                return False
            if self.version is not None and self.version != metadata.version:
                return False
            if self.path is not None and self.path != metadata.path:
                return False
            if self.additional is not None and self.additional != metadata.additional:
                return False
            return True

    def __init__(self, name, version, path, additional):
        self.name = name
        self.version = version
        self.path = path
        self.additional = additional
    
    def save_model(self, model):
        with open(self.path, 'wb') as f:
            pickle.dump(model, f)
        return self
    def load_model(self):
        try:
            with open(self.path, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return None

    def to_json(self):
        return {
            "name": self.name,
            "version": self.version,
            "path": self.path,
            "additional": self.additional
        }
    @staticmethod
    def from_json(data):
        return ModelMetadata(
            name=data.get("name"),
            version=data.get("version"),
            path=data.get("path"),
            additional=data.get("additional")
        )

class ModelManager:
    class BaseLoaderSaver:
        def __init__(self, path):
            self.path = path
    class JsonLoaderSaver(BaseLoaderSaver):
        def load(self):
            with open(self.path, 'r') as f:
                objects = json.load(f)
            metadata = []
            for object in objects:
                metadata.append(
                    ModelMetadata.from_json(object)
                )
            return metadata
        def save(self, data):
            objects = []
            for metadata in data:
                objects.append(metadata.to_json())
            with open(self.path, 'w') as f:
                json.dump(objects, f, indent=4)
    class PickleLoaderSaver(BaseLoaderSaver):
        def load(self):
            with open(self.path, 'rb') as f:
                return pickle.load(f)
        def save(self, data):
            with open(self.path, 'wb') as f:
                pickle.dump(data, f)

    class Category:
        class Filter:
            def __init__(self, name=None):
                self.name = name
            def match(self, category):
                if self.name is not None and self.name != category.name:
                    return False
                return True
        
        def __init__(self, name, description, subcategories=None, models=None):
            self.name = name
            self.description = description
            self.subcategories = subcategories if subcategories is not None else []
            self.models = models if models is not None else []
        
        def find_model(self, filter):
            results = []
            if filter.match(self):
                

    def __init__(self):
        self.metadata = []
        self.categories = []
    
    def find(self, filter):
        results = []
        for meta in self.metadata:
            if filter.match(meta):
                results.append(meta)
        return results


    def all(self):
        return self.metadata
    
    def load(self, loader):
        try:
            self.metadata = loader.load()
            return True
        except FileNotFoundError:
            return False
    def save(self, saver):
        saver.save(self.metadata)

    def describe(self):
        print("=== Model Manager Metadata ===")
        for model in self.metadata:
            print(f"Name: {model.name}, Version: {model.version}, Path: {model.path}, Additional: {model.additional}")
        print("=== End of Metadata ===")

    def add(self, metadata):
        self.metadata.append(metadata)
    def remove(self, metadata):
        if metadata in self.metadata:
            self.metadata.remove(metadata)

