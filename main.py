from fastapi import UploadFile, File, Request, FastAPI
from pdf_processor import process_pdf

app = FastAPI()


@app.get("/")
async def read_root(request: Request):
    base_url = request.base_url
    usage_message = (
        f"Welcome to the Summarizer Application!\n\n"
        f"Usage:\n"
        f"1. Upload a PDF file using the following `curl` command:"
        f"   curl -X POST -F 'file=@path/to/your/file.pdf' {base_url}upload/"
        f" to receive the summary of the uploaded PDF file as the response."
    )
    return {"message": usage_message}


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    summary_text = process_pdf(file)
    if summary_text is None:
        return {"error": "Only PDF files are supported"}
    else:
        return {"summary": summary_text}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
    )
