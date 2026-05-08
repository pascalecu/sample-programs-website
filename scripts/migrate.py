from pathlib import Path


def project_section(section: str, bound: str) -> None:
    base_path = Path("archive/projects/")

    for item_path in base_path.iterdir():
        if item_path.is_dir() and item_path.name != "index.md":
            index_file = item_path / "index.md"

            if not index_file.exists():
                continue

            with index_file.open(encoding="utf-8") as f:
                doc = f.readlines()

            try:
                start = doc.index(f"## {section}\n")
                end = doc.index(f"## {bound}\n")
                description = "".join(doc[start + 2: end - 1])

                dest_path = Path(f"sources/projects/{item_path.name}")
                dest_path.mkdir(parents=True, exist_ok=True)

                with (dest_path / f"{section.lower()}.md").open("w", encoding="utf-8") as desc:
                    desc.write(description)
            except ValueError:
                print(f"{item_path.name} has no {section}")
            generate_front_matter(
                index_file,
                Path(f"sources/projects/{item_path.name}/front_matter.yaml"),
            )


def language_section(bound: str) -> None:
    base_path = Path("archive/languages/_posts/")
    if not base_path.exists():
        return

    for post_path in base_path.iterdir():
        if not post_path.is_file():
            continue

        with post_path.open(encoding="utf-8") as f:
            doc = f.readlines()

        try:
            start = doc.index("---\n", 1)
            end = doc.index(f"## {bound}\n")
            description = "".join(doc[start + 2: end - 1])

            lang_name = post_path.stem.split("-")[-1]
            dest_path = Path(f"sources/languages/{lang_name}")
            dest_path.mkdir(parents=True, exist_ok=True)

            with (dest_path / "description.md").open("w", encoding="utf-8") as desc:
                desc.write(description)
        except ValueError:
            print(f"{post_path.name} has no {bound}")
        generate_front_matter(
            post_path,
            Path(f"sources/languages/{post_path.stem.split('-')[-1]}/front_matter.yaml"),
        )


def program_section(section: str, bound: str) -> None:
    projects_base = Path("archive/projects/")

    search_start = f"## {section.lower().replace('the ', '')}\n"
    search_end = f"## {bound.lower().replace('the ', '')}\n"

    for project_dir in projects_base.iterdir():
        if not project_dir.is_dir() or project_dir.name == "index.md":
            continue

        posts_dir = project_dir / "_posts"
        if not posts_dir.exists():
            continue

        for post_path in posts_dir.iterdir():
            if not post_path.is_file() or post_path.suffix != ".md":
                continue

            with post_path.open(encoding="utf-8") as f:
                doc = f.readlines()

            parts = post_path.stem.split("-")
            slug = "-".join(parts[3:]) if len(parts) > 3 else post_path.stem
            dest_dir = Path("sources/programs") / project_dir.name / slug

            lower_copy = [line.lower().replace("the ", "") for line in doc]

            try:
                start = lower_copy.index(search_start)
                end = lower_copy.index(search_end)
                description = "".join(doc[start + 2 : end - 1])

                dest_dir.mkdir(parents=True, exist_ok=True)
                file_name = f"{section.lower().replace(' ', '-')}.md"

                with (dest_dir / file_name).open("w", encoding="utf-8") as desc:
                    desc.write(description)

            except ValueError:
                print(f"{project_dir.name}:{post_path.name} has no {section}")

            generate_front_matter(
                post_path,
                dest_dir / "front_matter.yaml",
            )



def generate_front_matter(input_path: Path, output_path: Path) -> None:
    try:
        with input_path.open(encoding="utf-8") as f:
            doc = f.readlines()

        start = doc.index("---\n")
        end = doc.index("---\n", start + 1)
        front_matter = "".join(doc[start + 1 : end])

        output_path.parent.mkdir(parents=True, exist_ok=True)

        with output_path.open("w", encoding="utf-8") as f:
            f.write(front_matter)
    except ValueError:
        print(f"Warning: {input_path} has no valid YAML front matter")
    except Exception as e:
        print(f"Error processing {input_path}: {e}")


if __name__ == "__main__":
    project_section("Description", "Requirements")
    project_section("Requirements", "Testing")
    project_section("Testing", "Articles")
    language_section("Articles")
    program_section("How to Implement the Solution", "How to Run the Solution")
    program_section("How to Run the Solution", "Further Reading")
