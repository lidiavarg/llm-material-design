from src import extract, clean, tokenize, training

def main():
    print("Starting LLM pipeline...\n")

    print("Step 1: Extracting raw text...")
    extract.run()
    print("Text extraction completed.\n")

    print("Step 2: Cleaning text...")
    clean.run()
    print("Text cleaning completed.\n")

    print("Step 3: Tokenizing...")
    tokenize.run()
    print("Tokenization completed.\n")
    
    print("Step 4: Training...")
    training.run()
    print("Training completed.\n")

    print("All steps completed successfully!")

if __name__ == "__main__":
    main()
