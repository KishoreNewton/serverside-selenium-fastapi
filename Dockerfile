FROM python:3.9

# Install dependencies
RUN apt-get update && \
    apt-get install -y unzip wget default-jdk \
    xvfb x11vnc fluxbox \
    libxss1 libappindicator1 \
    libasound2 libnss3 libxtst6

# Install Chrome browser
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install

# Install Allure command-line tool
ARG ALLURE_VERSION=2.17.3
RUN wget "https://github.com/allure-framework/allure2/releases/download/${ALLURE_VERSION}/allure-${ALLURE_VERSION}.zip" -O allure.zip && \
    unzip allure.zip -d /opt && \
    rm allure.zip && \
    ln -s /opt/allure-${ALLURE_VERSION}/bin/allure /usr/local/bin/allure

# Set the working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY . .

# Start the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

