#!/usr/bin/env python3
"""
================================================================================
IC-307D: Data Structures and Algorithms Lab
Unit 6: Trees
Program 6: Hierarchical File System Simulator using N-ary Tree Structure

Author: Student Implementation
Course: IC-307D — DSA Lab (CO3)
Language: Python 3
================================================================================

CONCEPT & THEORETICAL BACKGROUND:
Operating system file systems (such as ext4 in Linux, NTFS in Windows, and APFS
in macOS) are naturally modeled as general hierarchical N-ary trees:
  - Root Node: The topmost directory (e.g., '/').
  - Internal Nodes: Directories containing an arbitrary list of child nodes.
  - Leaf Nodes: Regular files or empty directories.

TREE-BASED FILE SYSTEM MECHANICS:
  - Each FSNode represents either a File or a Directory.
  - Directory nodes maintain a list of child FSNodes and a reference to their parent.
  - Path traversal (e.g., '/home/user/docs') navigates sequentially down the tree.
  - Operations like 'cd ..' traverse upward via parent references.
  - Recursive tree walks implement 'tree' visualization, size calculation, and
    global file searches.

SAFETY & INTEGRITY CONSTRAINTS:
  - Duplicate names within the same directory are strictly rejected.
  - The root directory ('/') cannot be deleted.
  - Non-empty directories require recursive confirmation to prevent accidental loss.
  - A directory currently in use (or an ancestor of the current path) cannot be deleted.
  - ALL OPERATIONS OCCUR PURELY IN-MEMORY on the tree data structure (NO REAL OS FILES
    ARE CREATED OR MODIFIED).

COMPLEXITIES:
  - Create File / Dir: O(k) where k is the number of items in the current directory.
  - Navigate (cd / cd ..): O(1) or O(depth) for absolute paths.
  - Tree Display / Search: O(N) where N is total nodes in the subtree.
  - Space Complexity: O(N) for tree node hierarchy.
================================================================================
"""

import sys
from typing import Any, List, Optional, Tuple


class FSNode:
    """Represents a node (either a file or a directory) in the file system tree."""

    def __init__(self, name: str, is_directory: bool = False, size: int = 0) -> None:
        if not name or "/" in name:
            raise ValueError("Invalid node name: Name cannot be empty or contain '/' characters.")

        self.name: str = name
        self.is_directory: bool = is_directory
        self.size: int = size
        self.parent: Optional["FSNode"] = None
        self.children: List["FSNode"] = [] if is_directory else []

    def get_path(self) -> str:
        """Construct absolute path by traversing parent references to root."""
        if self.parent is None:
            return "/"
        path_components = []
        curr: Optional[FSNode] = self
        while curr is not None and curr.parent is not None:
            path_components.append(curr.name)
            curr = curr.parent
        return "/" + "/".join(reversed(path_components))

    def get_total_size(self) -> int:
        """Calculate total size recursively for directory or return file size."""
        if not self.is_directory:
            return self.size
        return sum(child.get_total_size() for child in self.children)

    def find_child(self, name: str) -> Optional["FSNode"]:
        """Find a direct child with the specified name."""
        for child in self.children:
            if child.name == name:
                return child
        return None

    def __repr__(self) -> str:
        type_str = "DIR" if self.is_directory else "FILE"
        return f"FSNode({self.name}, {type_str}, path='{self.get_path()}')"


class FileSystemSimulator:
    """Hierarchical in-memory file system using general N-ary tree."""

    def __init__(self) -> None:
        self.root: FSNode = FSNode(name="root", is_directory=True)
        # Fix root naming display
        self.root.name = ""
        self.cwd: FSNode = self.root  # Current Working Directory

    def get_current_path(self) -> str:
        """Return absolute path string of current working directory."""
        return self.cwd.get_path()

    def create_directory(self, name: str) -> FSNode:
        """
        Create a new directory inside current working directory.
        Raises ValueError on duplicate or invalid names.
        """
        if self.cwd.find_child(name) is not None:
            raise ValueError(f"Cannot create directory '{name}': Item with this name already exists.")

        new_dir = FSNode(name=name, is_directory=True)
        new_dir.parent = self.cwd
        self.cwd.children.append(new_dir)
        # Keep children sorted alphabetically
        self.cwd.children.sort(key=lambda x: (not x.is_directory, x.name.lower()))
        return new_dir

    def create_file(self, name: str, size: int = 0) -> FSNode:
        """
        Create a new file inside current working directory.
        Raises ValueError on duplicate or invalid names.
        """
        if self.cwd.find_child(name) is not None:
            raise ValueError(f"Cannot create file '{name}': Item with this name already exists.")
        if size < 0:
            raise ValueError("File size cannot be negative.")

        new_file = FSNode(name=name, is_directory=False, size=size)
        new_file.parent = self.cwd
        self.cwd.children.append(new_file)
        self.cwd.children.sort(key=lambda x: (not x.is_directory, x.name.lower()))
        return new_file

    def navigate_directory(self, name: str) -> None:
        """
        Navigate to a child directory ('cd <name>') or root ('/').
        """
        if name == "/":
            self.cwd = self.root
            return
        if name == "..":
            self.navigate_to_parent()
            return
        if name == "." or name == "":
            return

        child = self.cwd.find_child(name)
        if child is None:
            raise FileNotFoundError(f"Directory '{name}' not found.")
        if not child.is_directory:
            raise NotADirectoryError(f"'{name}' is a file, not a directory.")

        self.cwd = child

    def navigate_to_parent(self) -> None:
        """Navigate to parent directory ('cd ..')."""
        if self.cwd.parent is not None:
            self.cwd = self.cwd.parent

    def search(self, query: str) -> List[str]:
        """
        Search for files or directories matching query recursively across entire tree.
        Returns list of matching absolute paths.
        """
        matches: List[str] = []
        self._search_recursive(self.root, query.lower(), matches)
        return matches

    def _search_recursive(self, node: FSNode, query: str, matches: List[str]) -> None:
        if query in node.name.lower() and node != self.root:
            matches.append(node.get_path() + ("/" if node.is_directory else ""))

        if node.is_directory:
            for child in node.children:
                self._search_recursive(child, query, matches)

    def delete(self, name: str, recursive: bool = False) -> None:
        """
        Delete a file or directory inside the current working directory.
        Raises ValueError if attempting to delete non-empty directory without recursive=True,
        or deleting current path / root.
        """
        child = self.cwd.find_child(name)
        if child is None:
            raise FileNotFoundError(f"Item '{name}' not found in current directory.")

        if child.is_directory:
            if len(child.children) > 0 and not recursive:
                raise ValueError(
                    f"Directory '{name}' is not empty ({len(child.children)} items). Use recursive delete."
                )

        self.cwd.children.remove(child)
        child.parent = None

    def display_tree(self, start_node: Optional[FSNode] = None) -> None:
        """Display hierarchical tree layout with branches."""
        target = start_node if start_node is not None else self.cwd
        path_label = target.get_path()
        print(f"  {path_label} [DIR - {target.get_total_size()} bytes]")
        self._display_tree_recursive(target, prefix="")

    def _display_tree_recursive(self, node: FSNode, prefix: str) -> None:
        count = len(node.children)
        for idx, child in enumerate(node.children):
            is_last = (idx == count - 1)
            connector = "`-- " if is_last else "|-- "
            if child.is_directory:
                info = f"[DIR - {child.get_total_size()} B, {len(child.children)} items]"
            else:
                info = f"({child.size} B)"
            print(f"  {prefix}{connector}{child.name} {info}")

            if child.is_directory and len(child.children) > 0:
                extension = "    " if is_last else "|   "
                self._display_tree_recursive(child, prefix + extension)


def build_sample_filesystem() -> FileSystemSimulator:
    """Populate sample file system hierarchy for testing and demonstrations."""
    fs = FileSystemSimulator()
    # /bin
    fs.create_directory("bin")
    fs.navigate_directory("bin")
    fs.create_file("bash", 1024)
    fs.create_file("ls", 512)
    fs.navigate_to_parent()

    # /home
    fs.create_directory("home")
    fs.navigate_directory("home")
    fs.create_directory("student")
    fs.navigate_directory("student")
    fs.create_file("lab_report.pdf", 2048)
    fs.create_file("code.py", 450)
    fs.create_directory("projects")
    fs.navigate_directory("projects")
    fs.create_file("dsa_tree.py", 1200)
    fs.navigate_directory("/")  # return to root

    return fs


def run_tests() -> None:
    """Automated unit verification test suite for File System Simulator."""
    print("=" * 70)
    print("RUNNING AUTOMATED TEST SUITE: File System Simulator (N-ary Tree)")
    print("=" * 70)

    fs = FileSystemSimulator()
    assert fs.get_current_path() == "/"
    print("[PASS] Test 1: Root directory initialized.")

    # Test 2: Create directories and files
    docs = fs.create_directory("docs")
    fs.create_file("notes.txt", 100)
    assert len(fs.cwd.children) == 2
    assert fs.cwd.find_child("docs") is not None
    assert fs.cwd.find_child("notes.txt") is not None
    print("[PASS] Test 2: Directory and file creation verified.")

    # Test 3: Duplicate name validation
    try:
        fs.create_file("notes.txt", 50)
        assert False, "Should raise ValueError on duplicate name"
    except ValueError:
        pass
    print("[PASS] Test 3: Duplicate name rejection verified.")

    # Test 4: Navigation (cd and cd ..)
    fs.navigate_directory("docs")
    assert fs.get_current_path() == "/docs"
    fs.create_file("syllabus.pdf", 500)
    fs.navigate_to_parent()
    assert fs.get_current_path() == "/"
    print("[PASS] Test 4: Path navigation (cd and cd ..) verified.")

    # Test 5: Search functionality
    search_res = fs.search("syllabus")
    assert search_res == ["/docs/syllabus.pdf"]
    print("[PASS] Test 5: Recursive file search verified.")

    # Test 6: Deletion with non-empty directory protection
    try:
        fs.delete("docs", recursive=False)
        assert False, "Should raise ValueError on non-empty directory without recursive flag"
    except ValueError:
        pass
    fs.delete("docs", recursive=True)
    assert fs.cwd.find_child("docs") is None
    print("[PASS] Test 6: Non-empty directory safety and recursive deletion verified.")

    # Test 7: Complex sample hierarchy verification
    sample_fs = build_sample_filesystem()
    all_bash = sample_fs.search("bash")
    assert "/bin/bash" in all_bash
    all_py = sample_fs.search(".py")
    assert "/home/student/code.py" in all_py
    assert "/home/student/projects/dsa_tree.py" in all_py
    print("[PASS] Test 7: Multi-level sample tree search and navigation verified.")

    print("\nALL 7 TEST CASES PASSED SUCCESSFULLY!")
    print("=" * 70)


def print_menu() -> None:
    """Print the interactive CLI menu."""
    print("\n" + "=" * 55)
    print("         FILE SYSTEM TREE SIMULATOR")
    print("=" * 55)
    print(" 1. Display Current Directory Tree ('tree')")
    print(" 2. Create Directory ('mkdir <name>')")
    print(" 3. Create File ('touch <name> <size>')")
    print(" 4. Change Directory ('cd <dir>')")
    print(" 5. Navigate to Parent Directory ('cd ..')")
    print(" 6. Print Working Directory ('pwd')")
    print(" 7. Search File / Directory ('search <query>')")
    print(" 8. Delete File or Directory ('rm <name>')")
    print(" 9. Load Sample File System Hierarchy")
    print(" 10. Run Automated Tests (--test)")
    print(" 11. Exit")
    print("=" * 55)


def main() -> None:
    """Main CLI driver."""
    if len(sys.argv) > 1 and sys.argv[1] in ("--test", "-t"):
        run_tests()
        sys.exit(0)

    print("==========================================================")
    print("  IC-307D: Unit 6 — File System Simulator (N-ary Tree)")
    print("==========================================================")

    fs = build_sample_filesystem()
    print("Loaded standard sample file system hierarchy.")

    while True:
        print_menu()
        print(f"Current Directory: {fs.get_current_path()}")
        choice = input("Enter choice (1-11): ").strip()

        if choice == "1":
            print("\nDirectory Tree:")
            fs.display_tree()

        elif choice == "2":
            d_name = input("Enter directory name to create: ").strip()
            try:
                fs.create_directory(d_name)
                print(f"Directory '{d_name}' created successfully.")
            except ValueError as err:
                print(f"Error: {err}")

        elif choice == "3":
            f_name = input("Enter file name to create: ").strip()
            s_str = input("Enter file size in bytes (e.g. 1024): ").strip()
            try:
                size = int(s_str) if s_str else 0
                fs.create_file(f_name, size=size)
                print(f"File '{f_name}' ({size} bytes) created successfully.")
            except ValueError as err:
                print(f"Error: {err}")

        elif choice == "4":
            target = input("Enter directory name to navigate into (or '/' for root): ").strip()
            try:
                fs.navigate_directory(target)
                print(f"Moved to: {fs.get_current_path()}")
            except (FileNotFoundError, NotADirectoryError) as err:
                print(f"Navigation Error: {err}")

        elif choice == "5":
            fs.navigate_to_parent()
            print(f"Moved to: {fs.get_current_path()}")

        elif choice == "6":
            print(f"Current Path: {fs.get_current_path()}")

        elif choice == "7":
            q = input("Enter search keyword: ").strip()
            results = fs.search(q)
            if results:
                print(f"Found {len(results)} match(es):")
                for p in results:
                    print(f"  - {p}")
            else:
                print("No matching files or directories found.")

        elif choice == "8":
            target = input("Enter file or directory name to delete: ").strip()
            rec_input = input("Delete recursively if non-empty? (y/n): ").strip().lower()
            rec = rec_input == "y"
            try:
                fs.delete(target, recursive=rec)
                print(f"'{target}' deleted successfully.")
            except (FileNotFoundError, ValueError) as err:
                print(f"Deletion Error: {err}")

        elif choice == "9":
            fs = build_sample_filesystem()
            print("Reset to sample file system hierarchy.")

        elif choice == "10":
            run_tests()

        elif choice == "11":
            print("Exiting File System Simulator. Goodbye!")
            break

        else:
            print("Invalid choice! Please select an option from 1 to 11.")


if __name__ == "__main__":
    main()

