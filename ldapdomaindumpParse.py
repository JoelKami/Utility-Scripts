#!/usr/bin/env python3
# Description: script diseñado para visualizar de una mejor manera la información de los JSON del dump que hace la utilidad ldapdomaindump.

import json, os
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Tree, Pretty, Static
from textual.containers import Horizontal, VerticalScroll

class ADViewer(App):
    CSS = """
    Horizontal { width: 100%; height: 100%; }
    Tree { width: 40%; height: 100%; border-right: solid green; }
    VerticalScroll { width: 60%; height: 100%; padding: 1; }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            yield Tree("Objetos AD", id="ad_tree")
            with VerticalScroll(id="right_panel"):
                yield Static("Selecciona un objeto a la izquierda para ver sus atributos.", id="placeholder")
        yield Footer()

    def on_mount(self) -> None:
        tree = self.query_one(Tree)
        
        # Lista de archivos a buscar (no es necesario que sean todos)
        filenames = ['domain_computers.json', 'domain_groups.json', 'domain_policy.json', 'domain_trusts.json', 'domain_users.json']

        for filename in filenames:
            if os.path.exists(filename):
                cat_name = filename.split('.')[0].upper()
                cat_node = tree.root.add(cat_name, expand=False)
                
                with open(filename, 'r', encoding='utf-8') as f:
                    try:
                        data = json.load(f)
                        objects = data.get('data', data) if isinstance(data, dict) else data
                        
                        for obj in objects:
                            attrs = obj.get('attributes', obj)
                            cn = attrs.get('cn', 'Sin CN')
                            
                            if isinstance(cn, list) and len(cn) > 0:
                                label_str = str(cn[0])
                            else:
                                label_str = str(cn)
                                
                            cat_node.add_leaf(label_str, data=obj)
                    except Exception:
                        pass
                        
        tree.root.expand()

    def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        if not event.node.data:
            return

        panel = self.query_one("#right_panel", VerticalScroll)
        panel.query("*").remove()

        pretty_widget = Pretty(event.node.data)
        panel.mount(pretty_widget)

        panel.scroll_home(animate=False)

if __name__ == "__main__":
    app = ADViewer()
    app.run()
