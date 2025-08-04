"""Main GUI window for NiceType settings."""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict
from ..config.manager import config
from ..core.processor import input_processor


class SettingsWindow:
    """Main settings window for NiceType."""
    
    def __init__(self):
        """Initialize the settings window."""
        self.window = tk.Tk()
        self.window.title("NiceType Settings")
        self.window.geometry("600x500")
        self.window.resizable(True, True)
        
        # Variables for checkboxes
        self.enabled_var = tk.BooleanVar(value=config.is_enabled())
        self.punctuation_var = tk.BooleanVar(value=config.is_punctuation_conversion_enabled())
        self.auto_complete_var = tk.BooleanVar(value=config.is_auto_complete_enabled())
        
        self._create_widgets()
        self._load_settings()
    
    def _create_widgets(self):
        """Create and layout the GUI widgets."""
        # Main frame
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Enable/Disable section
        row = 0
        ttk.Label(main_frame, text="General Settings", font=("Arial", 12, "bold")).grid(
            row=row, column=0, columnspan=2, sticky=tk.W, pady=(0, 10)
        )
        
        row += 1
        ttk.Checkbutton(
            main_frame, text="Enable NiceType", variable=self.enabled_var,
            command=self._on_enabled_changed
        ).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=2)
        
        row += 1
        ttk.Checkbutton(
            main_frame, text="Enable Punctuation Conversion", variable=self.punctuation_var,
            command=self._on_punctuation_changed
        ).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=2)
        
        row += 1
        ttk.Checkbutton(
            main_frame, text="Enable Auto-Completion", variable=self.auto_complete_var,
            command=self._on_auto_complete_changed
        ).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=2)
        
        # Punctuation mapping section
        row += 1
        ttk.Separator(main_frame, orient='horizontal').grid(
            row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=20
        )
        
        row += 1
        ttk.Label(main_frame, text="Punctuation Conversion Rules", font=("Arial", 12, "bold")).grid(
            row=row, column=0, columnspan=2, sticky=tk.W, pady=(0, 10)
        )
        
        row += 1
        # Create frame for punctuation mapping
        punct_frame = ttk.Frame(main_frame)
        punct_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        punct_frame.columnconfigure(0, weight=1)
        punct_frame.rowconfigure(0, weight=1)
        
        # Punctuation mapping treeview
        self.punct_tree = ttk.Treeview(punct_frame, columns=("from", "to"), show="headings", height=8)
        self.punct_tree.heading("from", text="From (Chinese)")
        self.punct_tree.heading("to", text="To (English)")
        self.punct_tree.column("from", width=200)
        self.punct_tree.column("to", width=200)
        
        # Scrollbar for punctuation mapping
        punct_scrollbar = ttk.Scrollbar(punct_frame, orient="vertical", command=self.punct_tree.yview)
        self.punct_tree.configure(yscrollcommand=punct_scrollbar.set)
        
        self.punct_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        punct_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Buttons for punctuation mapping
        row += 1
        punct_btn_frame = ttk.Frame(main_frame)
        punct_btn_frame.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        ttk.Button(punct_btn_frame, text="Add Rule", command=self._add_punctuation_rule).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(punct_btn_frame, text="Edit Rule", command=self._edit_punctuation_rule).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(punct_btn_frame, text="Delete Rule", command=self._delete_punctuation_rule).pack(side=tk.LEFT, padx=(0, 5))
        
        # Auto-complete pairs section
        row += 1
        ttk.Separator(main_frame, orient='horizontal').grid(
            row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=20
        )
        
        row += 1
        ttk.Label(main_frame, text="Auto-Completion Pairs", font=("Arial", 12, "bold")).grid(
            row=row, column=0, columnspan=2, sticky=tk.W, pady=(0, 10)
        )
        
        row += 1
        # Create frame for auto-complete pairs
        auto_frame = ttk.Frame(main_frame)
        auto_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        auto_frame.columnconfigure(0, weight=1)
        auto_frame.rowconfigure(0, weight=1)
        
        # Auto-complete pairs treeview
        self.auto_tree = ttk.Treeview(auto_frame, columns=("open", "close"), show="headings", height=6)
        self.auto_tree.heading("open", text="Opening")
        self.auto_tree.heading("close", text="Closing")
        self.auto_tree.column("open", width=200)
        self.auto_tree.column("close", width=200)
        
        # Scrollbar for auto-complete pairs
        auto_scrollbar = ttk.Scrollbar(auto_frame, orient="vertical", command=self.auto_tree.yview)
        self.auto_tree.configure(yscrollcommand=auto_scrollbar.set)
        
        self.auto_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        auto_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Buttons for auto-complete pairs
        row += 1
        auto_btn_frame = ttk.Frame(main_frame)
        auto_btn_frame.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        ttk.Button(auto_btn_frame, text="Add Pair", command=self._add_auto_complete_pair).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(auto_btn_frame, text="Edit Pair", command=self._edit_auto_complete_pair).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(auto_btn_frame, text="Delete Pair", command=self._delete_auto_complete_pair).pack(side=tk.LEFT, padx=(0, 5))
        
        # Bottom buttons
        row += 1
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=20)
        
        ttk.Button(bottom_frame, text="Save & Apply", command=self._save_settings).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(bottom_frame, text="Reset to Defaults", command=self._reset_to_defaults).pack(side=tk.RIGHT)
        
        # Configure row weights for expansion
        main_frame.rowconfigure(row-3, weight=1)  # Punctuation mapping area
        main_frame.rowconfigure(row-1, weight=1)  # Auto-complete pairs area
    
    def _load_settings(self):
        """Load current settings into the GUI."""
        self._load_punctuation_mapping()
        self._load_auto_complete_pairs()
    
    def _load_punctuation_mapping(self):
        """Load punctuation mapping into the treeview."""
        # Clear existing items
        for item in self.punct_tree.get_children():
            self.punct_tree.delete(item)
        
        # Add current mappings
        mapping = config.get_punctuation_mapping()
        for from_chars, to_char in mapping.items():
            self.punct_tree.insert("", "end", values=(from_chars, to_char))
    
    def _load_auto_complete_pairs(self):
        """Load auto-complete pairs into the treeview."""
        # Clear existing items
        for item in self.auto_tree.get_children():
            self.auto_tree.delete(item)
        
        # Add current pairs
        pairs = config.get_auto_complete_pairs()
        for open_char, close_char in pairs.items():
            self.auto_tree.insert("", "end", values=(open_char, close_char))
    
    def _on_enabled_changed(self):
        """Handle enabled checkbox change."""
        config.set_enabled(self.enabled_var.get())
    
    def _on_punctuation_changed(self):
        """Handle punctuation conversion checkbox change."""
        config.set_punctuation_conversion_enabled(self.punctuation_var.get())
    
    def _on_auto_complete_changed(self):
        """Handle auto-complete checkbox change."""
        config.set_auto_complete_enabled(self.auto_complete_var.get())
    
    def _add_punctuation_rule(self):
        """Add a new punctuation conversion rule."""
        dialog = PunctuationRuleDialog(self.window, "Add Punctuation Rule")
        if dialog.result:
            from_chars, to_char = dialog.result
            # Check if rule already exists
            mapping = config.get_punctuation_mapping()
            if from_chars in mapping:
                messagebox.showwarning("Duplicate Rule", f"Rule for '{from_chars}' already exists.")
                return
            
            mapping[from_chars] = to_char
            config.set_punctuation_mapping(mapping)
            self._load_punctuation_mapping()
    
    def _edit_punctuation_rule(self):
        """Edit selected punctuation conversion rule."""
        selection = self.punct_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a rule to edit.")
            return
        
        item = selection[0]
        values = self.punct_tree.item(item, "values")
        from_chars, to_char = values
        
        dialog = PunctuationRuleDialog(self.window, "Edit Punctuation Rule", from_chars, to_char)
        if dialog.result:
            new_from_chars, new_to_char = dialog.result
            mapping = config.get_punctuation_mapping()
            
            # Remove old rule if key changed
            if new_from_chars != from_chars:
                del mapping[from_chars]
            
            mapping[new_from_chars] = new_to_char
            config.set_punctuation_mapping(mapping)
            self._load_punctuation_mapping()
    
    def _delete_punctuation_rule(self):
        """Delete selected punctuation conversion rule."""
        selection = self.punct_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a rule to delete.")
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this rule?"):
            item = selection[0]
            values = self.punct_tree.item(item, "values")
            from_chars = values[0]
            
            mapping = config.get_punctuation_mapping()
            if from_chars in mapping:
                del mapping[from_chars]
                config.set_punctuation_mapping(mapping)
                self._load_punctuation_mapping()
    
    def _add_auto_complete_pair(self):
        """Add a new auto-complete pair."""
        dialog = AutoCompletePairDialog(self.window, "Add Auto-Complete Pair")
        if dialog.result:
            open_char, close_char = dialog.result
            # Check if pair already exists
            pairs = config.get_auto_complete_pairs()
            if open_char in pairs:
                messagebox.showwarning("Duplicate Pair", f"Pair for '{open_char}' already exists.")
                return
            
            pairs[open_char] = close_char
            config.set_auto_complete_pairs(pairs)
            self._load_auto_complete_pairs()
    
    def _edit_auto_complete_pair(self):
        """Edit selected auto-complete pair."""
        selection = self.auto_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a pair to edit.")
            return
        
        item = selection[0]
        values = self.auto_tree.item(item, "values")
        open_char, close_char = values
        
        dialog = AutoCompletePairDialog(self.window, "Edit Auto-Complete Pair", open_char, close_char)
        if dialog.result:
            new_open_char, new_close_char = dialog.result
            pairs = config.get_auto_complete_pairs()
            
            # Remove old pair if key changed
            if new_open_char != open_char:
                del pairs[open_char]
            
            pairs[new_open_char] = new_close_char
            config.set_auto_complete_pairs(pairs)
            self._load_auto_complete_pairs()
    
    def _delete_auto_complete_pair(self):
        """Delete selected auto-complete pair."""
        selection = self.auto_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a pair to delete.")
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this pair?"):
            item = selection[0]
            values = self.auto_tree.item(item, "values")
            open_char = values[0]
            
            pairs = config.get_auto_complete_pairs()
            if open_char in pairs:
                del pairs[open_char]
                config.set_auto_complete_pairs(pairs)
                self._load_auto_complete_pairs()
    
    def _save_settings(self):
        """Save all settings to configuration file."""
        config.save()
        messagebox.showinfo("Settings Saved", "Settings have been saved successfully.")
    
    def _reset_to_defaults(self):
        """Reset all settings to defaults."""
        if messagebox.askyesno("Reset to Defaults", "Are you sure you want to reset all settings to defaults?"):
            config._config = config._load_default_config()
            self.enabled_var.set(config.is_enabled())
            self.punctuation_var.set(config.is_punctuation_conversion_enabled())
            self.auto_complete_var.set(config.is_auto_complete_enabled())
            self._load_settings()
    
    def run(self):
        """Start the GUI main loop."""
        self.window.mainloop()
    
    def destroy(self):
        """Destroy the window."""
        self.window.destroy()


class PunctuationRuleDialog:
    """Dialog for adding/editing punctuation conversion rules."""
    
    def __init__(self, parent, title, from_chars="", to_char=""):
        """Initialize the dialog."""
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x200")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (200 // 2)
        self.dialog.geometry(f"400x200+{x}+{y}")
        
        # Create widgets
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # From characters
        ttk.Label(main_frame, text="From (e.g., '，，'):").pack(anchor=tk.W, pady=(0, 5))
        self.from_entry = ttk.Entry(main_frame, width=30)
        self.from_entry.pack(fill=tk.X, pady=(0, 10))
        self.from_entry.insert(0, from_chars)
        
        # To character
        ttk.Label(main_frame, text="To (e.g., ','):").pack(anchor=tk.W, pady=(0, 5))
        self.to_entry = ttk.Entry(main_frame, width=30)
        self.to_entry.pack(fill=tk.X, pady=(0, 20))
        self.to_entry.insert(0, to_char)
        
        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X)
        
        ttk.Button(btn_frame, text="Cancel", command=self._cancel).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(btn_frame, text="OK", command=self._ok).pack(side=tk.RIGHT)
        
        # Focus on first entry
        self.from_entry.focus()
        
        # Wait for dialog to close
        self.dialog.wait_window()
    
    def _ok(self):
        """Handle OK button."""
        from_chars = self.from_entry.get().strip()
        to_char = self.to_entry.get().strip()
        
        if not from_chars or not to_char:
            messagebox.showwarning("Invalid Input", "Both fields are required.")
            return
        
        if len(from_chars) != 2:
            messagebox.showwarning("Invalid Input", "From field must be exactly 2 characters.")
            return
        
        if len(to_char) != 1:
            messagebox.showwarning("Invalid Input", "To field must be exactly 1 character.")
            return
        
        self.result = (from_chars, to_char)
        self.dialog.destroy()
    
    def _cancel(self):
        """Handle Cancel button."""
        self.dialog.destroy()


class AutoCompletePairDialog:
    """Dialog for adding/editing auto-complete pairs."""
    
    def __init__(self, parent, title, open_char="", close_char=""):
        """Initialize the dialog."""
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x200")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (200 // 2)
        self.dialog.geometry(f"400x200+{x}+{y}")
        
        # Create widgets
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Opening character
        ttk.Label(main_frame, text="Opening character (e.g., '('):").pack(anchor=tk.W, pady=(0, 5))
        self.open_entry = ttk.Entry(main_frame, width=30)
        self.open_entry.pack(fill=tk.X, pady=(0, 10))
        self.open_entry.insert(0, open_char)
        
        # Closing character
        ttk.Label(main_frame, text="Closing character (e.g., ')'):").pack(anchor=tk.W, pady=(0, 5))
        self.close_entry = ttk.Entry(main_frame, width=30)
        self.close_entry.pack(fill=tk.X, pady=(0, 20))
        self.close_entry.insert(0, close_char)
        
        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X)
        
        ttk.Button(btn_frame, text="Cancel", command=self._cancel).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(btn_frame, text="OK", command=self._ok).pack(side=tk.RIGHT)
        
        # Focus on first entry
        self.open_entry.focus()
        
        # Wait for dialog to close
        self.dialog.wait_window()
    
    def _ok(self):
        """Handle OK button."""
        open_char = self.open_entry.get().strip()
        close_char = self.close_entry.get().strip()
        
        if not open_char or not close_char:
            messagebox.showwarning("Invalid Input", "Both fields are required.")
            return
        
        if len(open_char) != 1:
            messagebox.showwarning("Invalid Input", "Opening character must be exactly 1 character.")
            return
        
        if len(close_char) != 1:
            messagebox.showwarning("Invalid Input", "Closing character must be exactly 1 character.")
            return
        
        self.result = (open_char, close_char)
        self.dialog.destroy()
    
    def _cancel(self):
        """Handle Cancel button."""
        self.dialog.destroy()