# Hand Tracking Application

This project is a simple hand tracking application that utilizes a camera to detect and track hands in real-time. It is built using Python and leverages libraries such as OpenCV for image processing.

## Project Structure

```
hand-tracking-app
├── src
│   ├── main.py               # Entry point of the application
│   ├── hand_tracker.py       # Contains the HandTracker class for hand detection
│   ├── camera_handler.py     # Manages camera input and frame capture
│   └── utils
│       └── __init__.py      # Utility functions and constants
├── requirements.txt          # Project dependencies
├── config.py                 # Configuration settings for the application
└── README.md                 # Documentation for the project
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd hand-tracking-app
   ```

2. **Install dependencies:**
   Make sure you have Python installed, then run:
   ```
   pip install -r requirements.txt
   ```

3. **Configure the application:**
   Modify the `config.py` file to set your desired camera resolution and model parameters.

4. **Run the application:**
   Execute the following command to start the hand tracking application:
   ```
   python src/main.py
   ```

## Usage

Once the application is running, it will open a window displaying the camera feed with hand tracking overlays. You can use your hands to interact with the application.

## Contributing

Feel free to submit issues or pull requests if you have suggestions or improvements for the project.

## License

This project is licensed under the MIT License. See the LICENSE file for details.