from pathlib import Path

import sass


def compile_scss(input_dir, output_dir):
    input_path = Path(input_dir)
    output_path = Path(output_dir)

    output_path.mkdir(parents=True, exist_ok=True)

    for scss_file in input_path.glob("*.scss"):
        output_file = output_path / (scss_file.stem + ".min.css")

        # The include paths will be the root of the project
        with scss_file.open() as file:
            scss_content = file.read()
            css_content = sass.compile(
                string=scss_content,
                output_style="compressed",
            )

        with output_file.open("w") as css_file:
            css_file.write(css_content)


if __name__ == "__main__":
    compile_scss("bookstore_binht/static/sass", "bookstore_binht/static/css")
