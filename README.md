# MediAssist-Healthcare-Data-Solutions
MediAssist is a healthcare solutions project focusing on medical coding and patient risk stratification using the MIMIC-IV dataset. It features a robust data pipeline for ingesting and analyzing healthcare data, aiming to enhance coding accuracy and improve patient outcomes through effective risk assessment.

## How to Create a Virtual Environment

Here’s a step-by-step guide to creating a virtual environment in your code space:

1. **Open Your Code Space Terminal**  
   You can usually find the terminal option in your IDE or directly through your code space interface.

2. **Install `virtualenv` (if not already installed)**  
   You may need to install `virtualenv` if it’s not already available. Run the following command:

   ```bash
   pip install virtualenv
    ```

3. ## Create a Virtual Environment

You can create a virtual environment by running:

```bash
virtualenv venv


4. **Activate the Virtual Environment**

### On macOS/Linux:

```bash
    source venv/bin/activate
```

5. ## Install Required Packages

Now that your virtual environment is active, you can install the required packages (e.g., `snowflake-connector-python`) without affecting the global Python environment:

```bash
pip install snowflake-connector-python
```

6. ## Deactivate the Virtual Environment

When you’re done working, you can deactivate the virtual environment by simply running:

```bash
deactivate
```

7. DBT
