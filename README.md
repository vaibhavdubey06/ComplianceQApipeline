# Compliance QA Pipeline

Compliance QA Pipeline is a brand-compliance auditing workflow built around Azure services and LangGraph. It ingests a YouTube video, extracts transcript and OCR insights through Azure Video Indexer, retrieves supporting rules from Azure AI Search, and uses Azure OpenAI to produce a compliance report.

## What it does

The current project flow is:

1. Download a YouTube video.
2. Upload the video to Azure Video Indexer.
3. Wait for indexing to complete and extract transcript and OCR text.
4. Retrieve relevant compliance rules from Azure AI Search.
5. Ask Azure OpenAI to evaluate the video against those rules.
6. Print a final compliance report in the console.

## Project Structure

- `main.py` - CLI entry point that runs the workflow.
- `backend/src/graph/state.py` - Shared LangGraph state schema.
- `backend/src/graph/nodes.py` - Indexing and compliance auditing nodes.
- `backend/src/graph/workflow.py` - LangGraph workflow wiring.
- `backend/src/services/video_indexer.py` - Azure Video Indexer and YouTube download integration.
- `backend/scripts/index_documents.py` - Indexes PDF policy documents into Azure AI Search.
- `backend/data/` - Source PDF documents used as the compliance knowledge base.
- `backend/src/api/server.py` - Empty placeholder for a future API server.
- `backend/src/api/telemetry.py` - Empty placeholder for future telemetry setup.

## Requirements

- Python 3.11 or newer
- Azure Video Indexer account and permissions
- Azure OpenAI deployment for chat and embeddings
- Azure AI Search index
- Azure credentials available through environment variables or DefaultAzureCredential

The codebase currently expects the Azure services to be configured before you run the workflow. Without them, the indexing or audit steps will fail early.

## Installation

Create and activate a virtual environment, then install the project dependencies from `pyproject.toml`:

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -U pip
pip install azure-identity azure-monitor-opentelemetry azure-search-documents azure-storage-blob fastapi firecrawl-py langchain langchain-community langchain-openai langgraph langsmith opentelemetry-instrumentation-fastapi pandas psycopg2-binary pydantic pypdf python-dotenv redis requests sqlalchemy streamlit uvicorn yt-dlp
```

The repository does not currently define a build backend or command entry points, so direct package installation is the most reliable setup path right now.

## Environment Variables

The workflow expects the following environment variables:

- `AZURE_VI_ACCOUNT_ID`
- `AZURE_VI_LOCATION`
- `AZURE_SUBSCRIPTION_ID`
- `AZURE_RESOURCE_GROUP`
- `AZURE_VI_NAME`
- `AZURE_OPENAI_CHAT_DEPLOYMENT`
- `AZURE_OPENAI_API_VERSION`
- `AZURE_SEARCH_ENDPOINT`
- `AZURE_SEARCH_API_KEY`
- `AZURE_SEARCH_INDEX_NAME`
- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_API_KEY`
- `AZURE_OPENAI_EMBEDDING_DEPLOYMENT`

Put them in a local `.env` file or export them in your shell before running the scripts.

## How To Run

### 1. Index the knowledge base

Place PDF policy or guideline documents in `backend/data/`, then run:

```bash
python backend/scripts/index_documents.py
```

This chunks the PDFs and uploads embeddings to the configured Azure AI Search index.

### 2. Run the compliance audit workflow

Run the CLI entry point:

```bash
python main.py
```

The default example video URL is hard-coded in `main.py`. You can replace it with another YouTube URL if needed.

## Workflow Summary

The LangGraph workflow currently has two nodes:

- `indexer` - downloads the YouTube video, uploads it to Azure Video Indexer, waits for processing, and extracts transcript/OCR data.
- `auditor` - retrieves relevant rules from Azure AI Search and uses Azure OpenAI to classify compliance findings.

The workflow state is defined in `backend/src/graph/state.py` and includes the video metadata, transcript, OCR text, compliance results, final status, final report, and any execution errors.

The document indexing utility in `backend/scripts/index_documents.py` loads PDF files from `backend/data/`, chunks them, embeds the text with Azure OpenAI, and pushes vectors into the configured Azure AI Search index.

## Notes

- `backend/src/api/server.py` is currently empty, so there is no running HTTP API yet.
- `requirements.txt` currently only contains `uv`; it is not the main dependency list.
- The indexing and audit steps depend on valid Azure service access and correctly configured deployment names.
- `main.py` currently uses a hard-coded sample YouTube URL for the audit run.
- `backend/data/` already contains two sample PDF policy documents that can be indexed immediately.

## License

No license file is included yet.
