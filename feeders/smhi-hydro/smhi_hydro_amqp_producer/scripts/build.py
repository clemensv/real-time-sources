"""
Build script for smhi_hydro_amqp_producer_amqp_producer
"""
import subprocess
import sys

def main():
    """Main build function"""
    print("Building smhi_hydro_amqp_producer_amqp_producer...")
    
    try:
        # Install dependencies
        subprocess.run(["poetry", "install"], check=True)
        
        # Run tests
        print("\nRunning tests...")
        subprocess.run(["poetry", "run", "pytest"], check=True)
        
        # Build package
        print("\nBuilding package...")
        subprocess.run(["poetry", "build"], check=True)
        
        print("\n✓ Build complete!")
        return 0
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Build failed: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())