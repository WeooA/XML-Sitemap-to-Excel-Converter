# Sitemap HTML to Excel Converter

A Python tool with GUI interface to convert HTML sitemaps into structured Excel files. Supports multiple sitemap formats including xml-sitemaps.com, standard HTML sitemaps, and WordPress sitemaps.

## Requirements

Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

Required packages:
- beautifulsoup4>=4.9.3
- pandas>=1.3.0
- openpyxl>=3.0.7
- tkinter (usually comes with Python)

## Installation

1. Clone or download this repository
2. Install the requirements:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### GUI Method
Run the GUI application:
```bash
python sitemap_gui.py
```

1. Click "Browse" to select your HTML sitemap file
2. Enter desired output filename (default: sitemap.xlsx)
3. Click "Convert to Excel"
4. The Excel file will be saved in the same directory as the input HTML file

### Command Line Method
You can also use the script directly from command line:
```bash
python generate_sitemap.py input_sitemap.html output_filename.xlsx
```

## Features

- GUI interface for easy use
- Supports multiple sitemap formats
- Automatic format detection
- Hierarchical structure preservation
- Duplicate URL removal
- Clean title formatting
- Section path tracking
- Error handling and status messages

## Output Format

The generated Excel file contains the following columns:
- Section: Full hierarchical path
- Level: Depth level in sitemap
- Parent: Parent page/section
- Title: Page title
- URL: Full page URL

## Supported Formats

- xml-sitemaps.com format (Recommended)
- Standard HTML sitemaps
- WordPress sitemaps
- Auto-detection for other formats

## Troubleshooting

If you encounter issues:
1. Ensure all requirements are installed
2. Check if the HTML file is properly formatted
3. Check console output for detailed error messages

## License

MIT License - Feel free to use and modify as needed.
