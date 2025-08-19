from bs4 import BeautifulSoup
import pandas as pd

class SitemapFormat:
    """Configuration for different sitemap formats"""
    def __init__(self, name, root_selector, section_class="lhead", 
                 level_class_prefix="level-", title_cleanup=None):
        self.name = name
        self.root_selector = root_selector
        self.section_class = section_class
        self.level_class_prefix = level_class_prefix
        self.title_cleanup = title_cleanup or []

# Common sitemap formats
SITEMAP_FORMATS = [
    SitemapFormat("xml-sitemaps.com", "ul.level-0", "lhead", "level-", 
                  ["– Website Name"]),
    SitemapFormat("standard", "ul.sitemap", "section", "level",
                  ["- Home", "| Site Map"]),
    SitemapFormat("wordpress", "ul#sitemap", "heading", "depth"),
]

def detect_sitemap_format(soup):
    """Detect which sitemap format we're dealing with"""
    for fmt in SITEMAP_FORMATS:
        if soup.select(fmt.root_selector):
            return fmt
            
    # Try to auto-detect format
    classes_found = set()
    for ul in soup.find_all("ul"):
        if ul.get("class"):
            classes_found.update(ul.get("class"))
    
    # Look for common patterns
    if any("level" in c for c in classes_found):
        return SITEMAP_FORMATS[0]  # xml-sitemaps format
    if any("sitemap" in c for c in classes_found):
        return SITEMAP_FORMATS[1]  # standard format
    
    return SITEMAP_FORMATS[0]  # default to xml-sitemaps format

def parse_list(ul, level=0, parent="", data=None, current_section="", parent_sections=None, format_config=None):
    """Recursive parser for extracting sitemap structure"""
    if data is None:
        data = []
    if parent_sections is None:
        parent_sections = []
    if format_config is None:
        format_config = SITEMAP_FORMATS[0]
    
    # Find all direct <li> children
    for li in ul.find_all("li", recursive=False):
        # Check for section header using configured class
        if format_config.section_class in li.get("class", []):
            section_text = li.text.strip()
            # Remove any span elements (like page counts)
            if "<span" in str(li):
                section_text = section_text.split("<span")[0].strip()
            section_text = section_text.rstrip('/ ')
            
            # Build section path
            if level == 0:
                current_section = section_text
                parent_sections = [section_text]
            else:
                current_section = section_text
                if len(parent_sections) > level:
                    parent_sections = parent_sections[:level]
                parent_sections.append(section_text)
            continue
            
        link = li.find("a")
        if link:
            title = link.text.strip()
            # Remove redundant "– Top Treasures" from titles
            title = title.replace("– Top Treasures", "").strip()
            url = link.get("href", "")
            
            # Skip if URL is empty or just a hash
            if url and url != "#":
                # Use full section path
                full_section = " > ".join(parent_sections) if parent_sections else ""
                data.append({
                    "Level": level,
                    "Section": full_section,
                    "Parent": parent,
                    "Title": title,
                    "URL": url
                })
        
        # Look for sub-lists with explicit level classes
        sub_uls = li.find_all("ul", class_=lambda x: x and "level-" in x)
        for sub_ul in sub_uls:
            # Extract level from class name
            sub_level = int(sub_ul.get("class")[0].split("-")[1])
            parse_list(sub_ul, sub_level, title if link else parent, 
                      data, current_section, parent_sections.copy(), format_config)
    
    return data

def debug_html_structure(soup):
    """Debug function to understand the HTML structure"""
    print("=== HTML STRUCTURE DEBUG ===")
    
    # Look for all ul elements
    all_uls = soup.find_all("ul")
    print(f"Total <ul> elements found: {len(all_uls)}")
    
    # Check for different class patterns
    classes_found = set()
    for ul in all_uls:
        if ul.get("class"):
            classes_found.update(ul.get("class"))
    
    print(f"UL classes found: {classes_found}")
    
    # Look for the main sitemap container
    possible_roots = []
    
    # Try different selectors
    selectors_to_try = [
        "ul.level-0",
        "ul[class*='level']",
        "ul[class*='sitemap']",
        "ul[class*='menu']",
        "div.sitemap ul",
        "nav ul",
        ".sitemap ul",
        "ul:first-of-type"
    ]
    
    for selector in selectors_to_try:
        elements = soup.select(selector)
        if elements:
            possible_roots.append((selector, len(elements)))
    
    print("Possible root elements:")
    for selector, count in possible_roots:
        print(f"  {selector}: {count} elements")
    
    # Show first few li elements for inspection
    all_lis = soup.find_all("li")
    print(f"\nTotal <li> elements found: {len(all_lis)}")
    print("First 3 <li> elements:")
    for i, li in enumerate(all_lis[:3]):
        print(f"  {i+1}: {li}")
    
    return all_uls

def find_sitemap_root(soup):
    """Try to find the sitemap root element using various strategies"""
    
    # Look for ul with class level-0 (primary strategy for this format)
    root = soup.find("ul", class_="level-0")
    if root:
        return root, "ul.level-0"
    
    # Strategy 2: Look for ul with any level class
    root = soup.find("ul", class_=lambda x: x and "level" in " ".join(x))
    if root:
        return root, "ul with level class"
    
    # Strategy 3: Look for ul inside sitemap container
    sitemap_container = soup.find("div", class_=lambda x: x and "sitemap" in " ".join(x))
    if sitemap_container:
        root = sitemap_container.find("ul")
        if root:
            return root, "ul inside sitemap container"
    
    # Strategy 4: Find the largest ul (likely the main menu/sitemap)
    all_uls = soup.find_all("ul")
    if all_uls:
        # Sort by number of child li elements
        largest_ul = max(all_uls, key=lambda ul: len(ul.find_all("li")))
        if len(largest_ul.find_all("li")) > 0:
            return largest_ul, "largest ul by li count"
    
    # Strategy 5: Look for ul with most nested structure
    for ul in all_uls:
        if ul.find("ul"):  # Has nested ul
            return ul, "ul with nested structure"
    
    return None, "No suitable root found"

def generate_sitemap_excel(html_file, output_file="sitemap.xlsx"):
    # Load sitemap file
    with open(html_file, "r", encoding="utf-8") as f:
        content = f.read()
        soup = BeautifulSoup(content, "html.parser")
    
    # Detect sitemap format
    format_config = detect_sitemap_format(soup)
    
    # Find root element using format-specific selector
    root_ul = soup.select_one(format_config.root_selector)
    if not root_ul:
        raise ValueError(f"Could not find root element using selector: {format_config.root_selector}")
    
    # Parse sitemap with format configuration
    sitemap_data = parse_list(root_ul, format_config=format_config)
    
    # Clean up titles using format-specific patterns
    for item in sitemap_data:
        title = item["Title"]
        for cleanup in format_config.title_cleanup:
            title = title.replace(cleanup, "").strip()
        item["Title"] = title
    
    # Remove duplicates while preserving order and sort by section
    seen = set()
    unique_data = []
    for item in sitemap_data:
        url = item["URL"]
        if url not in seen:
            seen.add(url)
            unique_data.append(item)
    
    # Sort data by full section path, then by Level
    sorted_data = sorted(unique_data, 
                        key=lambda x: (
                            [s.strip() for s in x["Section"].split(" > ")] if x["Section"] else [],
                            x["Level"], 
                            x["Title"].lower()
                        ))
    
    # Convert to DataFrame and save
    df = pd.DataFrame(sorted_data)
    
    # Reorder columns to put Section first
    columns = ["Section", "Level", "Parent", "Title", "URL"]
    df = df[columns]
    
    df.to_excel(output_file, index=False)
    print(f"\nSitemap saved to {output_file}")
    print(f"Total unique entries: {len(df)}")
    print(f"Sections found: {sorted(df['Section'].unique())}")
    print(f"Levels found: {sorted(df['Level'].unique())}")
