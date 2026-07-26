import sys
from pathlib import Path

from block_splitters import markdown_to_html_node
from textnode import TextNode, TextType


def extract_title(markdown):
    lines = markdown.splitlines()
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#") and not stripped.startswith("##"):
            title = stripped[1:].strip()
            if title:
                return title
    raise ValueError("No h1 header found in markdown")


def generate_page(from_path, template_path, dest_path, basepath="/"):
    from_path = Path(from_path)
    template_path = Path(template_path)
    dest_path = Path(dest_path)

    print(f"Generating page from `{from_path}` to `{dest_path}` using `{template_path}`")

    markdown = from_path.read_text(encoding="utf-8")
    template = template_path.read_text(encoding="utf-8")

    html_content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    full_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html_content)
    full_html = full_html.replace('href="/', f'href="{basepath}')
    full_html = full_html.replace('src="/', f'src="{basepath}')

    dest_path.parent.mkdir(parents=True, exist_ok=True)
    dest_path.write_text(full_html, encoding="utf-8")
    return full_html


def copy_directory_contents(source_dir, destination_dir):
    source_path = Path(source_dir)
    destination_path = Path(destination_dir)

    if not source_path.exists():
        raise FileNotFoundError(f"Source directory does not exist: {source_path}")

    destination_path.mkdir(parents=True, exist_ok=True)

    def clear_directory(path):
        for child in path.iterdir():
            if child.is_dir():
                clear_directory(child)
                child.rmdir()
            else:
                child.unlink()

    clear_directory(destination_path)

    def copy_contents(source_path, destination_path):
        for child in source_path.iterdir():
            target_path = destination_path / child.name
            if child.is_dir():
                target_path.mkdir(parents=True, exist_ok=True)
                copy_contents(child, target_path)
            else:
                with child.open("rb") as source_file, target_path.open("wb") as target_file:
                    target_file.write(source_file.read())
                print(f"Copied {child} -> {target_path}")

    copy_contents(source_path, destination_path)
    return destination_path


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    output_dir = "docs"

    text_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(text_node)
    copy_directory_contents("static", output_dir)

    pages = [
        ("content/index.md", f"{output_dir}/index.html"),
        ("content/blog/glorfindel/index.md", f"{output_dir}/blog/glorfindel/index.html"),
        ("content/blog/tom/index.md", f"{output_dir}/blog/tom/index.html"),
        ("content/blog/majesty/index.md", f"{output_dir}/blog/majesty/index.html"),
        ("content/contact/index.md", f"{output_dir}/contact/index.html"),
    ]

    for from_path, dest_path in pages:
        generate_page(from_path, "template.html", dest_path, basepath)


if __name__ == "__main__":
    main()
