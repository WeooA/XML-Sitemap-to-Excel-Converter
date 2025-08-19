import tkinter as tk
from tkinter import filedialog, messagebox
import os
from generate_sitemap import generate_sitemap_excel

class SitemapConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sitemap HTML to Excel Converter")
        self.root.geometry("600x300")
        
        # Create main frame with padding
        main_frame = tk.Frame(root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # File selection
        self.file_frame = tk.LabelFrame(main_frame, text="Input HTML File", padx=10, pady=10)
        self.file_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.file_path = tk.StringVar()
        self.file_entry = tk.Entry(self.file_frame, textvariable=self.file_path, width=50)
        self.file_entry.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
        
        self.browse_btn = tk.Button(self.file_frame, text="Browse", command=self.browse_file)
        self.browse_btn.pack(side=tk.RIGHT)
        
        # Output filename
        self.name_frame = tk.LabelFrame(main_frame, text="Output Excel Filename", padx=10, pady=10)
        self.name_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.output_name = tk.StringVar(value="sitemap.xlsx")
        self.name_entry = tk.Entry(self.name_frame, textvariable=self.output_name, width=50)
        self.name_entry.pack(fill=tk.X)
        
        # Status message
        self.status_var = tk.StringVar()
        self.status_label = tk.Label(main_frame, textvariable=self.status_var, wraplength=500)
        self.status_label.pack(fill=tk.X, pady=(0, 10))
        
        # Convert button
        self.convert_btn = tk.Button(main_frame, text="Convert to Excel", command=self.convert_sitemap)
        self.convert_btn.pack(pady=10)

    def browse_file(self):
        filename = filedialog.askopenfilename(
            title="Select HTML Sitemap",
            filetypes=[("HTML files", "*.html"), ("All files", "*.*")]
        )
        if filename:
            self.file_path.set(filename)

    def convert_sitemap(self):
        html_file = self.file_path.get()
        output_name = self.output_name.get()
        
        if not html_file:
            messagebox.showerror("Error", "Please select an HTML file first!")
            return
            
        if not output_name.endswith('.xlsx'):
            output_name += '.xlsx'
            
        try:
            self.status_var.set("Converting... Please wait.")
            self.root.update()
            
            # Get the directory of the input file
            output_dir = os.path.dirname(html_file)
            output_path = os.path.join(output_dir, output_name)
            
            # Generate the Excel file
            generate_sitemap_excel(html_file, output_path)
            
            self.status_var.set(f"Success! Excel file saved as: {output_name}")
            messagebox.showinfo("Success", f"Sitemap has been converted and saved as:\n{output_path}")
            
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")

def main():
    root = tk.Tk()
    app = SitemapConverterGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
