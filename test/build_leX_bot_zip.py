import os, json, zipfile

# === Directory layout ===
base_dir = "CourseDegreePlannerBot"
os.makedirs(base_dir + "/bot", exist_ok=True)
os.makedirs(base_dir + "/intents", exist_ok=True)
os.makedirs(base_dir + "/slotTypes", exist_ok=True)

lambda_arn = "arn:aws:lambda:us-east-1:482849671789:function:course-degree-planner-LF1Fulfillment-JKIVOOCy436S"

# === Slot type TargetTerm ===
slot_type = {
    "name": "TargetTerm",
    "description": "Academic terms",
    "enumerationValues": [{"value": v} for v in ["Winter", "Summer", "Fall"]],
    "valueSelectionStrategy": "ORIGINAL_VALUE"
}
with open(f"{base_dir}/slotTypes/TargetTerm.json", "w") as f:
    json.dump(slot_type, f, indent=2)

# === Intent 1: CheckPrerequisites ===
check_prereq = {
    "name": "CheckPrerequisites",
    "sampleUtterances": [
        "Do I meet the prerequisites for {course_code}?",
        "Am I eligible for {course_code}?"
    ],
    "slots": [{
        "name": "course_code",
        "slotConstraint": "Required",
        "slotType": "AMAZON.AlphaNumeric",
        "slotTypeVersion": "$LATEST",
        "valueElicitationPrompt": {
            "maxAttempts": 2,
            "messages": [{"contentType": "PlainText",
                          "content": "What course code are you asking about?"}]
        },
        "priority": 1
    }],
    "dialogCodeHook": {"uri": lambda_arn, "messageVersion": "1.0"},
    "fulfillmentActivity": {"type": "CodeHook",
                            "codeHook": {"uri": lambda_arn, "messageVersion": "1.0"}}
}
with open(f"{base_dir}/intents/CheckPrerequisites.json", "w") as f:
    json.dump(check_prereq, f, indent=2)

# === Intent 2: RecommendSchedule ===
recommend_schedule = {
    "name": "RecommendSchedule",
    "sampleUtterances": [
        "I have {credits_completed} out of 30. What should I take next?",
        "Suggest 2 or 3 courses for next term."
    ],
    "slots": [
        {
            "name": "credits_completed",
            "slotConstraint": "Required",
            "slotType": "AMAZON.NUMBER",
            "slotTypeVersion": "$LATEST",
            "valueElicitationPrompt": {
                "maxAttempts": 2,
                "messages": [{"contentType": "PlainText",
                              "content": "How many credits have you completed so far?"}]
            },
            "priority": 1
        },
        {
            "name": "target_term",
            "slotConstraint": "Optional",
            "slotType": "TargetTerm",
            "slotTypeVersion": "$LATEST",
            "valueElicitationPrompt": {
                "maxAttempts": 2,
                "messages": [{"contentType": "PlainText",
                              "content": "Which term are you planning for — Winter, Summer, or Fall?"}]
            },
            "priority": 2
        }
    ],
    "dialogCodeHook": {"uri": lambda_arn, "messageVersion": "1.0"},
    "fulfillmentActivity": {"type": "CodeHook",
                            "codeHook": {"uri": lambda_arn, "messageVersion": "1.0"}}
}
with open(f"{base_dir}/intents/RecommendSchedule.json", "w") as f:
    json.dump(recommend_schedule, f, indent=2)

# === Bot configuration ===
bot = {
    "name": "CourseDegreePlannerBot",
    "description": "Helps students check prerequisites and get course recommendations.",
    "locale": "en-US",
    "childDirected": False,
    "idleSessionTTLInSeconds": 300,
    "clarificationPrompt": {
        "maxAttempts": 2,
        "messages": [{"contentType": "PlainText",
                      "content": "Sorry, I didn’t get that. Can you rephrase?"}]
    },
    "abortStatement": {
        "messages": [{"contentType": "PlainText",
                      "content": "Okay, ending this conversation now."}]
    },
    "intents": [
        {"name": "CheckPrerequisites", "version": "$LATEST"},
        {"name": "RecommendSchedule", "version": "$LATEST"}
    ],
    "slotTypes": [{"name": "TargetTerm", "version": "$LATEST"}],
    "voiceId": None
}
with open(f"{base_dir}/bot/CourseDegreePlannerBot.json", "w") as f:
    json.dump(bot, f, indent=2)

# === manifest.json ===
manifest = {
    "metadata": {"schemaVersion": "1.0", "importType": "LEX", "importFormat": "JSON"},
    "resource": {"name": "CourseDegreePlannerBot", "type": "BOT"}
}
with open(f"{base_dir}/manifest.json", "w") as f:
    json.dump(manifest, f, indent=2)

# === Zip everything ===
zip_name = "CourseDegreePlannerBot.zip"
with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as z:
    for root, _, files in os.walk(base_dir):
        for file in files:
            path = os.path.join(root, file)
            z.write(path, arcname=os.path.relpath(path, base_dir))

print(f"✅ Created {zip_name} successfully.")
