"""
CareerCast Feedback Analyzer

This module analyzes user feedback collected
from the CareerCast system.
"""


class FeedbackAnalyzer:

    def __init__(self, feedback_manager):

        self.feedback_manager = feedback_manager


    # ========================================================
    # ANALYZE ALL FEEDBACK
    # ========================================================

    def analyze_feedback(self):

        feedback_list = self.feedback_manager.get_all_feedback()


        # ====================================================
        # NO FEEDBACK
        # ====================================================

        if not feedback_list:

            return {

                "total_feedback": 0,

                "average_rating": 0,

                "correct_predictions": 0,

                "incorrect_predictions": 0,

                "prediction_accuracy": 0,

                "positive_feedback_percentage": 0,

                "feedback_with_actual_role": 0,

                "message": "No feedback available yet."
            }


        # ====================================================
        # VARIABLES
        # ====================================================

        total_feedback = len(feedback_list)

        total_rating = 0

        correct_predictions = 0

        incorrect_predictions = 0

        positive_feedback = 0

        feedback_with_actual_role = 0


        # ====================================================
        # ANALYZE EACH FEEDBACK
        # ====================================================

        for feedback in feedback_list:


            # ------------------------------------------------
            # GET DATA
            # ------------------------------------------------

            rating = feedback.get(
                "rating",
                0
            )

            predicted_role = feedback.get(
                "predicted_role",
                ""
            )

            actual_role = feedback.get(
                "actual_role",
                ""
            )


            # ------------------------------------------------
            # RATING
            # ------------------------------------------------

            try:

                rating = float(rating)

            except (ValueError, TypeError):

                rating = 0


            total_rating += rating


            # ------------------------------------------------
            # POSITIVE FEEDBACK
            # Rating 4 or 5 = Positive
            # ------------------------------------------------

            if rating >= 4:

                positive_feedback += 1


            # ------------------------------------------------
            # PREDICTION ACCURACY
            #
            # Calculate only when the user provides
            # an actual role.
            # ------------------------------------------------

            if actual_role and actual_role.strip():

                feedback_with_actual_role += 1


                if (

                    predicted_role.strip().lower()

                    ==

                    actual_role.strip().lower()

                ):

                    correct_predictions += 1

                else:

                    incorrect_predictions += 1


        # ====================================================
        # CALCULATE AVERAGE RATING
        # ====================================================

        average_rating = round(

            total_rating / total_feedback,

            2

        )


        # ====================================================
        # CALCULATE PREDICTION ACCURACY
        # ====================================================

        if feedback_with_actual_role > 0:

            prediction_accuracy = round(

                (

                    correct_predictions

                    /

                    feedback_with_actual_role

                )

                * 100,

                2

            )

        else:

            prediction_accuracy = 0


        # ====================================================
        # POSITIVE FEEDBACK PERCENTAGE
        # ====================================================

        positive_feedback_percentage = round(

            (

                positive_feedback

                /

                total_feedback

            )

            * 100,

            2

        )


        # ====================================================
        # RETURN ANALYTICS
        # ====================================================

        return {

            "total_feedback":
                total_feedback,

            "average_rating":
                average_rating,

            "correct_predictions":
                correct_predictions,

            "incorrect_predictions":
                incorrect_predictions,

            "prediction_accuracy":
                prediction_accuracy,

            "positive_feedback_percentage":
                positive_feedback_percentage,

            "feedback_with_actual_role":
                feedback_with_actual_role,

            "message":
                "Feedback analysis completed successfully."
        }


    # ========================================================
    # GET MODEL IMPROVEMENT SUGGESTIONS
    # ========================================================

    def get_improvement_suggestions(self):

        analysis = self.analyze_feedback()

        suggestions = []


        # ====================================================
        # NO FEEDBACK
        # ====================================================

        if analysis["total_feedback"] == 0:

            return [

                "No feedback has been collected yet.",

                "Collect user feedback after career predictions.",

                "Use user ratings and actual career roles to evaluate the system."
            ]


        # ====================================================
        # CHECK PREDICTION ACCURACY
        # ====================================================

        accuracy = analysis.get(

            "prediction_accuracy",

            0

        )


        actual_role_count = analysis.get(

            "feedback_with_actual_role",

            0

        )


        if actual_role_count == 0:

            suggestions.append(

                "Ask users to provide their actual or desired career role "
                "to measure prediction accuracy."
            )

        elif accuracy < 50:

            suggestions.append(

                "Prediction accuracy is low. "
                "The career prediction model should be retrained "
                "with more relevant career data."
            )

        elif accuracy < 75:

            suggestions.append(

                "Prediction accuracy can be improved through additional "
                "training data and hyperparameter tuning."
            )

        else:

            suggestions.append(

                "Prediction accuracy is performing well."
            )


        # ====================================================
        # CHECK USER RATING
        # ====================================================

        average_rating = analysis.get(

            "average_rating",

            0

        )


        if average_rating < 3:

            suggestions.append(

                "User satisfaction is low. "
                "Review prediction quality, recommendations "
                "and skill-gap analysis."
            )

        elif average_rating < 4:

            suggestions.append(

                "User satisfaction is moderate. "
                "Improve career recommendations and "
                "skill-gap analysis."
            )

        else:

            suggestions.append(

                "Users are highly satisfied with the system."
            )


        # ====================================================
        # CHECK POSITIVE FEEDBACK
        # ====================================================

        positive_percentage = analysis.get(

            "positive_feedback_percentage",

            0

        )


        if positive_percentage < 60:

            suggestions.append(

                "Increase recommendation quality to improve "
                "positive user feedback."
            )

        elif positive_percentage < 80:

            suggestions.append(

                "Review moderate ratings and user comments "
                "to identify areas for improvement."
            )

        else:

            suggestions.append(

                "Positive feedback is strong. Continue monitoring "
                "user feedback for future improvements."
            )


        # ====================================================
        # RETURN SUGGESTIONS
        # ====================================================

        return suggestions


# ============================================================
# TEST MODULE
# ============================================================

if __name__ == "__main__":

    from feedback.feedback_manager import FeedbackManager


    manager = FeedbackManager()


    analyzer = FeedbackAnalyzer(

        manager

    )


    analysis = analyzer.analyze_feedback()


    print("\n" + "=" * 50)

    print("CAREERCAST FEEDBACK ANALYSIS")

    print("=" * 50)


    print(

        "\nTotal Feedback:",

        analysis["total_feedback"]

    )


    print(

        "Average Rating:",

        analysis["average_rating"]

    )


    print(

        "Correct Predictions:",

        analysis["correct_predictions"]

    )


    print(

        "Incorrect Predictions:",

        analysis["incorrect_predictions"]

    )


    print(

        "Prediction Accuracy:",

        str(analysis["prediction_accuracy"]) + "%"

    )


    print(

        "Positive Feedback:",

        str(

            analysis["positive_feedback_percentage"]

        ) + "%"

    )


    # ========================================================
    # IMPROVEMENT SUGGESTIONS
    # ========================================================

    suggestions = analyzer.get_improvement_suggestions()


    print("\nIMPROVEMENT SUGGESTIONS:\n")


    for suggestion in suggestions:

        print(

            "-",

            suggestion

        )


    print("\n" + "=" * 50)