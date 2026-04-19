"""
Filesystem skills
-----------------
Tools for reading directory trees, reading files, and writing files to disk.

Used by: all agents.
"""
from crewai_tools import FileReadTool, FileWriterTool, DirectoryReadTool

read_file  = FileReadTool()        # Read any file by path
write_file = FileWriterTool()      # Create or overwrite files on disk
read_dir   = DirectoryReadTool()   # List and explore directory trees
