"""
CareerCast Feedback Manager

This module handles user feedback for career predictions
and recommendations.
"""

import json
import os
from datetime import datetime


class FeedbackManager:

    def __init__(self, file_path="feedback/feedback_data.json"):

        self.file_path = file_path

        self.ensure_storage()


    # ========================================================
    # CREATE STORAGE FILE
    # ========================================================

    def ensure_storage(self):

        directory = os.path.dirname(self.file_path)

        if directory:

            os.makedirs(
                directory,
                exist_ok=True
            )

        if not os.path.exists(self.file_path):

            with open(
                self.file_path,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    [],
                    file,
                    indent=4
                )


    # ========================================================
    # LOAD FEEDBACK
    # ========================================================

    def load_feedback(self):

        try:

            with open(
                self.file_path,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

                return data if isinstance(data, list) else []

        except Exception:

            return []


    # ========================================================
    # SAVE FEEDBACK
    # ========================================================

    def save_feedback(self, feedback_data):

        with open(
            self.file_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                feedback_data,
                file,
                indent=4
            )


    # ========================================================
    # ADD FEEDBACK
    # ========================================================

    def add_feedback(self, feedback):

        if not isinstance(feedback, dict):

            raise ValueError(
                "Feedback must be provided as a dictionary."
            )

        feedback_list = self.load_feedback()

        # Create timestamp if not already provided
        if "created_at" not in feedback:

            feedback["created_at"] = datetime.now().isoformat()


        # Ensure important fields exist
        feedback_record = {

            "user_name": feedback.get(
                "user_name",
                "User"
            ),

            "user_email": feedback.get(
                "user_email",
                ""
            ),

            "rating": float(
                feedback.get(
                    "rating",
                    0
                )
            ),

            "predicted_role": feedback.get(
                "predicted_role",
                ""
            ),

            "actual_role": feedback.get(
                "actual_role",
                ""
            ),

            "comments": feedback.get(
                "comments",
                ""
            ),

            "created_at": feedback.get(
                "created_at",
                datetime.now().isoformat()
            )
        }


        feedback_list.append(
            feedback_record
        )


        self.save_feedback(
            feedback_list
        )


        return feedback_record


    # ========================================================
    # GET ALL FEEDBACK
    # ========================================================

    def get_all_feedback(self):

        return self.load_feedback()


    # ========================================================
    # GET USER FEEDBACK
    # ========================================================

    def get_user_feedback(self, user_email):

        feedback_list = self.load_feedback()


        user_feedback = [

            feedback

            for feedback in feedback_list

            if feedback.get(
                "user_email"
            ) == user_email
        ]


        return user_feedback


    # ========================================================
    # DELETE ALL FEEDBACK
    # ========================================================

    def clear_feedback(self):

        self.save_feedback([])

        return True


# ============================================================
# TEST MODULE
# ============================================================

if __name__ == "__main__":

    manager = FeedbackManager()


    test_feedback = {

        "user_name": "Test User",

        "user_email": "test@example.com",

        "rating": 5,

        "predicted_role": "Software Engineer",

        "actual_role": "Software Engineer",

        "comments": "The prediction was accurate."
    }


    manager.add_feedback("""
CareerCast Feedback Manager

This module handles storing and retrieving
user feedback for career predictions.
"""

import json
import os
from datetime import datetime


class FeedbackManager:

    def __init__(self, file_path="feedback/feedback_data.json"):

        self.file_path = file_path

        self.ensure_storage()


    # ========================================================
    # CREATE STORAGE
    # ========================================================

    def ensure_storage(self):

        directory = os.path.dirname(self.file_path)

        if directory:

            os.makedirs(
                directory,
                exist_ok=True
            )


        if not os.path.exists(self.file_path):

            with open(
                self.file_path,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    [],
                    file,
                    indent=4
                )


    # ========================================================
    # LOAD FEEDBACK
    # ========================================================

    def load_feedback(self):

        try:

            with open(
                self.file_path,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

                if isinstance(data, list):

                    return data

                return []

        except Exception:

            return []


    # ========================================================
    # SAVE FEEDBACK
    # ========================================================

    def save_feedback(self, feedback_list):

        with open(
            self.file_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                feedback_list,
                file,
                indent=4,
                ensure_ascii=False
            )


    # ========================================================
    # ADD FEEDBACK
    # ========================================================

    def add_feedback(self, feedback):

        if not isinstance(feedback, dict):

            raise ValueError(
                "Feedback must be provided as a dictionary."
            )


        feedback_list = self.load_feedback()


        # Add timestamp if not already available

        if "created_at" not in feedback:

            feedback["created_at"] = datetime.now().isoformat()


        feedback_list.append(
            feedback
        )


        self.save_feedback(
            feedback_list
        )


        return feedback


    # ========================================================
    # GET ALL FEEDBACK
    # ========================================================

    def get_all_feedback(self):

        return self.load_feedback()


    # ========================================================
    # GET TOTAL FEEDBACK
    # ========================================================

    def get_total_feedback(self):

        feedback_list = self.load_feedback()

        return len(feedback_list)


    # ========================================================
    # GET USER FEEDBACK
    # ========================================================

    def get_user_feedback(self, user_email):

        feedback_list = self.load_feedback()


        user_feedback = [

            feedback

            for feedback in feedback_list

            if feedback.get("user_email") == user_email

        ]


        return user_feedback


    # ========================================================
    # CLEAR ALL FEEDBACK
    # ========================================================

    def clear_feedback(self):

        self.save_feedback([])

        return True


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    manager = FeedbackManager()


    sample_feedback = {

        "user_name": "Test User",

        "user_email": "test@example.com",

        "rating": 5,

        "predicted_role": "Software Engineer",

        "actual_role": "Software Engineer",

        "comments": "The prediction was accurate."

    }


    manager.add_feedback(
        sample_feedback
    )


    print(

        manager.get_all_feedback()

    )
        test_feedback
    )


    print(
        manager.get_all_feedback()
    )