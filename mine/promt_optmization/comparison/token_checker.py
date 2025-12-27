import argparse

from transformers import AutoTokenizer


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Count RoBERTa MNLI tokens for a pair of text files."
    )
    parser.add_argument(
        "--dir",
        default="./TOC_generation(analyze)/",
        help="Directory containing the files (default: ./TOC_generation(analyze)/)",
    )
    parser.add_argument("--a", default="optimized.md", help="First filename (premise).")
    parser.add_argument(
        "--b", default="unoptimized-1.md", help="Second filename (hypothesis)."
    )
    args = parser.parse_args()

    tok = AutoTokenizer.from_pretrained("roberta-large-mnli")

    with open(f"{args.dir}{args.a}") as f:
        a_text = f.read()
    with open(f"{args.dir}{args.b}") as f:
        b_text = f.read()

    enc = tok(a_text, b_text, return_tensors="pt", truncation=False)
    print("Total tokens:", enc["input_ids"].shape[1])
    print("Tokenizer max length:", tok.model_max_length)


if __name__ == "__main__":
    main()
