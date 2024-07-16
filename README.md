# email-classification
Email address classification using LLM

Tested with Python 3.11.9

1. git checkout https://github.com/kemperd/email-classification
2. conda create -n email-classification python=3.11.9
3. conda activate email-classification
4. pip install -r requirements.txt
5. python server.py
6. Wait until server has fully started. This takes some time due to downloading models at the first run.
7. Switch to another terminal and run: python client.py
8. Output is written to output.csv
