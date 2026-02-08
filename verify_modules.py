import os
import sys
import importlib
import ast
import inspect
import traceback

# Add project root to path
sys.path.append(os.getcwd())

def find_main_class_in_file(file_path):
    with open(file_path, "r") as f:
        try:
            tree = ast.parse(f.read())
        except Exception:
            return None

    classes = [node.name for node in tree.body if isinstance(node, ast.ClassDef)]
    
    # Heuristics for finding the main class
    filename = os.path.basename(file_path).replace(".py", "")
    
    # 1. Exact match (PascalCase)
    pascal_name = "".join(x.title() for x in filename.split("_"))
    if pascal_name in classes:
        return pascal_name
        
    # 2. Ends with "Engine" or "Analyzer"
    candidates = [c for c in classes if c.endswith("Engine") or c.endswith("Analyzer") or c.endswith("Detector") or c.endswith("Metrics") or c.endswith("Modeller") or c.endswith("Values") or c.endswith("Mapper") or c.endswith("Predictor") or c.endswith("Aesthetics")]
    if len(candidates) == 1:
        return candidates[0]
        
    # 3. Contains part of filename
    for c in classes:
        if filename.split("_")[0].title() in c:
            return c
            
    return classes[0] if classes else None

def verify_modules():
    root_dir = "totality_engine/engines"
    modules_found = 0
    modules_passed = 0
    
    print(f"Scanning {root_dir}...")
    
    for subdir, dirs, files in os.walk(root_dir):
        if "__pycache__" in subdir:
            continue
            
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                file_path = os.path.join(subdir, file)
                module_path = file_path.replace(os.sep, ".").replace(".py", "")
                
                print(f"\nChecking {module_path}...")
                
                class_name = find_main_class_in_file(file_path)
                if not class_name:
                    print(f"  [WARN] No class found in {file}")
                    continue
                    
                print(f"  Found class candidate: {class_name}")
                
                try:
                    module = importlib.import_module(module_path)
                    cls = getattr(module, class_name)
                    
                    # Try instantiation
                    # Most engines take optional config, some take nothing
                    try:
                        instance = cls()
                    except TypeError:
                        try:
                            instance = cls({})
                        except:
                             # Try with nothing if config failed (some might not take config)
                             # Or maybe it requires arguments. 
                             # We'll just print error if both fail.
                             print(f"  [FAIL] Could not instantiate {class_name}")
                             traceback.print_exc()
                             continue

                    print(f"  [PASS] Successfully instantiated {class_name}")
                    modules_passed += 1
                    
                except ImportError as e:
                    print(f"  [FAIL] Import Error: {e}")
                except AttributeError:
                    print(f"  [FAIL] Class {class_name} not found in module")
                except Exception as e:
                    print(f"  [FAIL] Unexpected Error: {e}")
                    traceback.print_exc()
                
                modules_found += 1

    print(f"\nSummary: {modules_passed}/{modules_found} modules passed.")

if __name__ == "__main__":
    verify_modules()
