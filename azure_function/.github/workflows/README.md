## Manual function deployment

az login

az account set --subscription <your-subscription-id>


cd azure_function

python -m venv .venv
source .venv/bin/activate     # Linux/macOS
# or
.venv\Scripts\activate        # Windows

pip install -r requirements.txt
