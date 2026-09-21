"""
CareerCast Command Line Interface

Provides CLI commands for:
- Career prediction
- Career recommendations
- Model information
- Version information
"""

import argparse
import os

from . import __version__
from .parser import extract_resume_text
from .predictor import predict_top_k, get_model_information
from .recommender import get_career_recommendations


def read_resume(file_path):
    """
    Read resume text from PDF, DOCX, or TXT file.

    Parameters
    ----------
    file_path : str
        Path to the resume file.

    Returns
    -------
    str
        Extracted resume text.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    ValueError
        If the file format is unsupported.
    """
    if not file_path:
        raise ValueError("Resume file path is required.")

    file_path = os.path.abspath(file_path)

    if not os.path.isfile(file_path):
        raise FileNotFoundError(
            f"Resume file not found: {file_path}"
        )

    extension = os.path.splitext(file_path)[1].lower()

    if extension not in {".pdf", ".docx", ".txt"}:
        raise ValueError(
            "Unsupported file format. "
            "Please upload PDF, DOCX or TXT."
        )

    try:
        with open(file_path, "rb") as resume_file:
            text = extract_resume_text(resume_file)

        if not text or not text.strip():
            raise ValueError(
                "Could not extract any text from the resume."
            )

        return text

    except ValueError:
        raise

    except Exception as exc:
        raise RuntimeError(
            f"Could not read resume: {exc}"
        ) from exc


def command_predict(args):
    """Handle the predict command."""

    print("\n" + "=" * 55)
    print("CareerCast Career Prediction")
    print("=" * 55)

    try:
        resume_text = read_resume(args.resume)

        result = predict_top_k(
            resume_text=resume_text,
            model_name=args.model,
            top_k=args.top_k
        )

        if not result:
            print("\nNo career predictions were generated.")
            return 1

        print("\nPredicted Career Roles:")
        print("-" * 55)

        for prediction in result:
            role = prediction.get("role", "Unknown")
            confidence = prediction.get(
                "confidence_percentage",
                prediction.get("confidence", 0)
            )

            if isinstance(confidence, (int, float)):
                if confidence <= 1:
                    confidence *= 100

            print(f"{prediction.get('rank', '')}. {role}")
            print(f"   Confidence: {confidence:.2f}%")

        print()

        return 0

    except Exception as exc:
        print(f"\nError: {exc}")
        return 1


def command_recommend(args):
    """Handle the recommend command."""

    print("\n" + "=" * 55)
    print("CareerCast Career Recommendations")
    print("=" * 55)

    try:
        resume_text = read_resume(args.resume)

        recommendations = get_career_recommendations(
            resume_text=resume_text,
            top_k=args.top_k,
            model_name=args.model
        )

        if not recommendations:
            print("\nNo career recommendations were generated.")
            return 1

        print("\nRecommended Career Paths:")
        print("-" * 55)

        for recommendation in recommendations:
            role = recommendation.get("role", "Unknown")
            confidence = recommendation.get(
                "confidence_percentage",
                recommendation.get("confidence", 0)
            )

            if isinstance(confidence, (int, float)):
                if confidence <= 1:
                    confidence *= 100

            print(f"{recommendation.get('rank', '')}. {role}")
            print(f"   Confidence: {confidence:.2f}%")

            description = recommendation.get("description")
            if description:
                print(f"   {description}")

        print()

        return 0

    except Exception as exc:
        print(f"\nError: {exc}")
        return 1


def command_model_info(args):
    """Handle the model-info command."""

    print("\n" + "=" * 55)
    print("CareerCast Model Information")
    print("=" * 55)

    try:
        information = get_model_information()

        for key, value in information.items():
            print(f"{key}: {value}")

        print()

        return 0

    except Exception as exc:
        print(f"\nError: {exc}")
        return 1


def command_version(args):
    """Handle the version command."""

    print(f"CareerCast version {__version__}")
    return 0


def build_parser():
    """Build the CareerCast CLI argument parser."""

    parser = argparse.ArgumentParser(
        prog="careercast",
        description=(
            "CareerCast - AI-Powered Career Intelligence Platform"
        )
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )

    subparsers = parser.add_subparsers(
        dest="command"
    )

    # --------------------------------------------------------
    # PREDICT
    # --------------------------------------------------------

    predict_parser = subparsers.add_parser(
        "predict",
        help="Predict career roles from a resume."
    )

    predict_parser.add_argument(
        "resume",
        help="Path to PDF, DOCX, or TXT resume."
    )

    predict_parser.add_argument(
        "--model",
        choices=[
            "xgboost",
            "random_forest",
            "role_classifier"
        ],
        default="xgboost",
        help="Model to use for prediction."
    )

    predict_parser.add_argument(
        "--top-k",
        type=int,
        default=5,
        help="Number of career predictions to display."
    )

    predict_parser.set_defaults(
        func=command_predict
    )

    # --------------------------------------------------------
    # RECOMMEND
    # --------------------------------------------------------

    recommend_parser = subparsers.add_parser(
        "recommend",
        help="Generate Top-K career recommendations."
    )

    recommend_parser.add_argument(
        "resume",
        help="Path to PDF, DOCX, or TXT resume."
    )

    recommend_parser.add_argument(
        "--model",
        choices=[
            "xgboost",
            "random_forest",
            "role_classifier"
        ],
        default="xgboost",
        help="Model to use."
    )

    recommend_parser.add_argument(
        "--top-k",
        type=int,
        default=5,
        help="Number of recommendations to display."
    )

    recommend_parser.set_defaults(
        func=command_recommend
    )

    # --------------------------------------------------------
    # MODEL INFO
    # --------------------------------------------------------

    model_parser = subparsers.add_parser(
        "model-info",
        help="Display CareerCast model information."
    )

    model_parser.set_defaults(
        func=command_model_info
    )

    # --------------------------------------------------------
    # VERSION
    # --------------------------------------------------------

    version_parser = subparsers.add_parser(
        "version",
        help="Display CareerCast version."
    )

    version_parser.set_defaults(
        func=command_version
    )

    return parser


def main(argv=None):
    """CLI entry point."""

    parser = build_parser()
    args = parser.parse_args(argv)

    if not hasattr(args, "func"):
        parser.print_help()
        return 0

    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())