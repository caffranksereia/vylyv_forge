from vylyv.generator import create_project, TEMPLATES


def ask_yes_no(question: str) -> bool:
    answer = input(f"{question} (y/n): ").strip().lower()
    return answer == "y"


def main():
    print("========================")
    print("      VYLYV FORGE")
    print("========================\n")

    print("Select project template:\n")

    templates = list(TEMPLATES.keys())

    for index, template in enumerate(templates, start=1):
        print(f"{index}. {template}")

    choice = input("\nChoose: ").strip()

    if not choice.isdigit():
        print("Invalid option.")
        return

    index = int(choice) - 1

    if index < 0 or index >= len(templates):
        print("Invalid option.")
        return

    template = templates[index]

    project_name = input("Project name: ").strip()

    install = ask_yes_no("Install dependencies automatically?")
    use_git = ask_yes_no("Initialize git?")

    create_project(
        template=template,
        project_name=project_name,
        install=install,
        use_git=use_git,
    )


if __name__ == "__main__":
    main()