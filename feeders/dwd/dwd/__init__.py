def main():
    """Entry point — deferred to avoid circular imports with dwd_core."""
    from dwd.dwd import main as _main
    _main()

if __name__ == "__main__":
    main()
