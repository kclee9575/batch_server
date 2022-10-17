import os
import inspect
import importlib
from define import BASE_DIR
from src.flow import Flow


class FlowManager:
    def get_flow_list(self):
        package_path = os.path.join(BASE_DIR, "src", "flow")
        modules = self.get_modules_in_package(package_path)

        get_flow_map = {}

        for module_name in modules:
            if ".pyc" in module_name:
                continue
            module_package_name = os.path.join(package_path, module_name)
            files = os.listdir(module_package_name)
            for file in files:
                if self.is_common_package_file(file) or file[-3:] != ".py":
                    continue

                module_name = self.make_module_name(BASE_DIR, file, module_package_name)
                for name, cls in inspect.getmembers(
                    importlib.import_module(module_name, package=__name__),
                    inspect.isclass,
                ):
                    if cls.__module__ != module_name or not issubclass(cls, Flow):
                        continue
                    get_flow_map[file] = cls

        return get_flow_map

    def is_common_package_file(self, file) -> bool:
        if file in ["__init__.py", "__pycache__"]:
            return True
        return False

    def get_modules_in_package(self, package_path):
        packeges = os.listdir(package_path)
        modules = []
        for package in packeges:
            if self.is_common_package_file(package):
                continue
            modules.append(package)
        return modules

    def make_module_name(
        self, base_dir: str, file: str, module_package_name: str
    ) -> str:
        file_name = file[:-3]
        module_name = os.path.join(module_package_name, file_name)
        module_name = module_name.replace(base_dir + os.sep, "")
        module_name = module_name.replace(os.sep, ".")
        return module_name
