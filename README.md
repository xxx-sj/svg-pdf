# SVG to PDF Converter (Docker Version)

This project provides a web server, running in a Docker container, to convert SVG files (including those with Korean, Japanese, and Chinese text) into PDF files.

Using Docker solves system-level dependency issues (like the Cairo library) by creating a self-contained, portable environment for the application.

## Prerequisites

- [Docker](https://www.docker.com/get-started) must be installed and running on your system.

## How to Run

1.  **Build the Docker image:**
    Open your terminal in the project directory and run the following command. This will build the Docker image and tag it as `svg-converter`.
    ```bash
    docker build -t svg-converter .
    ```

2.  **Run the Docker container:**
    Once the image is built, run the following command to start the container. This will run the server in the background and map port 5000 of the container to port 5000 on your local machine.
    ```bash
    docker run -d -p 5000:5000 --name svg-converter-app svg-converter
    ```
    - `-d`: Run in detached mode (in the background).
    - `-p 5000:5000`: Map port 5000 from the host to the container.
    - `--name svg-converter-app`: Give the container a memorable name.

3.  **Check if the server is running:**
    You can check the container's logs to ensure it started correctly:
    ```bash
    docker logs svg-converter-app
    ```
    You should see output indicating that the Flask server is running on `http://0.0.0.0:5000/`.

## API Endpoint: `/convert`

- **URL:** `http://localhost:5000/convert`
- **Method:** `POST`
- **Body:** `form-data` with a `file` key containing the SVG file.

### Example Usage with `curl`

You can test the endpoint from your terminal using `curl`.

```bash
curl -X POST -F "file=@sample.svg" http://localhost:5000/convert -o converted_output.pdf
```

- This command sends the `sample.svg` file from your project directory to the running server.
- The converted PDF will be saved as `converted_output.pdf` in your current directory.

## How to Stop the Container

When you are finished, you can stop and remove the container using its name:

```bash
docker stop svg-converter-app
docker rm svg-converter-app
```

## Files

- `app.py`: The Flask web server application.
- `Dockerfile`: Instructions to build the Docker image.
- `sample.svg`: A sample SVG file for testing.
- `requirements.txt`: A list of Python libraries needed for the project. 