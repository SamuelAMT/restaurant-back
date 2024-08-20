for env_file in env_files:
    if env_file.exists():
        print(f"Loading: {env_file}")
        load_dotenv(env_file)
    else:
        print(f"File not found: {env_file}")