# import shutil
# import tempfile
# from zipfile import ZipFile
# import subprocess
# from fastapi import FastAPI, UploadFile, File
# from fastapi.responses import FileResponse
# 
# app = FastAPI()
# 
# @app.post("/run_tests/")
# async def run_tests(test_file: UploadFile = File(...)):
#     # Save the test file to a temporary location
#     temp_dir = tempfile.mkdtemp()
#     test_file_path = f"{temp_dir}/{test_file.filename}"
#     with open(test_file_path, "wb") as f:
#         shutil.copyfileobj(test_file.file, f)
# 
#     # Run the tests using pytest and Selenium in headless and headful modes
#     subprocess.run(["pytest", test_file_path, "-m", "headless or headful", "--alluredir", "allure-results"])
# 
#     # Generate Allure report
#     subprocess.run(["allure", "generate", "allure-results", "-o", "allure-report", "--clean"])
# 
#     # Zip the Allure report folder
#     shutil.make_archive("allure-report", "zip", "allure-report")
# 
#     # Send the zipped report to the frontend
#     return FileResponse("allure-report.zip", media_type="application/zip")

from fastapi import FastAPI, File, UploadFile
import os
import subprocess
import shutil
import zipfile
from starlette.responses import FileResponse

app = FastAPI()

@app.post("/run_tests/")
async def run_tests(test_file: UploadFile = File(...)):
    with open("sample_test.py", "wb") as f:
        f.write(await test_file.read())

    pytest_result = subprocess.run(
        ["pytest", "-v", "--alluredir=allure-results", "sample_test.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    print("Pytest stdout:", pytest_result.stdout)
    print("Pytest stderr:", pytest_result.stderr)

    allure_result = subprocess.run(
        ["allure", "generate", "allure-results", "-o", "allure-report", "--clean"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    print("Allure stdout:", allure_result.stdout)
    print("Allure stderr:", allure_result.stderr)

    shutil.make_archive("allure-report", "zip", "allure-report")

    return FileResponse("allure-report.zip", media_type="application/zip")

