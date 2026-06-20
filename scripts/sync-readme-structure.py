#!/usr/bin/env python3
"""
Sync the directory structure in README.md with the actual filesystem.

Uses HTML comments to mark the auto-generated section:
  <!-- STRUCTURE_START --> ... <!-- STRUCTURE_END -->

Run from the repo root: python scripts/sync-readme-structure.py
"""

from pathlib import Path


def format_plugin_tree(root: Path) -> list[str]:
    """Format the plugins directory tree, showing only key files (SKILL.md, plugin.json, references/)."""
    lines = []
    plugins_path = root / "plugins"
    
    # Maintain original order of plugins
    plugin_order = ["devcontainer", "engineering-workflow", "synouser", "ugacltool", "aspire"]
    plugin_dirs = []
    for name in plugin_order:
        dir_path = plugins_path / name
        if dir_path.exists():
            plugin_dirs.append(dir_path)
    # Add any new plugins not in the order list
    all_dirs = [d for d in plugins_path.iterdir() if d.is_dir()]
    for d in all_dirs:
        if d not in plugin_dirs:
            plugin_dirs.append(d)
    
    for i, plugin_dir in enumerate(plugin_dirs):
        is_last = (i == len(plugin_dirs) - 1)
        
        # Plugin directory line
        if is_last:
            lines.append("    └── " + plugin_dir.name + "/")
            prefix = "        "
        else:
            lines.append("    ├── " + plugin_dir.name + "/")
            prefix = "    │   "
        
        # Get items in order: README.md, .plugin, .claude-plugin, agents, skills
        items = []
        readme = plugin_dir / "README.md"
        if readme.exists():
            items.append(("README.md                 # How plugin packages are organized", None, True))
        
        for d in [".plugin", ".claude-plugin"]:
            dir_path = plugin_dir / d
            if dir_path.exists():
                items.append((d + "/", dir_path, False))
        
        # Add agents and skills dirs
        agents_dir = plugin_dir / "agents"
        if agents_dir.exists():
            items.append(("agents/", agents_dir, False))
        
        skills_dir = plugin_dir / "skills"
        if skills_dir.exists():
            items.append(("skills/", skills_dir, False))
        
        # Process items
        for j, (name, path, is_file) in enumerate(items):
            is_last_item = (j == len(items) - 1)
            
            if is_file:
                # README.md with comment
                connector = "└── " if is_last_item else "├── "
                lines.append(prefix + connector + name)
            else:
                # Directory
                connector = "└── " if is_last_item else "├── "
                lines.append(prefix + connector + name)
                
                sub_prefix = prefix + ("    " if is_last_item else "│   ")
                
                if name.startswith("."):
                    # .plugin or .claude-plugin - just show plugin.json
                    lines.append(sub_prefix + "└── plugin.json")
                elif name == "agents/":
                    # List agent files
                    agent_files = sorted([f for f in path.iterdir() 
                                        if f.is_file() and f.name.endswith('.agent.md')])
                    for k, af in enumerate(agent_files):
                        is_last_af = (k == len(agent_files) - 1)
                        af_connector = "└── " if is_last_af else "├── "
                        lines.append(sub_prefix + af_connector + af.name)
                elif name == "skills/":
                    # List skill directories
                    skill_dirs = sorted([d for d in path.iterdir() if d.is_dir()])
                    for k, sd in enumerate(skill_dirs):
                        is_last_sd = (k == len(skill_dirs) - 1)
                        sd_connector = "└── " if is_last_sd else "├── "
                        lines.append(sub_prefix + sd_connector + sd.name + "/")
                        
                        sd_prefix = sub_prefix + ("    " if is_last_sd else "│   ")
                        
                        # Collect all children to display for this skill
                        children = []
                        skill_md = [f for f in sd.iterdir() if f.is_file() and f.name == "SKILL.md"]
                        children.extend(skill_md)
                        
                        ref_dir = sd / "references"
                        if ref_dir.exists() and any(f.is_file() for f in ref_dir.iterdir()):
                            children.append(ref_dir)
                        
                        # Display all children
                        for m, child in enumerate(children):
                            is_last_child = (m == len(children) - 1)
                            child_connector = "└── " if is_last_child else "├── "
                            
                            if isinstance(child, Path) and child.is_file():
                                # SKILL.md file
                                lines.append(sd_prefix + child_connector + child.name)
                            elif isinstance(child, Path) and child.is_dir():
                                # references directory
                                lines.append(sd_prefix + child_connector + child.name + "/")
                                # Add reference files
                                ref_files = sorted([f for f in child.iterdir() if f.is_file()])
                                ref_prefix = sd_prefix + ("    " if is_last_child else "│   ")
                                for n, rf in enumerate(ref_files):
                                    is_last_rf = (n == len(ref_files) - 1)
                                    rf_connector = "└── " if is_last_rf else "├── "
                                    lines.append(ref_prefix + rf_connector + rf.name)
    
    return lines


def update_readme():
    """Update the README.md structure section."""
    repo_root = Path(__file__).parent.parent
    readme_path = repo_root / "README.md"
    
    # Read the current README
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the structure section between HTML comments
    start_marker = "<!-- STRUCTURE_START -->"
    end_marker = "<!-- STRUCTURE_END -->"
    
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)
    
    if start_idx == -1 or end_idx == -1:
        print("Error: Could not find STRUCTURE_START and/or STRUCTURE_END markers in README.md")
        print("Please add these HTML comments to mark the auto-generated section:")
        print(f"  {start_marker}")
        print(f"  ... (the tree structure) ...")
        print(f"  {end_marker}")
        return False
    
    # Extract the prefix (everything before START marker including the marker)
    prefix = content[:start_idx + len(start_marker)]
    # Extract the suffix (everything after END marker)
    suffix = content[end_idx:]
    
    # Generate the new tree
    tree_lines = ["agentic/"]
    
    # Add root files
    tree_lines.append("├── AGENTS.md                    # Repo-specific rules for future Codex/Copilot work")
    
    # Add .claude-plugin
    tree_lines.append("├── .claude-plugin/")
    tree_lines.append("│   └── marketplace.json          # Canonical marketplace catalog (Claude & Copilot)")
    
    # Add .github
    tree_lines.append("├── .github/")
    tree_lines.append("│   ├── copilot-instructions.md   # Global Copilot instructions for this repo")
    tree_lines.append("│   └── plugin/")
    tree_lines.append("│       └── marketplace.json      # Compatibility copy of marketplace catalog")
    
    # Add plugins tree
    tree_lines.append("└── plugins/")
    plugin_lines = format_plugin_tree(repo_root)
    tree_lines.extend(plugin_lines)
    
    # Build the new content with backticks
    new_tree = "\n".join(tree_lines)
    new_content = prefix + "\n```\n" + new_tree + "\n```\n" + suffix
    
    # Write the updated README
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("Successfully updated README.md structure section")
    return True


if __name__ == "__main__":
    update_readme()
