
import datetime
import webbrowser
import wikipedia
import subprocess
import ast
import operator

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod
}


def calculate(expression):

    def evaluate(node):

        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value

        if isinstance(node, ast.BinOp) and type(node.op) in OPERATORS:
            return OPERATORS[type(node.op)](
                evaluate(node.left),
                evaluate(node.right)
            )

        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            value = evaluate(node.operand)
            return value if isinstance(node.op, ast.UAdd) else -value

        raise ValueError("Invalid calculation")

    tree = ast.parse(expression, mode="eval")
    return evaluate(tree.body)


def execute_command(command):

    command = command.lower().strip()

    if not command:
        return "Please enter a command."

    # Exit
    if command in ["exit", "quit", "stop", "bye", "band ho jao"]:
        return "EXIT"

    # Greetings
    if any(word in command for word in [
        "hello", "hi", "hey", "namaste", "good morning",
        "good evening", "good afternoon"
    ]):
        return "Hello! I am eJARVIS. I am listening. How can I help you?"

    # Voice test
    if any(phrase in command for phrase in [
        "can you speak",
        "speak to me",
        "say something",
        "talk to me",
        "can you hear me"
    ]):
        return "Yes! I can speak. I can hear your commands when your microphone is working. How can I help you?"

    # Identity
    if "who are you" in command or "tum kaun ho" in command:
        return "I am eJARVIS 2.0, your personal desktop voice assistant."

    # Time
    if "time" in command or "samay" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        return f"The current time is {current_time}."

    # Date
    if "date" in command or "today" in command or "tarikh" in command:
        today = datetime.datetime.now().strftime("%d %B %Y")
        return f"Today's date is {today}."

    # Open websites
    if "open google" in command or "google kholo" in command:
        webbrowser.open("https://www.google.com")
        return "Opening Google."

    if "open youtube" in command or "youtube kholo" in command:
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube."

    if "open gmail" in command or "gmail kholo" in command:
        webbrowser.open("https://mail.google.com")
        return "Opening Gmail."

    # Windows applications
    if "open notepad" in command or "notepad kholo" in command:
        subprocess.Popen("notepad.exe")
        return "Opening Notepad."

    if "open calculator" in command or "calculator kholo" in command:
        subprocess.Popen("calc.exe")
        return "Opening Calculator."

    # Google search
    if command.startswith("search ") or command.startswith("google search "):
        query = command.replace("google search ", "", 1)

        if query == command:
            query = command.replace("search ", "", 1)

        webbrowser.open(
            "https://www.google.com/search?q=" + query.replace(" ", "+")
        )
        return f"Searching Google for {query}."

    # YouTube search
    if command.startswith("play "):
        song = command.replace("play ", "", 1)

        webbrowser.open(
            "https://www.youtube.com/results?search_query="
            + song.replace(" ", "+")
        )

        return f"Searching YouTube for {song}."

    # Calculator
    if command.startswith("calculate "):
        expression = command.replace("calculate ", "", 1)

        try:
            result = calculate(expression)
            return f"The answer is {result}."

        except Exception:
            return "Sorry, I could not calculate that expression."

    # Wikipedia
    if command.startswith("wikipedia "):
        topic = command.replace("wikipedia ", "", 1)

        try:
            wikipedia.set_lang("en")
            return wikipedia.summary(topic, sentences=2)

        except Exception:
            return "Sorry, I could not find information on Wikipedia."

    # Thanks
    if "thank" in command or "shukriya" in command:
        return "You're welcome! I am always ready to help."

    # Help
    if "help" in command or "commands" in command:
        return (
            "You can ask me to open Google, YouTube, Gmail, "
            "Notepad, Calculator, tell you the time or date, "
            "search Google, play videos, calculate expressions, "
            "or search Wikipedia."
        )

    return "Sorry, I don't understand that command yet. Please try another command."
