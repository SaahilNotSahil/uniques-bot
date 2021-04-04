import subprocess


def run(filename, extension, language, code):
    with open(f"{filename}.{extension}", "w") as c:
        c.write(code)
    c.close()

    compile_error = ''
    output = ''
    runtime_error = ''

    if language.startswith("py"):
        process = subprocess.Popen(
            ["python", f"{filename}.{extension}"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )

        output, runtime_error = process.communicate()

        return [compile_error, output, runtime_error]
    elif language == "c":
        process = subprocess.Popen(
            ["gcc", "-o", f"{filename}c", f"{filename}.{extension}"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )

        output, compile_error = process.communicate()

        if compile_error is None:
            process = subprocess.Popen(
                [f"./{filename}c"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )

            output, runtime_error = process.communicate()

        return [compile_error, output, runtime_error]
    elif language == "c++" or language == "cpp":
        process = subprocess.Popen(
            ["g++", "-o", f"{filename}cpp", f"{filename}.{extension}"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )

        output, compile_error = process.communicate()

        if compile_error is None:
            process = subprocess.Popen(
                [f"./{filename}cpp"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )

            output, runtime_error = process.communicate()

        return [compile_error, output, runtime_error]
